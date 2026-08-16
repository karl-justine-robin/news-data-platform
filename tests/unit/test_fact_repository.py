from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from src.framework.repository.fact_repository import (
    FactRepository,
)


def create_mock_db():
    db = MagicMock()

    source = MagicMock()
    source.source_key = 1

    date_dimension = MagicMock()
    date_dimension.date_key = 20260809

    db.scalar.side_effect = [
        source,
        date_dimension,
        None,
    ]

    return db


def test_save_articles_inserts_new_article():

    db = create_mock_db()

    repository = FactRepository()

    articles = [
        {
            "source": "Reuters",
            "headline": "Test Article",
            "published_at": "2026-08-09",
        }
    ]

    with patch(
        "src.framework.repository.fact_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_articles(
            articles
        )

    assert inserted == 1

    db.add.assert_called_once()

    fact = db.add.call_args.args[0]

    assert fact.date_key == 20260809
    assert fact.source_key == 1
    assert fact.headline == "Test Article"
    assert fact.published_at == date(2026, 8, 9)

    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_articles_skips_missing_published_at():

    db = MagicMock()

    repository = FactRepository()

    articles = [
        {
            "source": "Reuters",
            "headline": "Missing Date",
            "published_at": None,
        }
    ]

    with patch(
        "src.framework.repository.fact_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_articles(
            articles
        )

    assert inserted == 0

    db.scalar.assert_not_called()
    db.add.assert_not_called()
    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_articles_skips_unknown_source():

    db = MagicMock()

    db.scalar.return_value = None

    repository = FactRepository()

    articles = [
        {
            "source": "Unknown",
            "headline": "Test Article",
            "published_at": "2026-08-09",
        }
    ]

    with patch(
        "src.framework.repository.fact_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_articles(
            articles
        )

    assert inserted == 0

    db.add.assert_not_called()
    db.commit.assert_called_once()


def test_save_articles_skips_missing_date_dimension():

    db = MagicMock()

    source = MagicMock()
    source.source_key = 1

    db.scalar.side_effect = [
        source,
        None,
    ]

    repository = FactRepository()

    articles = [
        {
            "source": "Reuters",
            "headline": "Test Article",
            "published_at": "2026-08-09",
        }
    ]

    with patch(
        "src.framework.repository.fact_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_articles(
            articles
        )

    assert inserted == 0

    db.add.assert_not_called()
    db.commit.assert_called_once()


def test_save_articles_skips_existing_fact():

    db = MagicMock()

    source = MagicMock()
    source.source_key = 1

    date_dimension = MagicMock()
    date_dimension.date_key = 20260809

    existing_fact = MagicMock()

    db.scalar.side_effect = [
        source,
        date_dimension,
        existing_fact,
    ]

    repository = FactRepository()

    articles = [
        {
            "source": "Reuters",
            "headline": "Existing Article",
            "published_at": "2026-08-09",
        }
    ]

    with patch(
        "src.framework.repository.fact_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_articles(
            articles
        )

    assert inserted == 0

    db.add.assert_not_called()
    db.commit.assert_called_once()


def test_save_articles_accepts_date_object():

    db = MagicMock()

    source = MagicMock()
    source.source_key = 1

    date_dimension = MagicMock()
    date_dimension.date_key = 20260809

    db.scalar.side_effect = [
        source,
        date_dimension,
        None,
    ]

    repository = FactRepository()

    articles = [
        {
            "source": "Reuters",
            "headline": "Date Object Article",
            "published_at": date(2026, 8, 9),
        }
    ]

    with patch(
        "src.framework.repository.fact_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_articles(
            articles
        )

    assert inserted == 1

    db.add.assert_called_once()


def test_save_articles_rolls_back_on_error():

    db = MagicMock()

    db.scalar.side_effect = RuntimeError(
        "Database failure"
    )

    repository = FactRepository()

    articles = [
        {
            "source": "Reuters",
            "headline": "Test Article",
            "published_at": "2026-08-09",
        }
    ]

    with patch(
        "src.framework.repository.fact_repository.SessionLocal",
        return_value=db,
    ):

        with pytest.raises(RuntimeError):

            repository.save_articles(
                articles
            )

    db.rollback.assert_called_once()
    db.close.assert_called_once()