from datetime import datetime


class Validator:

    def validate(self, articles):
        print("Validating articles...")

        validated_articles = []

        for article in articles:

            if not article.get("headline"):
                raise ValueError("Missing required field: headline")

            if not article.get("published_at"):
                raise ValueError("Missing required field: published_at")

            if not article.get("body"):
                raise ValueError("Missing required field: body")

            try:
                datetime.strptime(article["published_at"], "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    f"Invalid date format: {article['published_at']}"
                )

            validated_articles.append(article)

        return validated_articles