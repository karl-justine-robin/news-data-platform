import json
from pathlib import Path


class WatermarkRepository:

    def __init__(self):

        self.file = Path(
            "data/watermarks.json"
        )

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file.exists():

            self.file.write_text(
                "{}",
                encoding="utf-8",
            )

    def load(self):

        with self.file.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def save(
        self,
        watermarks,
    ):

        with self.file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                watermarks,
                file,
                indent=4,
            )