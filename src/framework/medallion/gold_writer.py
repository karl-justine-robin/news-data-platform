import json
from collections import Counter
from pathlib import Path


class GoldWriter:

    def __init__(self):

        self.base_path = Path("data/gold")

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        articles,
        validation_metrics,
        timestamp,
    ):

        generated_files = []

        # -----------------------------------------
        # Dataset 1 - Articles by Source
        # -----------------------------------------

        source_counts = Counter()

        for article in articles:
            source_counts[
                article["source"]
            ] += 1

        source_file = (
            self.base_path
            / f"articles_by_source_{timestamp}.json"
        )

        with source_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                dict(source_counts),
                file,
                indent=4,
                ensure_ascii=False,
            )

        generated_files.append(source_file)

        # -----------------------------------------
        # Dataset 2 - Articles by Date
        # -----------------------------------------

        date_counts = Counter()

        for article in articles:
            date_counts[
                str(article["published_at"])
            ] += 1

        date_file = (
            self.base_path
            / f"articles_by_date_{timestamp}.json"
        )

        with date_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                dict(date_counts),
                file,
                indent=4,
                ensure_ascii=False,
            )

        generated_files.append(date_file)

        # -----------------------------------------
        # Dataset 3 - Quality Summary
        # -----------------------------------------

        quality_summary = {
            "total_records": validation_metrics.total_records,
            "valid_records": validation_metrics.valid_records,
            "invalid_records": validation_metrics.invalid_records,
            "missing_headline": validation_metrics.missing_headline,
            "missing_body": validation_metrics.missing_body,
            "invalid_date": validation_metrics.invalid_date,
        }

        quality_file = (
            self.base_path
            / f"quality_summary_{timestamp}.json"
        )

        with quality_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                quality_summary,
                file,
                indent=4,
                ensure_ascii=False,
            )

        generated_files.append(quality_file)

        return generated_files