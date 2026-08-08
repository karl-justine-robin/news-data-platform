import json
from pathlib import Path


class SilverWriter:

    def __init__(self):

        self.base_path = Path("data/silver")

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        articles,
        timestamp,
    ):

        output_file = (
            self.base_path /
            f"articles_{timestamp}.json"
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                articles,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output_file