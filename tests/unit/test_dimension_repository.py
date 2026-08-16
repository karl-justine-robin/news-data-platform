from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from src.framework.repository.dimension_repository import (
    DimensionRepository,
)


def test_save_sources_inserts_new_sources():

    repository = DimensionRepository()

    db = MagicMock()

    existing_source = MagicMock()
    existing_source.source_name = "Reuters"

    db.scalars.return_value.all.return_value = [
        existing_source
    ]

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_sources(
            [
                "Reuters",
                "Bloomberg",
                "CNBC",
            ]
        )

    assert inserted == 2

    assert db.add.call_count == 2

    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_sources_skips_existing_sources():

    repository = DimensionRepository()

    db = MagicMock()

    existing_source = MagicMock()
    existing_source.source_name = "Reuters"

    db.scalars.return_value.all.return_value = [
        existing_source
    ]

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_sources(
            ["Reuters"]
        )

    assert inserted == 0

    db.add.assert_not_called()
    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_sources_rolls_back_on_error():

    repository = DimensionRepository()

    db = MagicMock()

    db.scalars.side_effect = RuntimeError(
        "Database failure"
    )

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        with pytest.raises(RuntimeError):

            repository.save_sources(
                ["Reuters"]
            )

    db.rollback.assert_called_once()
    db.close.assert_called_once()


def test_save_categories_inserts_new_categories():

    repository = DimensionRepository()

    db = MagicMock()

    existing_category = MagicMock()
    existing_category.category_name = "Business"

    db.scalars.return_value.all.return_value = [
        existing_category
    ]

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_categories(
            [
                "Business",
                "Technology",
                "Sports",
            ]
        )

    assert inserted == 2

    assert db.add.call_count == 2

    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_categories_skips_existing_categories():

    repository = DimensionRepository()

    db = MagicMock()

    existing_category = MagicMock()
    existing_category.category_name = "Business"

    db.scalars.return_value.all.return_value = [
        existing_category
    ]

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_categories(
            ["Business"]
        )

    assert inserted == 0

    db.add.assert_not_called()
    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_categories_rolls_back_on_error():

    repository = DimensionRepository()

    db = MagicMock()

    db.scalars.side_effect = RuntimeError(
        "Database failure"
    )

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        with pytest.raises(RuntimeError):

            repository.save_categories(
                ["Business"]
            )

    db.rollback.assert_called_once()
    db.close.assert_called_once()


def test_save_dates_inserts_new_dates():

    repository = DimensionRepository()

    db = MagicMock()

    existing_date = MagicMock()
    existing_date.full_date = date(
        2026,
        8,
        8,
    )

    db.scalars.return_value.all.return_value = [
        existing_date
    ]

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_dates(
            [
                date(2026, 8, 8),
                date(2026, 8, 9),
                date(2026, 8, 10),
            ]
        )

    assert inserted == 2

    assert db.add.call_count == 2

    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_dates_skips_existing_dates():

    repository = DimensionRepository()

    db = MagicMock()

    existing_date = MagicMock()
    existing_date.full_date = date(
        2026,
        8,
        9,
    )

    db.scalars.return_value.all.return_value = [
        existing_date
    ]

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_dates(
            [
                date(2026, 8, 9)
            ]
        )

    assert inserted == 0

    db.add.assert_not_called()
    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_dates_creates_date_dimension_fields():

    repository = DimensionRepository()

    db = MagicMock()

    db.scalars.return_value.all.return_value = []

    current_date = date(
        2026,
        8,
        16,
    )

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        inserted = repository.save_dates(
            [current_date]
        )

    assert inserted == 1

    added_date = db.add.call_args.args[0]

    assert added_date.date_key == 20260816
    assert added_date.full_date == current_date
    assert added_date.year == 2026
    assert added_date.month == 8
    assert added_date.month_name == "August"
    assert added_date.day == 16
    assert added_date.day_of_week == "Sunday"

    db.commit.assert_called_once()
    db.close.assert_called_once()


def test_save_dates_rolls_back_on_error():

    repository = DimensionRepository()

    db = MagicMock()

    db.scalars.side_effect = RuntimeError(
        "Database failure"
    )

    with patch(
        "src.framework.repository.dimension_repository.SessionLocal",
        return_value=db,
    ):

        with pytest.raises(RuntimeError):

            repository.save_dates(
                [date(2026, 8, 16)]
            )

    db.rollback.assert_called_once()
    db.close.assert_called_once()