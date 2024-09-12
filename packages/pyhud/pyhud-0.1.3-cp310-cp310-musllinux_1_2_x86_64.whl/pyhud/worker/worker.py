import asyncio
import sys
import threading
from typing import TYPE_CHECKING, Any, Optional

from .._internal import worker_queue
from ..client import Client, HudClientException, get_client  # noqa: F401
from ..collectors import PerformanceMonitor, get_loaded_modules, runtime_info
from ..config import config
from ..declarations import Declaration, DeclarationsAggregator
from ..exception_handler import FatalErrorData
from ..hook import set_hook
from ..invocations_handler import InvocationsHandler
from ..logging import internal_logger, send_logs_handler
from ..run_mode import disable_hud, should_run_hud
from ..schemas.events import WorkloadData
from ..utils import suppress_exceptions_async, suppress_exceptions_sync
from ..workload_metadata import get_cpu_limit, get_workload_metadata
from .task_manager import TaskManager

if TYPE_CHECKING:
    from collections import deque

worker_thread = None  # type: Optional[threading.Thread]


def should_run_worker() -> bool:
    return bool(
        should_run_hud() and worker_thread and not should_finalize_worker(worker_thread)
    )


def should_finalize_worker(worker_thread: threading.Thread) -> bool:
    for thread in threading.enumerate():
        if thread == worker_thread:
            continue
        if (
            not thread.daemon
            and thread.is_alive()
            and thread.name != "pydevd.CheckAliveThread"
        ):
            return False
    return True


class Worker:
    def __init__(
        self, key: Optional[str] = None, service: Optional[str] = None
    ) -> None:
        self.key = key
        self.service = service
        self.declarations = DeclarationsAggregator()
        self.invocationsHandler = InvocationsHandler()
        self.client = None  # type: Optional[Client]
        self.task_manager = TaskManager()

    async def run(self) -> None:
        try:
            self.client = get_client(self.key, self.service, is_async=True)
            await self.client.init_session()
        except Exception as e:
            if self.client:
                await self.client.close()
            disable_hud()
            if not isinstance(e, HudClientException):
                internal_logger.exception("Failed to initialize client")
            return

        try:
            pod_cpu_limit = get_cpu_limit()
            workload_metadata = await get_workload_metadata(pod_cpu_limit)
            perf_monitor = PerformanceMonitor(pod_cpu_limit)

            self._register_tasks(perf_monitor, workload_metadata)

            await self._send_runtime()  # We don't need to send runtime info periodically

            await self.task_manager.wait_for_tasks()
        except Exception as e:
            internal_logger.exception("Exception in worker loop: {}".format(e))
        finally:
            await self._finalize()

    def _register_tasks(
        self, perf_monitor: PerformanceMonitor, workload_metadata: WorkloadData
    ) -> None:
        self.task_manager.register_periodic_task(
            self._dump_declarations, config.declarations_flush_interval
        )
        self.task_manager.register_periodic_task(
            self._dump_invocations, config.invocations_flush_interval
        )
        self.task_manager.register_periodic_task(
            self._dump_logs, config.logs_flush_interval
        )
        self.task_manager.register_periodic_task(
            self._send_workload_data,
            config.workload_data_flush_interval,
            workload_metadata,
        )
        self.task_manager.register_periodic_task(
            self._send_loaded_modules, config.modules_report_interval
        )
        self.task_manager.register_periodic_task(
            self._send_performance, config.performace_report_interval, perf_monitor
        )
        self.task_manager.register_periodic_task(self.check_should_run, 1)

    async def check_should_run(self) -> None:
        while should_run_worker():
            await asyncio.sleep(1)
        self.task_manager.stop_running_tasks()

    async def _finalize(self) -> None:
        if self.client:
            await self.client.close()

        if not should_run_hud():
            # Hud is disabled, so we don't need to dump the remaining items
            return

        # Switch to the synchronous client for final processing
        session_id = self.client.session_id if self.client else None
        self.client = get_client(self.key, self.service, is_async=False)
        if session_id:
            self.client.set_session_id(session_id)

        try:
            await self._final_dump()
        except Exception:
            internal_logger.exception("Exception during final dump")

    async def _final_dump(self) -> None:
        await self._dump_declarations()
        await self._dump_invocations()
        await self._dump_logs()

    @suppress_exceptions_sync(default_return_value=lambda: None)
    def process_queue(self, queue: "deque[Any]") -> None:
        """
        This function is currently only called when dumping declarations.
        If we need to process other types of items in the future, this probably needs to be a task.
        """
        qsize = len(queue)
        if not qsize:
            return
        if hasattr(queue, "maxlen") and queue.maxlen == qsize:
            internal_logger.warning("Event queue is full")
        try:
            for item in iter(queue.popleft, None):
                if isinstance(item, Declaration):
                    self.declarations.add_declaration(item)
                else:
                    internal_logger.warning("Invalid item type: {}".format(type(item)))
                qsize -= 1
                if qsize == 0:
                    break
        except IndexError:
            pass

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _dump_declarations(self) -> None:
        # Currently, only declarations are processed in the queue so we only process the queue here
        self.process_queue(worker_queue)
        latest_declarations = self.declarations.get_and_clear_declarations()
        if latest_declarations and self.client:
            await self.client.send_declarations(latest_declarations)

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _dump_invocations(self) -> None:
        invocations = self.invocationsHandler.get_and_clear_invocations()
        if invocations and self.client:
            await self.client.send_invocations(invocations)

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _dump_logs(self) -> None:
        logs = send_logs_handler.get_and_clear_logs()
        if logs.logs and self.client:
            await self.client.send_logs(logs)

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _send_workload_data(self, workload_metadata: WorkloadData) -> None:
        if self.client:
            await self.client.send_workload_data(workload_metadata)

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _send_loaded_modules(self) -> None:
        modules = get_loaded_modules()
        if self.client:
            await self.client.send_modules(modules)

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _send_performance(self, perf_monitor: PerformanceMonitor) -> None:
        performance = perf_monitor.monitor_process()
        if config.log_performance:
            internal_logger.info("performance data", data=performance.to_json_data())
        if self.client:
            await self.client.send_performance(performance)

    @suppress_exceptions_async(default_return_factory=lambda: None)
    async def _send_runtime(self) -> None:
        runtime = runtime_info()
        if self.client:
            await self.client.send_runtime(runtime)


def init_hud_thread(key: Optional[str] = None, service: Optional[str] = None) -> None:
    set_hook()  # Ensure the hook is set before starting the worker thread

    global worker_thread
    if worker_thread is not None and worker_thread.is_alive():
        internal_logger.info("Worker thread is already running")
        return

    if not should_run_hud():
        disable_hud()
        return

    def target() -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        worker = Worker(key, service)
        try:
            loop.run_until_complete(worker.run())
        except Exception as e:
            try:
                disable_hud()
                internal_logger.exception("Exception in worker thread target")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                client = get_client(key, service, False)
                fatal_error = FatalErrorData(
                    exc_type=exc_type,
                    exc_value=exc_value,
                    exc_traceback=exc_traceback,
                )
                client.send_fatal_error(fatal_error)
            except Exception:
                internal_logger.exception(
                    "Failed to send fatal error", data={"original_error": str(e)}
                )
        finally:
            loop.stop()
            loop.close()

    worker_thread = threading.Thread(target=target)
    worker_thread.start()
