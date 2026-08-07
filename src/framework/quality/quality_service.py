from src.framework.quality.quality_report import (
    QualityReport,
)
from src.framework.quality.quality_metrics import (
    QualityMetrics,
)


class QualityService:

    def __init__(self):

        self.report = QualityReport()

    def generate_report(
        self,
        metrics: QualityMetrics,
    ) -> str:

        return self.report.generate(
            metrics,
        )