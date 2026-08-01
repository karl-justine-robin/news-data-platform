import json

from config import SAMPLE_DATA_DIR

from src.framework.error.exceptions import CollectorException
from src.framework.error.retry import retry
from src.framework.logging.logger import logger


class Collector:

    def collect(self):
        logger.info("Starting data collection...")

        try:
            return retry(
                self._collect,
                max_attempts=3,
                delay=2,
                exceptions=(
                    FileNotFoundError,
                    json.JSONDecodeError,
                    OSError,
                ),
            )

        except Exception as error:
            raise CollectorException(
                f"Data collection failed: {error}"
            ) from error

    def _collect(self):
        feeds = []

        for file in sorted(SAMPLE_DATA_DIR.glob("*.json")):

            logger.info(
                f"Collecting data from {file.stem}..."
            )

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as stream:

                feed = json.load(stream)

            source = feed.get(
                "source",
                file.stem.capitalize(),
            )

            logger.info(
                "Collected %d article(s) from %s (feed date: %s).",
                len(feed["items"]),
                source,
                feed["feed_date"],
            )

            feeds.append(feed)

        total_articles = sum(
            len(feed["items"])
            for feed in feeds
        )

        logger.info(
            "Collected %d total article(s) from %d feed(s).",
            total_articles,
            len(feeds),
        )

        return feeds