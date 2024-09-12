import asyncio
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, List, Optional, Sequence, Union  # noqa: F401

import aiohttp
import requests
from requests.adapters import HTTPAdapter, Retry

from . import version as hud_version
from .config import config
from .logging import internal_logger
from .schemas.events import (
    Event,
    FunctionDeclaration,
    Invocations,
    LoadedModules,
    Performance,
    Runtime,
    WorkloadData,
)
from .schemas.requests import (
    Batch as BatchRequest,
)
from .schemas.requests import (
    FatalError as FatalErrorRequest,
)
from .schemas.requests import (
    Init as InitRequest,
)
from .schemas.requests import (
    Logs as LogsRequest,
)
from .schemas.requests import (
    Send as SendRequest,
)

if TYPE_CHECKING:
    # We need it to avoid circular imports
    from .exception_handler import FatalErrorData


class HudClientException(Exception):
    pass


class Client(ABC):
    session_id = None  # type: Optional[str]

    def set_session_id(self, session_id: str) -> None:
        internal_logger.info("Setting session_id", data=dict(session_id=session_id))
        self.session_id = session_id

    @abstractmethod
    async def init_session(self) -> None:
        pass

    @abstractmethod
    async def send_invocations(self, invocations: List[Invocations]) -> None:
        pass

    @abstractmethod
    async def send_declarations(self, declarations: List[FunctionDeclaration]) -> None:
        pass

    @abstractmethod
    async def send_logs(self, logs: LogsRequest) -> None:
        pass

    @abstractmethod
    async def send_workload_data(self, data: WorkloadData) -> None:
        pass

    @abstractmethod
    async def send_runtime(self, data: Runtime) -> None:
        pass

    @abstractmethod
    async def send_performance(self, data: Performance) -> None:
        pass

    @abstractmethod
    async def send_modules(self, modules: LoadedModules) -> None:
        pass

    @abstractmethod
    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        pass

    async def close(self) -> None:
        return


class ConsoleClient(Client):
    async def init_session(self) -> None:
        print("init_session")

    async def send_invocations(self, invocations: List[Invocations]) -> None:
        print("send_invocations for {} invocations".format(len(invocations)))
        for invocation in invocations:
            print(invocation.to_json_data())

    async def send_declarations(self, declarations: List[FunctionDeclaration]) -> None:
        print("send_declarations for {} declarations".format(len(declarations)))
        for declaration in declarations:
            print(declaration.to_json_data())

    async def send_logs(self, logs: LogsRequest) -> None:
        print("send_logs for {} logs".format(len(logs.logs)))
        for log in logs.logs:
            print({"log": log.to_json_data()})

    async def send_workload_data(self, data: WorkloadData) -> None:
        print("send_workload_data: {}".format(data.to_json_data()))

    async def send_runtime(self, data: Runtime) -> None:
        print("send_runtime: {}".format(data.to_json_data()))

    async def send_performance(self, data: Performance) -> None:
        print("send_performance: {}".format(data.to_json_data()))

    async def send_modules(self, modules: LoadedModules) -> None:
        print("send_modules: {}".format(modules.to_json_data()))

    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        fatal_error_request = FatalErrorRequest(
            fatal_error,
            send_time=datetime.now(timezone.utc),
        )
        print("send_fatal_error: {}".format(fatal_error_request.to_json_data()))


class JSONClient(Client):
    def __init__(self, path: str) -> None:
        self.path = path

    def _write_to_json(self, data: Any) -> None:
        with open(self.path, mode="a") as file:
            file.write(json.dumps(data) + "\n")

    async def init_session(self) -> None:
        self._write_to_json({"type": "init_session"})

    async def send_invocations(self, invocations: List[Invocations]) -> None:
        for invocation in invocations:
            self._write_to_json({"type": "invocation", **invocation.to_json_data()})

    async def send_declarations(self, declarations: List[FunctionDeclaration]) -> None:
        for declaration in declarations:
            self._write_to_json({"type": "declaration", **declaration.to_json_data()})

    async def send_logs(self, logs: LogsRequest) -> None:
        for log in logs.logs:
            self._write_to_json({"type": "log", **log.to_json_data()})

    async def send_workload_data(self, data: WorkloadData) -> None:
        self._write_to_json({"type": "workload_data", **data.to_json_data()})

    async def send_runtime(self, data: Runtime) -> None:
        self._write_to_json({"type": "runtime", **data.to_json_data()})

    async def send_performance(self, data: Performance) -> None:
        self._write_to_json({"type": "performance", **data.to_json_data()})

    async def send_modules(self, modules: LoadedModules) -> None:
        self._write_to_json({"type": "modules", **modules.to_json_data()})

    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        fatal_error_request = FatalErrorRequest(
            fatal_error, send_time=datetime.now(timezone.utc)
        )
        self._write_to_json(
            {"type": "fatal_error", **fatal_error_request.to_json_data()}
        )


class BaseHttpClient(Client):
    source = "python-sdk"

    def __init__(self, host: str, api_key: str, service: str) -> None:
        self.host = host
        self.api_key = api_key
        self.service = service
        self.session = (
            None
        )  # type: Optional[Union[aiohttp.ClientSession, requests.Session]]
        self.session_id = None  # type: Optional[str]
        self.max_retries = config.api_max_retries
        self.backoff_factor = config.api_backoff_factor
        self.status_forcelist = [429, 500, 502, 503, 504]

    @abstractmethod
    async def _send(self, uri: str, request: Any, request_type: str) -> Any:
        pass

    async def init_session(self) -> None:
        internal_logger.debug(
            "Initializing session for service", data=dict(service=self.service)
        )
        request = InitRequest(
            token=self.api_key,
            service=self.service,
            start_time=datetime.now(timezone.utc),
            type=self.source,
            sdk_version=hud_version,
        )
        res = await self._send("sink/init", request.to_json_data(), "Init")
        session_id = res["sessionId"]
        self.set_session_id(session_id)

    async def _send_batch(self, arr: Sequence[Event]) -> None:
        size = config.batch_size
        for i in range(0, len(arr), size):
            request = BatchRequest(
                arr=[i.to_json_data() for i in arr[i : i + size]],
                event_version=arr[0].get_version(),
                send_time=datetime.now(timezone.utc),
                source=self.source,
                type=arr[0].get_type(),
            )
            await self._send("sink/batch", request.to_json_data(), arr[0].get_type())

    async def _send_single(self, event: Event) -> None:
        request = SendRequest(
            event_version=event.get_version(),
            send_time=datetime.now(timezone.utc),
            source=self.source,
            type=event.get_type(),
            raw=event.to_json_data(),
        )
        await self._send("sink/send", request.to_json_data(), event.get_type())

    async def send_invocations(self, invocations: List[Invocations]) -> None:
        internal_logger.info("Sending invocations", data=dict(count=len(invocations)))
        await self._send_batch(invocations)

    async def send_declarations(self, declarations: List[FunctionDeclaration]) -> None:
        internal_logger.info("Sending declarations", data=dict(count=len(declarations)))
        await self._send_batch(declarations)

    async def send_logs(self, logs: LogsRequest) -> None:
        await self._send("sink/logs", logs.to_json_data(), "Logs")

    async def send_workload_data(self, data: WorkloadData) -> None:
        internal_logger.info("Sending workload data")
        await self._send_single(data)

    async def send_runtime(self, data: Runtime) -> None:
        internal_logger.info("Sending runtime data")
        await self._send_single(data)

    async def send_performance(self, data: Performance) -> None:
        internal_logger.info("Sending performance data")
        await self._send_single(data)

    async def send_modules(self, modules: LoadedModules) -> None:
        internal_logger.info("Sending modules data")
        await self._send_single(modules)


class AsyncHttpClient(BaseHttpClient):
    def __init__(self, host: str, api_key: str, service: str) -> None:
        super().__init__(host, api_key, service)
        self.session = aiohttp.ClientSession()  # type: aiohttp.ClientSession
        self.timeout = None  # type: Optional[Union[aiohttp.ClientTimeout, float]]
        if hasattr(aiohttp, "ClientTimeout"):
            self.timeout = aiohttp.ClientTimeout(total=config.api_timeout)
        else:
            self.timeout = config.api_timeout

    async def _send(self, uri: str, request: Any, request_type: str) -> Any:
        url = "{}/{}".format(self.host, uri)
        headers = {"Content-Type": "application/json"}

        if self.session_id:
            headers["X-Session-ID"] = self.session_id

        for attempt in range(self.max_retries):
            try:
                async with self.session.post(
                    url,
                    data=json.dumps(request),
                    headers=headers,
                    timeout=self.timeout,  # type: ignore[arg-type]
                ) as res:
                    if (
                        res.status in self.status_forcelist
                        and attempt < self.max_retries - 1
                    ):
                        await asyncio.sleep(self.backoff_factor * (2**attempt))
                        continue
                    res.raise_for_status()
                    return await res.json()
            except Exception as e:
                if (
                    isinstance(e, asyncio.TimeoutError)
                    and attempt < self.max_retries - 1
                ):
                    await asyncio.sleep(self.backoff_factor * (2**attempt))
                    continue
                internal_logger.exception(
                    "Failed to send request", data=dict(type=request_type)
                )
                raise

    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        raise NotImplementedError(
            "send_fatal_error is not implemented for async client"
        )

    async def close(self) -> None:
        await self.session.close()


class SyncHttpClient(BaseHttpClient):
    def __init__(self, host: str, api_key: str, service: str) -> None:
        super().__init__(host, api_key, service)
        self.session = requests.Session()  # type: requests.Session
        self.session.mount(
            self.host,
            HTTPAdapter(
                max_retries=Retry(
                    total=config.api_max_retries,
                    backoff_factor=config.api_backoff_factor,
                    status_forcelist=self.status_forcelist,
                )
            ),
        )

    def set_session_id(self, session_id: str) -> None:
        super().set_session_id(session_id)
        self.session.headers["X-Session-ID"] = session_id

    async def _send(self, uri: str, request: Any, request_type: str) -> Any:
        return self._send_sync(uri, request, request_type)

    def _send_sync(self, uri: str, request: Any, request_type: str) -> Any:
        try:
            with self.session.post(
                "{}/{}".format(self.host, uri),
                json=request,
            ) as res:
                res.raise_for_status()
                return res.json()
        except Exception:
            internal_logger.exception(
                "Failed to send request", data=dict(type=request_type)
            )
            raise

    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        request = FatalErrorRequest(
            fatal_error,
            send_time=datetime.now(timezone.utc),
            token=self.api_key,
            service=self.service,
        )
        self._send_sync("sink/redline", request.to_json_data(), "FatalError")


def get_client(
    key: Optional[str] = None,
    service: Optional[str] = None,
    is_async: bool = False,
) -> Client:

    client_type = config.client_type
    if client_type == "console":
        return ConsoleClient()
    if client_type == "json":
        return JSONClient(config.json_path)
    if client_type == "http":
        host = config.host
        key = key or os.environ.get("HUD_KEY", None)
        service = service or os.environ.get("HUD_SERVICE", None)

        if not host:
            internal_logger.warning("HUD_HOST is not set")
            raise HudClientException("HUD_HOST is not set")
        if not key:
            internal_logger.warning("HUD_KEY is not set")
            raise HudClientException("HUD_KEY is not set")
        if not service:
            internal_logger.warning("HUD_SERVICE is not set")
            raise HudClientException("HUD_SERVICE is not set")
        if is_async:
            return AsyncHttpClient(
                host,
                key,
                service,
            )
        return SyncHttpClient(
            host,
            key,
            service,
        )
    raise HudClientException("Unknown client type: {}".format(client_type))
