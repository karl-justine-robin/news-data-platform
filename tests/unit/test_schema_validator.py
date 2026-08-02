import pytest

from src.framework.error.exceptions import PipelineException
from src.framework.schema.schema_validator import SchemaValidator


def test_valid_schema_passes():

    validator = SchemaValidator()

    feeds = [
        {
            "source": "Reuters",
            "items": [
                {
                    "title": "Test",
                    "content": "Body",
                    "publish_date": "2026-08-02",
                    "category": "Business",
                }
            ],
        }
    ]

    validator.validate(feeds)


def test_missing_required_field_fails():

    validator = SchemaValidator()

    feeds = [
        {
            "source": "Reuters",
            "items": [
                {
                    # title intentionally missing
                    "content": "Body",
                    "publish_date": "2026-08-02",
                }
            ],
        }
    ]

    with pytest.raises(PipelineException):
        validator.validate(feeds)


def test_unknown_vendor_fails():

    validator = SchemaValidator()

    feeds = [
        {
            "source": "CNN",
            "items": [
                {
                    "title": "Test",
                    "content": "Body",
                    "publish_date": "2026-08-02",
                }
            ],
        }
    ]

    with pytest.raises(PipelineException):
        validator.validate(feeds)

def test_missing_container_fails():

    validator = SchemaValidator()

    feeds = [
        {
            "source": "Reuters",
            "articles": []
        }
    ]

    with pytest.raises(PipelineException):
        validator.validate(feeds)


def test_additional_fields_pass():

    validator = SchemaValidator()

    feeds = [
        {
            "source": "Reuters",
            "items": [
                {
                    "title": "Test",
                    "content": "Body",
                    "publish_date": "2026-08-02",
                    "category": "Business",
                    "image": "image.jpg",
                    "author": "Robin",
                }
            ],
        }
    ]

    validator.validate(feeds)


def test_empty_feed_passes():

    validator = SchemaValidator()

    feeds = [
        {
            "source": "Reuters",
            "items": [],
        }
    ]

    validator.validate(feeds)