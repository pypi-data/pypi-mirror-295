from .__version__ import version as version
from .hook import set_hook as set_hook
from .logging import internal_logger as internal_logger
from .worker.worker import init_hud_thread as init

del internal_logger

__all__ = ["version", "set_hook", "init"]
