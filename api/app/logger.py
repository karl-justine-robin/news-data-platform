from src.framework.logging.logging_config import configure_logger

logger = configure_logger(
    name="api",
    logfile="api.log",
)