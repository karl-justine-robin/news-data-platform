from src.framework.logging.logger import logger


class Validator:

    def validate(self, articles):
        logger.info("Validating articles...")

        validated_articles = []

        for article in articles:

            if (
                article["headline"]
                and article["published_at"]
                and article["body"]
            ):
                validated_articles.append(article)

        logger.info(f"Validated {len(validated_articles)} article(s).")

        return validated_articles