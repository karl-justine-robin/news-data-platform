from dataclasses import dataclass, field

from src.framework.quality.quality_metrics import (
    QualityMetrics,
)


@dataclass
class ValidationResult:

    valid_articles: list = field(default_factory=list)

    invalid_articles: list = field(default_factory=list)

    metrics: QualityMetrics = field(
        default_factory=QualityMetrics
    )