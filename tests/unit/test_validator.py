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

    validated = validator.validate(articles)

    assert len(validated) == 1


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

    validated = validator.validate(articles)

    assert validated == []


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

    validated = validator.validate(articles)

    assert validated == []


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

    validated = validator.validate(articles)

    assert validated == []


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

    validated = validator.validate(articles)

    assert len(validated) == 2

