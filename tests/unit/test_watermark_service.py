from unittest.mock import MagicMock

from src.framework.incremental.watermark_service import (
    WatermarkService,
)


def test_get_returns_watermark_for_source():

    service = WatermarkService()

    service.repository = MagicMock()

    service.repository.load.return_value = {
        "Reuters": "2026-08-09",
        "Bloomberg": "2026-08-08",
    }

    result = service.get("Reuters")

    assert result == "2026-08-09"

    service.repository.load.assert_called_once()


def test_get_returns_none_for_unknown_source():

    service = WatermarkService()

    service.repository = MagicMock()

    service.repository.load.return_value = {
        "Reuters": "2026-08-09",
    }

    result = service.get("Bloomberg")

    assert result is None

    service.repository.load.assert_called_once()


def test_update_saves_new_watermark():

    service = WatermarkService()

    service.repository = MagicMock()

    service.repository.load.return_value = {
        "Reuters": "2026-08-09",
    }

    service.update(
        "Bloomberg",
        "2026-08-10",
    )

    service.repository.save.assert_called_once_with(
        {
            "Reuters": "2026-08-09",
            "Bloomberg": "2026-08-10",
        }
    )


def test_update_replaces_existing_watermark():

    service = WatermarkService()

    service.repository = MagicMock()

    service.repository.load.return_value = {
        "Reuters": "2026-08-08",
    }

    service.update(
        "Reuters",
        "2026-08-10",
    )

    service.repository.save.assert_called_once_with(
        {
            "Reuters": "2026-08-10",
        }
    )


def test_update_many_returns_without_saving_when_empty():

    service = WatermarkService()

    service.repository = MagicMock()

    service.update_many({})

    service.repository.load.assert_not_called()
    service.repository.save.assert_not_called()


def test_update_many_saves_multiple_watermarks():

    service = WatermarkService()

    service.repository = MagicMock()

    service.repository.load.return_value = {
        "Reuters": "2026-08-08",
    }

    service.update_many(
        {
            "Reuters": "2026-08-10",
            "Bloomberg": "2026-08-09",
        }
    )

    service.repository.save.assert_called_once_with(
        {
            "Reuters": "2026-08-10",
            "Bloomberg": "2026-08-09",
        }
    )