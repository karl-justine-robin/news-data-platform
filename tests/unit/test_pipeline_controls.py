from unittest.mock import MagicMock

import src.framework.pipeline as pipeline_module
from src.framework.pipeline import Pipeline


def test_incremental_enabled_calls_filter(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_INCREMENTAL",
        True,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.return_value = []

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.incremental_filter.filter.assert_called_once_with(
        []
    )


def test_incremental_disabled_bypasses_filter(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_INCREMENTAL",
        False,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    articles = [
        {
            "headline": "Test article",
            "published_at": "2026-08-11",
            "body": "Test body",
            "source": "Reuters",
        }
    ]

    pipeline.collector.collect.return_value = []

    pipeline.transformer.transform.return_value = articles

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.incremental_filter.filter.assert_not_called()

    pipeline.validator.validate.assert_called_once_with(
        articles
    )


def test_incremental_disabled_does_not_update_watermarks(
    monkeypatch,
):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_INCREMENTAL",
        False,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.return_value = []

    pipeline.transformer.transform.return_value = []

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.incremental_filter.filter.assert_not_called()

    pipeline.watermark_service.update_many.assert_not_called()


def test_bronze_enabled_calls_writer(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_BRONZE",
        True,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    feed = []

    pipeline.collector.collect.return_value = feed

    pipeline.bronze_writer.write.return_value = (
        "2026-08-12T00:00:00"
    )

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.bronze_writer.write.assert_called_once_with(
        feed
    )


def test_bronze_disabled_skips_writer(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_BRONZE",
        False,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.return_value = []

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.bronze_writer.write.assert_not_called()


def test_silver_enabled_calls_writer(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_SILVER",
        True,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    feed = []

    pipeline.collector.collect.return_value = feed

    pipeline.bronze_writer.write.return_value = (
        "2026-08-12T00:00:00"
    )

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.silver_writer.write.return_value = (
        "data/silver/test.json"
    )

    pipeline.run()

    pipeline.silver_writer.write.assert_called_once_with(
        [],
        "2026-08-12T00:00:00",
    )


def test_silver_disabled_skips_writer(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_SILVER",
        False,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.return_value = []

    pipeline.bronze_writer.write.return_value = (
        "2026-08-12T00:00:00"
    )

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.silver_writer.write.assert_not_called()



def test_gold_enabled_calls_writer(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_GOLD",
        True,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.return_value = []

    pipeline.bronze_writer.write.return_value = (
        "2026-08-12T00:00:00"
    )

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.gold_writer.write.return_value = []

    pipeline.run()

    pipeline.gold_writer.write.assert_called_once_with(
        [],
        pipeline.validator.validate.return_value.metrics,
        "2026-08-12T00:00:00",
    )


def test_gold_disabled_skips_writer(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_GOLD",
        False,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.return_value = []

    pipeline.bronze_writer.write.return_value = (
        "2026-08-12T00:00:00"
    )

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.gold_writer.write.assert_not_called()


def test_warehouse_enabled_calls_loaders(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_WAREHOUSE",
        True,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.return_value = []

    pipeline.bronze_writer.write.return_value = (
        "2026-08-12T00:00:00"
    )

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.gold_writer.write.return_value = []

    pipeline.run()

    pipeline.loader.load.assert_called_once_with([])

    pipeline.fact_loader.load_articles.assert_called_once_with(
        []
    )


def test_warehouse_disabled_skips_loaders(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_WAREHOUSE",
        False,
    )

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.bronze_writer = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.dimension_loader = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.fact_loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.quality_service = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.return_value = []

    pipeline.bronze_writer.write.return_value = (
        "2026-08-12T00:00:00"
    )

    pipeline.transformer.transform.return_value = []

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks={},
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.gold_writer.write.return_value = []

    pipeline.run()

    pipeline.loader.load.assert_not_called()

    pipeline.fact_loader.load_articles.assert_not_called()