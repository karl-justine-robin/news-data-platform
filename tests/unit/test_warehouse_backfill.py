from unittest.mock import patch

from src.framework.warehouse.warehouse_backfill import (
    WarehouseBackfill,
)


def test_backfill_returns_zero_when_no_articles():

    backfill = WarehouseBackfill()

    with patch(
        "src.framework.warehouse.warehouse_backfill.SessionLocal"
    ) as mock_session, patch.object(
        backfill.dimension_repository,
        "save_sources",
    ) as mock_sources, patch.object(
        backfill.dimension_repository,
        "save_dates",
    ) as mock_dates, patch.object(
        backfill.fact_repository,
        "save_articles",
    ) as mock_facts:

        db = mock_session.return_value

        db.query.return_value.all.return_value = []

        result = backfill.run()

    assert result == 0

    db.close.assert_called_once()

    mock_sources.assert_not_called()
    mock_dates.assert_not_called()
    mock_facts.assert_not_called()