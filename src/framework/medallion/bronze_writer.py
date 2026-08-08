import json
from datetime import UTC, datetime
from pathlib import Path


class BronzeWriter:

    def __init__(self):

        self.base_path = Path("data/bronze")

    def write(
        self,
        feeds,
    ):

        timestamp = datetime.now(UTC).strftime(
            "%Y%m%d_%H%M%S"
        )

        for feed in feeds:

            source = feed["source"].lower()

            folder = self.base_path / source

            folder.mkdir(
                parents=True,
                exist_ok=True,
            )

            output_file = (
                folder /
                f"{source}_{timestamp}.json"
            )

            with output_file.open(
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    feed,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        return timestamp