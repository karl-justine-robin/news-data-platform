import json

from config import SAMPLE_FEED
from src.framework.logging.logger import logger


class Collector:

    def collect(self):
        logger.info("Collecting data from BusinessDesk...")

        with open(SAMPLE_FEED, "r", encoding="utf-8") as file:
            data = json.load(file)

        logger.info(
            "Collected %d article(s) from BusinessDesk (feed date: %s).",
            len(data["items"]),
            data["feed_date"],
        )

        return data