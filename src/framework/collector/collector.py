import json
from pathlib import Path

from config import SAMPLE_DATA_DIR
from src.framework.logging.logger import logger


class Collector:

    def collect(self):
        combined_feed = {
            "feed_date": None,
            "timezone": None,
            "items": [],
        }

        json_files = sorted(Path(SAMPLE_DATA_DIR).glob("*.json"))

        for json_file in json_files:
            logger.info("Collecting data from %s...", json_file.stem)

            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            logger.info(
                "Collected %d article(s) from %s (feed date: %s).",
                len(data["items"]),
                data.get("vendor", json_file.stem),
                data["feed_date"],
            )

            combined_feed["items"].extend(data["items"])

            if combined_feed["feed_date"] is None:
                combined_feed["feed_date"] = data["feed_date"]

            if combined_feed["timezone"] is None:
                combined_feed["timezone"] = data["timezone"]

        logger.info(
            "Collected %d total article(s) from %d feed(s).",
            len(combined_feed["items"]),
            len(json_files),
        )

        return combined_feed