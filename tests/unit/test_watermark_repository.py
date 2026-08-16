from pathlib import Path

from src.framework.incremental.watermark_repository import (
    WatermarkRepository,
)


def test_repository_creates_watermark_file_when_missing():

    file = Path("data/watermarks.json")

    original_contents = None

    if file.exists():
        original_contents = file.read_text(
            encoding="utf-8"
        )
        file.unlink()

    try:

        repository = WatermarkRepository()

        assert repository.file.exists()
        assert repository.load() == {}

    finally:

        if file.exists():
            file.unlink()

        if original_contents is not None:
            file.write_text(
                original_contents,
                encoding="utf-8",
            )