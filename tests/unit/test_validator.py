from src.framework.validator.validator import Validator


def test_valid_article():

    validator = Validator()

    articles = [
        {
            "headline": "Test",
            "body": "Body",
            "published_at": "2026-08-02",
            "source": "Reuters",
        }
    ]

    result = validator.validate(articles)

    assert len(result.valid_articles) == 1
    assert len(result.invalid_articles) == 0

    assert result.metrics.total_records == 1
    assert result.metrics.valid_records == 1
    assert result.metrics.invalid_records == 0


def test_missing_headline():

    validator = Validator()

    articles = [
        {
            "headline": None,
            "body": "Body",
            "published_at": "2026-08-02",
            "source": "Reuters",
        }
    ]

    result = validator.validate(articles)

    assert result.valid_articles == []
    assert len(result.invalid_articles) == 1

    assert result.metrics.total_records == 1
    assert result.metrics.valid_records == 0
    assert result.metrics.invalid_records == 1
    assert result.metrics.missing_headline == 1


def test_missing_body():

    validator = Validator()

    articles = [
        {
            "headline": "Test",
            "body": None,
            "published_at": "2026-08-02",
            "source": "Reuters",
        }
    ]

    result = validator.validate(articles)

    assert result.valid_articles == []
    assert len(result.invalid_articles) == 1

    assert result.metrics.total_records == 1
    assert result.metrics.valid_records == 0
    assert result.metrics.invalid_records == 1
    assert result.metrics.missing_body == 1


def test_missing_publish_date():

    validator = Validator()

    articles = [
        {
            "headline": "Test",
            "body": "Body",
            "published_at": None,
            "source": "Reuters",
        }
    ]

    result = validator.validate(articles)

    assert result.valid_articles == []
    assert len(result.invalid_articles) == 1

    assert result.metrics.total_records == 1
    assert result.metrics.valid_records == 0
    assert result.metrics.invalid_records == 1
    assert result.metrics.invalid_date == 1


def test_mixed_articles():

    validator = Validator()

    articles = [
        {
            "headline": "Good",
            "body": "Body",
            "published_at": "2026-08-02",
            "source": "Reuters",
        },
        {
            "headline": None,
            "body": "Body",
            "published_at": "2026-08-02",
            "source": "Reuters",
        },
        {
            "headline": "Another",
            "body": "Body",
            "published_at": "2026-08-02",
            "source": "Bloomberg",
        },
    ]

    result = validator.validate(articles)

    assert len(result.valid_articles) == 2
    assert len(result.invalid_articles) == 1

    assert result.metrics.total_records == 3
    assert result.metrics.valid_records == 2
    assert result.metrics.invalid_records == 1
    assert result.metrics.missing_headline == 1


def test_validator_separates_valid_and_invalid_articles():
    validator = Validator()

    articles = [
        {
            "headline": "Valid Article",
            "body": "This is a valid article body.",
            "source": "Reuters",
            "canonical_url": "https://example.com/valid",
            "published_at": "2026-08-15T10:00:00",
        },
        {
            "headline": "",
            "body": "This article is missing a headline.",
            "source": "Reuters",
            "canonical_url": "https://example.com/invalid",
            "published_at": "2026-08-15T10:00:00",
        },
    ]

    result = validator.validate(articles)

    assert len(result.valid_articles) == 1
    assert len(result.invalid_articles) == 1


def test_validator_generates_correct_quality_metrics():
    validator = Validator()

    articles = [
        {
            "headline": "Valid Article",
            "body": "Valid article body.",
            "source": "Reuters",
            "canonical_url": "https://example.com/valid",
            "published_at": "2026-08-15T10:00:00",
        },
        {
            "headline": "",
            "body": "Missing headline.",
            "source": "Reuters",
            "canonical_url": "https://example.com/no-headline",
            "published_at": "2026-08-15T10:00:00",
        },
        {
            "headline": "Another Valid Article",
            "body": "Another valid article body.",
            "source": "Reuters",
            "canonical_url": "https://example.com/another",
            "published_at": "not-a-date",
        },
    ]

    result = validator.validate(articles)

    assert result.metrics.total_records == 3
    assert result.metrics.valid_records == 2
    assert result.metrics.invalid_records == 1
    assert result.metrics.missing_headline == 1
    assert result.metrics.missing_body == 0
    assert result.metrics.missing_source == 0
    assert result.metrics.invalid_date == 0