from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar

from .logging import internal_logger

T = TypeVar("T")


def suppress_exceptions_async(
    default_return_factory: Callable[[], T],
) -> Callable[
    [Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]
]:
    def decorator(
        func: Callable[..., Coroutine[Any, Any, T]]
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                internal_logger.exception(
                    "Exception in {}: {}".format(func.__name__, e)
                )
                return default_return_factory()

        return async_wrapper

    return decorator


def suppress_exceptions_sync(
    default_return_value: Callable[[], T],
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except Exception:
                internal_logger.exception(
                    "Supressed exception in function", data=dict(function=func.__name__)
                )
                return default_return_value()

        return sync_wrapper

    return decorator
