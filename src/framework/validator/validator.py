from src.framework.logging.logger import logger


class Validator:

    def validate(self, articles):
        logger.info("Validating articles...")

        valid_articles = []
        rejected_count = 0

        for article in articles:

            reason = None

            if not article.get("headline"):
                reason = "Missing headline"

            elif not article.get("body"):
                reason = "Missing body"

            elif not article.get("published_at"):
                reason = "Missing published_at"

            if reason:

                rejected_count += 1

                logger.warning(
                    "Rejected article | Source: %s | Headline: %s | Reason: %s",
                    article.get("source", "Unknown"),
                    article.get("headline", "<missing>"),
                    reason,
                )

                continue

            valid_articles.append(article)

        logger.info(
            "Validated %d article(s).",
            len(valid_articles),
        )

        logger.info(
            "Rejected %d article(s).",
            rejected_count,
        )

        return valid_articles