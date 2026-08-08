from src.framework.incremental.watermark_repository import (
    WatermarkRepository,
)


class WatermarkService:

    def __init__(self):

        self.repository = WatermarkRepository()

    def get(
        self,
        source,
    ):

        watermarks = self.repository.load()

        return watermarks.get(source)

    def update(
        self,
        source,
        watermark,
    ):

        watermarks = self.repository.load()

        watermarks[source] = watermark

        self.repository.save(
            watermarks
        )

    def update_many(
        self,
        latest_watermarks,
    ):

        if not latest_watermarks:
            return

        watermarks = self.repository.load()

        watermarks.update(
            latest_watermarks
        )

        self.repository.save(
            watermarks
        )