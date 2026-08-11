from unittest.mock import MagicMock

import pytest

from src.framework.error.exceptions import PipelineException
from src.framework.pipeline import Pipeline


def test_watermark_not_updated_when_pipeline_fails():

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

    pipeline.collector.collect.side_effect = (
        PipelineException("Collection failed")
    )

    with pytest.raises(PipelineException):

        pipeline.run()

    pipeline.watermark_service.update_many.assert_not_called()


def test_watermark_not_updated_when_gold_fails():

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
        latest_watermarks={
            "Reuters": "2026-08-11T10:00:00"
        },
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.gold_writer.write.side_effect = (
        PipelineException("Gold write failed")
    )

    with pytest.raises(PipelineException):

        pipeline.run()

    pipeline.watermark_service.update_many.assert_not_called()


def test_pipeline_failure_is_tracked():

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.schema_validator = MagicMock()
    pipeline.preprocessor = MagicMock()
    pipeline.transformer = MagicMock()
    pipeline.incremental_filter = MagicMock()
    pipeline.validator = MagicMock()
    pipeline.tracker = MagicMock()

    pipeline.collector.collect.side_effect = (
        PipelineException("Collection failed")
    )

    with pytest.raises(PipelineException):

        pipeline.run()

    pipeline.tracker.finish.assert_called_once()

    call = pipeline.tracker.finish.call_args

    assert call.kwargs["run_id"] == (
        pipeline.tracker.start.return_value
    )

    assert call.kwargs["records_processed"] == 0

    assert call.kwargs["success"] is False

    assert call.kwargs["error_message"] == (
        "Collection failed"
    )


def test_watermark_not_updated_when_loader_fails():

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
        latest_watermarks={
            "Reuters": "2026-08-11T10:00:00",
        },
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.loader.load.side_effect = (
        PipelineException("Warehouse load failed")
    )

    with pytest.raises(PipelineException):

        pipeline.run()

    pipeline.watermark_service.update_many.assert_not_called()

    pipeline.tracker.finish.assert_called_once()

    call = pipeline.tracker.finish.call_args

    assert call.kwargs["success"] is False

    assert call.kwargs["error_message"] == (
        "Warehouse load failed"
    )


def test_watermark_updated_when_pipeline_succeeds():

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

    latest_watermarks = {
        "Reuters": "2026-08-11T10:00:00",
    }

    pipeline.incremental_filter.filter.return_value = MagicMock(
        new_articles=[],
        latest_watermarks=latest_watermarks,
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.run()

    pipeline.watermark_service.update_many.assert_called_once_with(
        latest_watermarks
    )


def test_pipeline_stops_after_gold_failure():

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
        latest_watermarks={
            "Reuters": "2026-08-11T10:00:00",
        },
    )

    pipeline.validator.validate.return_value = MagicMock(
        valid_articles=[],
        invalid_articles=[],
        metrics=MagicMock(),
    )

    pipeline.gold_writer.write.side_effect = (
        PipelineException("Gold write failed")
    )

    with pytest.raises(PipelineException):

        pipeline.run()

    pipeline.loader.load.assert_not_called()

    pipeline.watermark_service.update_many.assert_not_called()


def test_pipeline_preserves_original_exception():

    pipeline = Pipeline()

    pipeline.collector = MagicMock()
    pipeline.tracker = MagicMock()

    error = PipelineException(
        "Collection failed"
    )

    pipeline.collector.collect.side_effect = error

    with pytest.raises(PipelineException) as exc_info:

        pipeline.run()

    assert exc_info.value is error

    pipeline.tracker.finish.assert_called_once()

    call = pipeline.tracker.finish.call_args

    assert call.kwargs["success"] is False

    assert call.kwargs["error_message"] == (
        "Collection failed"
    )