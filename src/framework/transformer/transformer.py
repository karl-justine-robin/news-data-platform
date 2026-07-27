import json


class Transformer:

    def transform(self, data):
        print("Transforming feed...")

        with open(
            "src/framework/mappings/businessdesk.json",
            "r",
            encoding="utf-8"
        ) as file:
            config = json.load(file)

        mappings = config["mappings"]

        articles = []

        for item in data["items"]:
            article = {}

            for target_field, source_field in mappings.items():
                article[target_field] = item.get(source_field)

            articles.append(article)

        return articles