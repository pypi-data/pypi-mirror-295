import asyncio
import time
from typing import Any, Callable, List  # noqa: F401

from ..logging import internal_logger


def create_task(
    function: Callable[..., Any], *args: Any, **kwargs: Any
) -> "asyncio.Task[Any]":
    coroutine = function(*args, **kwargs)
    if hasattr(asyncio, "create_task"):
        return asyncio.create_task(coroutine)
    else:
        loop = asyncio.get_event_loop()
        return loop.create_task(coroutine)


class TaskManager:
    def __init__(self) -> None:
        self.tasks = []  # type: List[asyncio.Task[Any]]
        self.stop_event = asyncio.Event()

    async def _create_periodic_task(
        self, function: Callable[..., Any], interval: int, *args: Any, **kwargs: Any
    ) -> None:
        # Wait for the first interval before running the function
        try:
            await asyncio.wait_for(self.stop_event.wait(), timeout=interval)
        except (asyncio.TimeoutError, TimeoutError):
            pass

        while not self.stop_event.is_set():
            start_time = time.time()
            try:
                await function(*args, **kwargs)
            except Exception as e:
                internal_logger.exception(
                    "Exception in periodic task: {}".format(e), exc_info=e
                )
            elapsed_time = time.time() - start_time
            sleep_time = max(0, interval - elapsed_time)
            try:
                await asyncio.wait_for(self.stop_event.wait(), timeout=sleep_time)
            except (asyncio.TimeoutError, TimeoutError):
                pass

    def register_periodic_task(
        self, function: Callable[..., Any], interval: int, *args: Any, **kwargs: Any
    ) -> None:
        task = create_task(
            self._create_periodic_task, function, interval, *args, **kwargs
        )
        self.tasks.append(task)

    def stop_running_tasks(self) -> None:
        self.stop_event.set()

    async def wait_for_tasks(self) -> None:
        await asyncio.gather(
            *self.tasks, return_exceptions=True
        )  # return_exceptions=True is used to suppress exceptions
