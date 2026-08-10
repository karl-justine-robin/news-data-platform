from unittest.mock import MagicMock

from src.framework.quality.quality_metrics import (
    QualityMetrics,
)
from src.framework.quality.quality_service import (
    QualityService,
)


def test_generate_report():

    service = QualityService()

    service.repository = MagicMock()

    metrics = QualityMetrics(
        total_records=30,
        valid_records=28,
        invalid_records=2,
        missing_headline=1,
        missing_body=1,
        missing_source=0,
        invalid_date=0,
    )

    result = service.generate_report(
        metrics
    )

    assert "DATA QUALITY REPORT" in result

    assert service.latest_metrics is metrics

    service.repository.save.assert_called_once_with(
        metrics
    )


def test_get_latest_metrics():

    service = QualityService()

    metrics = QualityMetrics(
        total_records=30,
        valid_records=30,
        invalid_records=0,
    )

    service.latest_metrics = metrics

    result = service.get_latest_metrics()

    assert result is metrics