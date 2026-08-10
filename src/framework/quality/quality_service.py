from src.framework.quality.quality_report import (
    QualityReport,
)
from src.framework.quality.quality_metrics import (
    QualityMetrics,
)
from src.framework.repository.quality_run_repository import (
    QualityRunRepository,
)


class QualityService:

    def __init__(self):

        self.report = QualityReport()
        self.repository = QualityRunRepository()
        self.latest_metrics = None

    def generate_report(
        self,
        metrics: QualityMetrics,
    ) -> str:

        self.latest_metrics = metrics

        self.repository.save(
            metrics
        )

        return self.report.generate(
            metrics,
        )

    def get_latest_metrics(
        self,
    ) -> QualityMetrics | None:

        return self.latest_metrics