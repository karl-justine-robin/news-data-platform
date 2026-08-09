from unittest.mock import patch

from src.framework.warehouse.dimension_loader import (
    DimensionLoader,
)

from datetime import date




def test_load_sources():

    loader = DimensionLoader()

    with patch.object(
        loader.repository,
        "save_sources",
        return_value=4,
    ) as mock_save:

        inserted = loader.load_sources(
            [
                "Reuters",
                "Bloomberg",
                "CNBC",
                "BusinessDesk",
            ]
        )

    assert inserted == 4

    mock_save.assert_called_once_with(
        [
            "Reuters",
            "Bloomberg",
            "CNBC",
            "BusinessDesk",
        ]
    )


def test_load_sources_empty():

    loader = DimensionLoader()

    with patch.object(
        loader.repository,
        "save_sources",
        return_value=0,
    ):

        inserted = loader.load_sources([])

    assert inserted == 0


def test_load_categories():

    loader = DimensionLoader()

    with patch.object(
        loader.repository,
        "save_categories",
        return_value=3,
    ) as mock_save:

        inserted = loader.load_categories(
            [
                "Business",
                "Technology",
                "Sports",
            ]
        )

    assert inserted == 3

    mock_save.assert_called_once_with(
        [
            "Business",
            "Technology",
            "Sports",
        ]
    )


def test_load_categories_empty():

    loader = DimensionLoader()

    with patch.object(
        loader.repository,
        "save_categories",
        return_value=0,
    ):

        inserted = loader.load_categories([])

    assert inserted == 0


def test_load_dates():

    loader = DimensionLoader()

    dates = [
        date(2026, 8, 9),
        date(2026, 8, 10),
    ]

    with patch.object(
        loader.repository,
        "save_dates",
        return_value=2,
    ) as mock_save:

        inserted = loader.load_dates(
            dates
        )

    assert inserted == 2

    mock_save.assert_called_once()

    saved_dates = mock_save.call_args.args[0]

    assert saved_dates == {
        date(2026, 8, 9),
        date(2026, 8, 10),
    }


def test_load_dates_empty():

    loader = DimensionLoader()

    with patch.object(
        loader.repository,
        "save_dates",
        return_value=0,
    ):

        inserted = loader.load_dates([])

    assert inserted == 0