from src.framework.logging.logger import logger
from src.framework.validator.validation_result import (
    ValidationResult,
)


class Validator:

    def validate(self, articles):

        logger.info("Validating articles...")

        result = ValidationResult()

        for article in articles:

            reason = None

            result.metrics.total_records += 1

            if not article.get("headline"):
                reason = "Missing headline"
                result.metrics.missing_headline += 1

            elif not article.get("body"):
                reason = "Missing body"
                result.metrics.missing_body += 1

            elif not article.get("published_at"):
                reason = "Missing published_at"
                result.metrics.invalid_date += 1

            if reason:

                result.invalid_articles.append(article)
                result.metrics.invalid_records += 1

                logger.warning(
                    "Rejected article | Source: %s | Headline: %s | Reason: %s",
                    article.get("source", "Unknown"),
                    article.get("headline", "<missing>"),
                    reason,
                )

                continue

            result.valid_articles.append(article)
            result.metrics.valid_records += 1

        logger.info(
            "Validated %d article(s).",
            result.metrics.valid_records,
        )

        logger.info(
            "Rejected %d article(s).",
            result.metrics.invalid_records,
        )

        return result