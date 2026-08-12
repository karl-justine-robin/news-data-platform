from unittest.mock import MagicMock

from src.framework.pipeline import Pipeline
import src.framework.pipeline as pipeline_module


def test_pipeline_runs_with_optional_stages_disabled(
    monkeypatch,
):
    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_INCREMENTAL",
        False,
    )

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_BRONZE",
        False,
    )

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_SILVER",
        False,
    )

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_GOLD",
        False,
    )

    monkeypatch.setattr(
        pipeline_module,
        "ENABLE_WAREHOUSE",
        False,
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

    pipeline.collector.collect.return_value = []

    pipeline.transformer.transform.return_value = []

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.incremental_filter.filter.assert_not_called()

    pipeline.bronze_writer.write.assert_not_called()

    pipeline.silver_writer.write.assert_not_called()

    pipeline.gold_writer.write.assert_not_called()

    pipeline.loader.load.assert_not_called()

    pipeline.fact_loader.load_articles.assert_not_called()

    pipeline.watermark_service.update_many.assert_not_called()