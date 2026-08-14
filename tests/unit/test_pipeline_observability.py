from unittest.mock import MagicMock

import pytest

from src.framework.pipeline import Pipeline


def test_pipeline_logs_stage_lifecycle(caplog):

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.tracker = MagicMock()
    pipeline.quality_service = MagicMock()

    pipeline.collector.collect.return_value = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

    pipeline.preprocessor.preprocess.return_value = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

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

    with caplog.at_level("INFO"):
        pipeline.run()

    assert "[COLLECT] Starting" in caplog.text
    assert "[COLLECT] Completed" in caplog.text

    assert "[TRANSFORM] Starting" in caplog.text
    assert "[TRANSFORM] Completed" in caplog.text

    assert "[VALIDATE] Starting" in caplog.text
    assert "[VALIDATE] Completed" in caplog.text

    assert "[WAREHOUSE] Starting" in caplog.text
    assert "[WAREHOUSE] Completed" in caplog.text


def test_pipeline_records_run_level_observability():

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.tracker = MagicMock()
    pipeline.quality_service = MagicMock()

    pipeline.collector.collect.return_value = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

    pipeline.preprocessor.preprocess.return_value = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

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

    pipeline.tracker.start.assert_called_once()
    pipeline.tracker.finish.assert_called_once()

    call = pipeline.tracker.finish.call_args

    assert call.kwargs["run_id"] == (
        pipeline.tracker.start.return_value
    )

    assert call.kwargs["success"] is True
    assert call.kwargs["records_processed"] == 0



def test_pipeline_records_failed_run_observability():

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.side_effect = RuntimeError(
        "Collection service unavailable"
    )

    with pytest.raises(RuntimeError):

        pipeline.run()

    pipeline.tracker.start.assert_called_once()
    pipeline.tracker.finish.assert_called_once()

    call = pipeline.tracker.finish.call_args

    assert call.kwargs["run_id"] == (
        pipeline.tracker.start.return_value
    )

    assert call.kwargs["success"] is False

    assert call.kwargs["records_processed"] == 0

    assert call.kwargs["error_message"] == (
        "Collection service unavailable"
    )



def test_pipeline_logs_execution_time(caplog):

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.silver_writer = MagicMock()
    pipeline.gold_writer = MagicMock()
    pipeline.loader = MagicMock()
    pipeline.watermark_service = MagicMock()
    pipeline.tracker = MagicMock()
    pipeline.quality_service = MagicMock()

    pipeline.collector.collect.return_value = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

    pipeline.preprocessor.preprocess.return_value = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

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

    with caplog.at_level("INFO"):
        pipeline.run()

    assert "Execution time:" in caplog.text
    assert "seconds" in caplog.text