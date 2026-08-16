from unittest.mock import MagicMock

from src.framework.pipeline import Pipeline
import src.framework.pipeline as pipeline_module
from src.framework.incremental.incremental_result import (
    IncrementalResult,
)


def test_full_pipeline_execution(monkeypatch):

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_INCREMENTAL",
        True,
    )

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_BRONZE",
        True,
    )

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_SILVER",
        True,
    )

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_GOLD",
        True,
    )

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_WAREHOUSE",
        True,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    feeds = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

    articles = [
        {
            "headline": "Test Article 1",
            "published_at": "2026-08-09",
            "body": "Test body 1",
            "source": "Reuters",
        },
        {
            "headline": "Test Article 2",
            "published_at": "2026-08-09",
            "body": "Test body 2",
            "source": "Reuters",
        },
    ]

    valid_articles = articles

    pipeline.collector.collect.return_value = feeds

    pipeline.preprocessor.preprocess.return_value = feeds

    pipeline.transformer.transform.return_value = articles

    pipeline.incremental_filter.filter.return_value = (
        IncrementalResult(
            new_articles=articles,
            latest_watermarks={
                "Reuters": "2026-08-09"
            },
        )
    )

    pipeline.validator.validate.return_value = (
        MagicMock(
            valid_articles=valid_articles,
            invalid_articles=[],
            metrics=MagicMock(),
        )
    )

    pipeline.bronze_writer.write.return_value = (
        "2026-08-09T00:00:00"
    )

    pipeline.silver_writer.write.return_value = (
        "silver/test.json"
    )

    pipeline.gold_writer.write.return_value = [
        "gold/articles.json"
    ]

    pipeline.tracker.start.return_value = 1

    pipeline.run()

    pipeline.collector.collect.assert_called_once()

    pipeline.schema_validator.validate.assert_called_once_with(
        feeds
    )

    pipeline.preprocessor.preprocess.assert_called_once_with(
        feeds
    )

    pipeline.transformer.transform.assert_called_once_with(
        feeds
    )

    pipeline.incremental_filter.filter.assert_called_once_with(
        articles
    )

    pipeline.validator.validate.assert_called_once_with(
        articles
    )

    pipeline.dimension_loader.load_sources.assert_called_once_with(
        {"Reuters"}
    )

    pipeline.dimension_loader.load_dates.assert_called_once_with(
        {"2026-08-09"}
    )

    pipeline.bronze_writer.write.assert_called_once_with(
        feeds
    )

    pipeline.silver_writer.write.assert_called_once()

    pipeline.gold_writer.write.assert_called_once()

    pipeline.loader.load.assert_called_once_with(
        valid_articles
    )

    pipeline.fact_loader.load_articles.assert_called_once_with(
        valid_articles
    )

    pipeline.watermark_service.update_many.assert_called_once_with(
        {
            "Reuters": "2026-08-09"
        }
    )

    pipeline.quality_service.generate_report.assert_called_once()

    pipeline.tracker.start.assert_called_once()

    pipeline.tracker.finish.assert_called_once_with(
        run_id=1,
        records_processed=2,
        success=True,
        error_message=None,
    )