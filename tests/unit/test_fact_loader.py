from unittest.mock import patch

from src.framework.warehouse.fact_loader import FactLoader


def test_load_articles():

    loader = FactLoader()

    articles = [
        {
            "headline": "Reuters News",
            "published_at": "2026-08-09",
            "body": "Body",
            "source": "Reuters",
        },
        {
            "headline": "Bloomberg News",
            "published_at": "2026-08-09",
            "body": "Body",
            "source": "Bloomberg",
        },
    ]

    with patch.object(
        loader.repository,
        "save_articles",
        return_value=2,
    ) as mock_save:

        inserted = loader.load_articles(
            articles
        )

    assert inserted == 2

    mock_save.assert_called_once_with(
        articles
    )


def test_load_articles_empty():

    loader = FactLoader()

    with patch.object(
        loader.repository,
        "save_articles",
        return_value=0,
    ):

        inserted = loader.load_articles([])

    assert inserted == 0