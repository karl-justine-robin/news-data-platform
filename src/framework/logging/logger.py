import logging
from pathlib import Path

from config import LOG_LEVEL

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("news_pipeline")

logger.setLevel(
    getattr(logging, LOG_LEVEL.upper(), logging.INFO)
)

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_DIR / "pipeline.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)