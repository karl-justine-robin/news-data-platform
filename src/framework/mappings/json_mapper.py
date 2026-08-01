class JsonMapper:

    MAPPINGS = {
        "BusinessDesk": {
            "items": "items",
            "headline": "title",
            "body": "content",
            "published_at": "publish_date",
        },
        "Reuters": {
            "items": "items",
            "headline": "title",
            "body": "content",
            "published_at": "publish_date",
        },
        "Bloomberg": {
            "items": "items",
            "headline": "title",
            "body": "content",
            "published_at": "publish_date",
        },
        "CNBC": {
            "items": "items",
            "headline": "title",
            "body": "content",
            "published_at": "publish_date",
        },
    }

    @classmethod
    def get_mapping(cls, source):
        return cls.MAPPINGS.get(source)