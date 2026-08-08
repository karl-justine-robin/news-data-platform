from datetime import datetime

from src.framework.incremental.incremental_result import (
    IncrementalResult,
)
from src.framework.incremental.watermark_service import (
    WatermarkService,
)


class IncrementalFilter:

    def __init__(self):

        self.watermark_service = (
            WatermarkService()
        )

    def filter(
        self,
        articles,
    ):

        new_articles = []

        latest_watermarks = {}

        for article in articles:

            source = article["source"]

            published_at = str(
                article["published_at"]
            )

            article_date = datetime.fromisoformat(
                published_at
            )

            last_watermark = (
                self.watermark_service.get(
                    source
                )
            )

            if last_watermark is None:

                watermark_date = datetime.min

            else:

                watermark_date = (
                    datetime.fromisoformat(
                        str(last_watermark)
                    )
                )

            if article_date > watermark_date:

                new_articles.append(
                    article
                )

                current = latest_watermarks.get(
                    source
                )

                if (
                    current is None
                    or article_date
                    > datetime.fromisoformat(
                        current
                    )
                ):

                    latest_watermarks[source] = (
                        published_at
                    )

        return IncrementalResult(
            new_articles=new_articles,
            latest_watermarks=latest_watermarks,
        )