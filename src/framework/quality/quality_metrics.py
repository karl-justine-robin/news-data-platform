from dataclasses import dataclass


@dataclass
class QualityMetrics:
    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0

    missing_headline: int = 0
    missing_body: int = 0
    missing_source: int = 0
    invalid_date: int = 0

    @property
    def quality_score(self) -> float:
        if self.total_records == 0:
            return 100.0

        return (
            self.valid_records / self.total_records
        ) * 100