import json
from pathlib import Path


class Loader:

    def load(self, articles):
        print("Loading articles...")

        output_dir = Path("data/silver")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "articles.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                articles,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f"Saved {len(articles)} articles to {output_file.as_posix()}")