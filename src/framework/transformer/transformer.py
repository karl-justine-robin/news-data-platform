from src.framework.logging.logger import logger
from src.framework.mappings.json_mapper import JsonMapper


class Transformer:

    def transform(self, feeds):
        logger.info("Transforming feed...")

        articles = []

        for feed in feeds:

            source = feed.get("source", "Unknown")

            mapping = JsonMapper.get_mapping(source)

            if mapping is None:
                logger.warning(
                    f"No mapping found for source '{source}'. Skipping feed."
                )
                continue

            items = feed.get(mapping["items"], [])

            for item in items:

                article = {
                    "headline": item.get(mapping["headline"]),
                    "published_at": item.get(mapping["published_at"]),
                    "body": item.get(mapping["body"]),
                    "source": source,
                }

                articles.append(article)

        logger.info(
            f"Transformed {len(articles)} article(s)."
        )

        return articles