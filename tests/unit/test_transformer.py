from unittest.mock import patch

from src.framework.transformer.transformer import (
    Transformer,
)


def test_transform_valid_feed():

    transformer = Transformer()

    feeds = [
        {
            "source": "Reuters",
            "items": [
                {
                    "title": "Breaking News",
                    "content": "This is the body.",
                    "publish_date": "2026-08-02",
                    "category": "Business",
                }
            ],
        }
    ]

    articles = transformer.transform(feeds)

    assert len(articles) == 1

    assert articles[0]["headline"] == "Breaking News"
    assert articles[0]["body"] == "This is the body."
    assert articles[0]["published_at"] == "2026-08-02"
    assert articles[0]["source"] == "Reuters"


def test_transform_multiple_feeds():

    transformer = Transformer()

    feeds = [
        {
            "source": "Reuters",
            "items": [
                {
                    "title": "Reuters News",
                    "content": "Body 1",
                    "publish_date": "2026-08-02",
                }
            ],
        },
        {
            "source": "Bloomberg",
            "items": [
                {
                    "title": "Bloomberg News",
                    "content": "Body 2",
                    "publish_date": "2026-08-02",
                }
            ],
        },
    ]

    articles = transformer.transform(feeds)

    assert len(articles) == 2
    assert articles[0]["source"] == "Reuters"
    assert articles[1]["source"] == "Bloomberg"

def test_transform_empty_feed():

    transformer = Transformer()

    feeds = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

    articles = transformer.transform(feeds)

    assert articles == []



def test_transform_missing_title():

    transformer = Transformer()

    feeds = [
        {
            "source": "Reuters",
            "items": [
                {
                    "content": "Body",
                    "publish_date": "2026-08-02",
                }
            ],
        }
    ]

    articles = transformer.transform(feeds)

    assert len(articles) == 1
    assert articles[0]["headline"] is None


def test_transform_preserves_source():

    transformer = Transformer()

    feeds = [
        {
            "source": "CNBC",
            "items": [
                {
                    "title": "Market News",
                    "content": "Stocks up",
                    "publish_date": "2026-08-02",
                }
            ],
        }
    ]

    articles = transformer.transform(feeds)

    assert articles[0]["source"] == "CNBC"


def test_unknown_source_is_skipped():

    transformer = Transformer()

    with patch(
        "src.framework.transformer.transformer.JsonMapper.get_mapping",
        return_value=None,
    ):

        result = transformer.transform(
            [
                {
                    "source": "UnknownSource",
                    "items": [
                        {
                            "title": "Test Article",
                        }
                    ],
                }
            ]
        )

    assert result == []