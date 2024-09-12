import os

from ._internal import worker_queue
from .logging import internal_logger, send_logs_handler
from .native import (
    get_and_swap_aggregations,
    get_hud_running_mode,
    set_hud_running_mode,
)


def should_run_hud() -> bool:
    hud_env_var = os.environ.get("HUD_ENABLE", False)
    if hud_env_var is False:
        internal_logger.info("HUD_ENABLE is not set")
        return False
    if not (
        isinstance(hud_env_var, str)
        and hud_env_var.lower() == "true"
        or hud_env_var == "1"
    ):
        internal_logger.info("HUD_ENABLE is not set to 'true' or '1'")
        return False
    if not get_hud_running_mode():
        internal_logger.info("HUD is not enabled")
        return False
    return True


def disable_hud() -> None:
    internal_logger.info(
        "Disabling HUD"
    )  # It will print to the console if HUD_DEBUG is set
    set_hud_running_mode(False)
    worker_queue.clear()

    get_and_swap_aggregations().clear()
    # we have two dictionaries swapping
    get_and_swap_aggregations().clear()

    send_logs_handler.get_and_clear_logs()


def enable_hud() -> None:
    set_hud_running_mode(True)
