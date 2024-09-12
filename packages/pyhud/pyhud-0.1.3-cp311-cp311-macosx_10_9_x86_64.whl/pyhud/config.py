import os

DEFAULT_HUD_HOST = "https://api-prod.hud.io"
DEFAULT_CLIENT = "http"
DEFAULT_DEBUG_PREFIX = "[HUD]"
DEFAULT_JSON_PATH = "hud.json"


class Config:
    def __init__(self) -> None:
        self.host = os.environ.get("HUD_HOST", DEFAULT_HUD_HOST)
        self.logs_queue_size = int(os.environ.get("HUD_LOGS_QUEUE_SIZE", 4000))
        self.batch_size = int(os.environ.get("HUD_BATCH_SIZE", 100))
        self.logs_flush_interval = int(
            os.environ.get("HUD_LOGS_QUEUE_FLUSH_INTERVAL", 5)
        )
        self.invocations_flush_interval = int(
            os.environ.get("HUD_INVOCATIONS_FLUSH_INTERVAL", 5)
        )
        self.workload_data_flush_interval = int(
            os.environ.get("HUD_WORKLOAD_DATA_FLUSH_INTERVAL", 300)
        )
        self.modules_report_interval = int(
            os.environ.get("HUD_MODULES_REPORT_INTERVAL", 60 * 60)
        )
        self.performace_report_interval = int(
            os.environ.get("HUD_PERFORMANCE_REPORT_INTERVAL", 5 * 60)
        )
        self.declarations_flush_interval = int(
            os.environ.get("HUD_DECLARATIONS_FLUSH_INTERVAL", 5)
        )
        self.api_max_retries = int(os.environ.get("HUD_API_MAX_RETRIES", 5))
        self.api_backoff_factor = float(os.environ.get("HUD_API_BACKOFF_FACTOR", 0.2))
        self.api_timeout = float(os.environ.get("HUD_API_TIMEOUT", 5))  # seconds
        self.debug_prefix = os.environ.get("HUD_DEBUG_PREFIX", DEFAULT_DEBUG_PREFIX)
        self.client_type = os.environ.get("HUD_CLIENT", DEFAULT_CLIENT)
        self.json_path = os.environ.get("HUD_JSON_PATH", DEFAULT_JSON_PATH)

        modules_to_trace_str = os.environ.get("HUD_MODULES_TO_TRACE")
        self.modules_to_trace = (
            modules_to_trace_str.split(",") if modules_to_trace_str else []
        )
        self.log_level = os.environ.get("HUD_LOG_LEVEL", "INFO")
        self.verbose_logs = os.environ.get("HUD_VERBOSE", "").lower() in ["true", "1"]
        self.debug_logs = os.environ.get("HUD_DEBUG", "").lower() in ["true", "1"]
        self.pretty_logs = os.environ.get("HUD_PRETTY_LOGS", "false").lower() in [
            "true",
            "1",
        ]
        self.aws_metadata_server = os.environ.get(
            "HUD_AWS_METADATA_SERVER", "169.254.169.254"
        )
        self.aws_metadata_timeout = float(os.environ.get("HUD_AWS_METADATA_TIMEOUT", 5))
        self.aws_local_metadata_file = os.environ.get(
            "HUD_AWS_LOCAL_METADATA_FILE", "/run/cloud-init/instance-data.json"
        )
        self.disable_exception_handler = os.environ.get(
            "HUD_DISABLE_EXCEPTION_HANDLER", ""
        ).lower() in ["true", "1"]
        self.sketch_bin_width = float(os.environ.get("HUD_SKETCH_BIN_WIDTH", 1.2))
        self.log_performance = os.environ.get(
            "HUD_LOG_PERFORMANCE", "true"
        ).lower() not in [
            "false",
            "0",
        ]


config = Config()
