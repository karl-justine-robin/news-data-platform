from src.framework.error.exceptions import PipelineException
from src.framework.logging.logger import logger


class SchemaValidator:

    EXPECTED_SCHEMA = {
        "BusinessDesk": {
            "container": "items",
            "fields": {
                "title",
                "content",
                "publish_date",
            },
        },
        "Reuters": {
            "container": "items",
            "fields": {
                "title",
                "content",
                "publish_date",
            },
        },
        "Bloomberg": {
            "container": "items",
            "fields": {
                "title",
                "content",
                "publish_date",
            },
        },
        "CNBC": {
            "container": "items",
            "fields": {
                "title",
                "content",
                "publish_date",
            },
        },
    }

    INTERNAL_FIELDS = {
        "source",
    }

    def validate(self, feeds):

        logger.info("Validating vendor schemas...")

        feeds_checked = 0
        passed = 0
        errors = 0

        failed_vendors = []

        for feed in feeds:

            feeds_checked += 1

            source = feed["source"]

            if source not in self.EXPECTED_SCHEMA:

                logger.error(
                    "No schema registered for '%s'.",
                    source,
                )

                errors += 1
                failed_vendors.append(source)
                continue

            expected = self.EXPECTED_SCHEMA[source]

            container = expected["container"]

            if container not in feed:

                logger.error(
                    "%s: Missing top-level container '%s'.",
                    source,
                    container,
                )

                errors += 1
                failed_vendors.append(source)
                continue

            if not feed[container]:

                logger.warning(
                    "%s: Feed contains no articles.",
                    source,
                )

                passed += 1
                continue

            actual_fields = set(
                feed[container][0].keys()
            )

            actual_fields -= self.INTERNAL_FIELDS

            expected_fields = expected["fields"]

            missing = expected_fields - actual_fields
            additional = actual_fields - expected_fields

            if additional:

                logger.info(
                    "%s: Additional unmapped fields detected: %s",
                    source,
                    sorted(additional),
                )

            if missing:

                logger.error(
                    "Schema mismatch detected for %s",
                    source,
                )

                logger.error(
                    "Missing required fields: %s",
                    sorted(missing),
                )

                errors += 1
                failed_vendors.append(source)

            else:
                passed += 1

        logger.info("")
        logger.info("Schema Validation Summary")
        logger.info("-------------------------")
        logger.info("Feeds Checked : %d", feeds_checked)
        logger.info("Passed        : %d", passed)
        logger.info("Errors        : %d", errors)

        if failed_vendors:

            logger.error(
                "Failed Vendors: %s",
                ", ".join(failed_vendors),
            )

            raise PipelineException(
                "Vendor schema validation failed."
            )

        logger.info("Schema validation passed.")