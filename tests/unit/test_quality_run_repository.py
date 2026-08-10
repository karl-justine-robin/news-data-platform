from unittest.mock import MagicMock, patch

from src.framework.quality.quality_metrics import QualityMetrics
from src.framework.repository.quality_run_repository import (
    QualityRunRepository,
)


def test_save():

    repository = QualityRunRepository()

    metrics = QualityMetrics(
        total_records=30,
        valid_records=28,
        invalid_records=2,
        missing_headline=1,
        missing_body=1,
        missing_source=0,
        invalid_date=0,
    )

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (123,)

    mock_connection = MagicMock()

    mock_connection.__enter__.return_value = (
        mock_connection
    )

    mock_connection.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    with patch(
        "src.framework.repository.quality_run_repository.psycopg.connect",
        return_value=mock_connection,
    ) as mock_connect:

        result = repository.save(metrics)

    assert result == 123

    mock_connect.assert_called_once()

    mock_cursor.execute.assert_called_once()

    mock_connection.commit.assert_called_once()


def test_get_latest():

    repository = QualityRunRepository()

    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = (
        30,
        30,
        0,
        0,
        0,
        0,
        0,
        100.0,
    )

    mock_connection = MagicMock()

    mock_connection.__enter__.return_value = (
        mock_connection
    )

    mock_connection.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    with patch(
        "src.framework.repository.quality_run_repository.psycopg.connect",
        return_value=mock_connection,
    ):

        result = repository.get_latest()

    assert result == {
        "total_records": 30,
        "valid_records": 30,
        "invalid_records": 0,
        "missing_headline": 0,
        "missing_body": 0,
        "missing_source": 0,
        "invalid_date": 0,
        "quality_score": 100.0,
    }

    mock_cursor.execute.assert_called_once()


def test_get_latest_returns_none():

    repository = QualityRunRepository()

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None

    mock_connection = MagicMock()

    mock_connection.__enter__.return_value = (
        mock_connection
    )

    mock_connection.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    with patch(
        "src.framework.repository.quality_run_repository.psycopg.connect",
        return_value=mock_connection,
    ):

        result = repository.get_latest()

    assert result is None