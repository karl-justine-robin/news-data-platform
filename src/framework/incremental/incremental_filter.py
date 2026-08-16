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

        seen_articles = set()

        for article in articles:

            source = article["source"]

            published_at = str(
                article["published_at"]
            )

            canonical_url = article.get(
                "canonical_url"
            )

            if canonical_url:
                article_key = (
                    source,
                    canonical_url,
                )

                if article_key in seen_articles:
                    continue

                seen_articles.add(article_key)

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