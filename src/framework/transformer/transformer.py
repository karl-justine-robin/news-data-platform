from src.framework.logging.logger import logger


class Transformer:

    def transform(self, feeds):
        logger.info("Transforming feed...")

        articles = []

        for feed in feeds:

            for item in feed["items"]:

                article = {
                    "headline": item["title"],
                    "published_at": item["publish_date"],
                    "body": item["content"],
                    "source": item["source"],
                }

                articles.append(article)

        logger.info(
            f"Transformed {len(articles)} article(s)."
        )

        return articles