from src.framework.quality.quality_metrics import (
    QualityMetrics,
)


class QualityReport:

    def generate(
        self,
        metrics: QualityMetrics,
    ) -> str:

        return f"""
=================================================
              DATA QUALITY REPORT
=================================================

Total Records      : {metrics.total_records}
Valid Records      : {metrics.valid_records}
Invalid Records    : {metrics.invalid_records}

Quality Score      : {metrics.quality_score:.2f}%

Validation Failures

Missing Headline   : {metrics.missing_headline}
Missing Body       : {metrics.missing_body}
Missing Source     : {metrics.missing_source}
Invalid Date       : {metrics.invalid_date}

=================================================
"""