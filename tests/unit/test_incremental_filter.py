from src.framework.incremental.incremental_filter import (
    IncrementalFilter,
)


def test_first_run_accepts_articles():

    incremental = IncrementalFilter()

    incremental.watermark_service.repository.save({})

    articles = [
        {
            "source": "Reuters",
            "published_at": "2026-08-08",
        }
    ]

    result = incremental.filter(
        articles
    )

    assert len(result.new_articles) == 1

    assert (
        result.latest_watermarks["Reuters"]
        == "2026-08-08"
    )


def test_existing_watermark_filters_old_articles():

    incremental = IncrementalFilter()

    incremental.watermark_service.repository.save(
        {
            "Reuters": "2026-08-08"
        }
    )

    articles = [
        {
            "source": "Reuters",
            "published_at": "2026-08-08",
        },
        {
            "source": "Reuters",
            "published_at": "2026-08-09",
        },
    ]

    result = incremental.filter(
        articles
    )

    assert len(result.new_articles) == 1

    assert (
        result.new_articles[0]["published_at"]
        == "2026-08-09"
    )


def test_older_articles_are_ignored():

    incremental = IncrementalFilter()

    incremental.watermark_service.repository.save(
        {
            "Reuters": "2026-08-09"
        }
    )

    articles = [
        {
            "source": "Reuters",
            "published_at": "2026-08-08",
        }
    ]

    result = incremental.filter(
        articles
    )

    assert result.new_articles == []

    assert result.latest_watermarks == {}


def test_multiple_sources():

    incremental = IncrementalFilter()

    incremental.watermark_service.repository.save(
        {
            "Reuters": "2026-08-08",
            "Bloomberg": "2026-08-07",
        }
    )

    articles = [
        {
            "source": "Reuters",
            "published_at": "2026-08-09",
        },
        {
            "source": "Bloomberg",
            "published_at": "2026-08-08",
        },
    ]

    result = incremental.filter(
        articles
    )

    assert len(result.new_articles) == 2

    assert (
        result.latest_watermarks["Reuters"]
        == "2026-08-09"
    )

    assert (
        result.latest_watermarks["Bloomberg"]
        == "2026-08-08"
    )


def test_latest_watermark_is_kept():

    incremental = IncrementalFilter()

    incremental.watermark_service.repository.save({})

    articles = [
        {
            "source": "Reuters",
            "published_at": "2026-08-07",
        },
        {
            "source": "Reuters",
            "published_at": "2026-08-09",
        },
        {
            "source": "Reuters",
            "published_at": "2026-08-08",
        },
    ]

    result = incremental.filter(
        articles
    )

    assert (
        result.latest_watermarks["Reuters"]
        == "2026-08-09"
    )


def test_duplicate_articles_are_not_processed_twice():

    incremental = IncrementalFilter()

    incremental.watermark_service.repository.save({})

    articles = [
        {
            "source": "Reuters",
            "published_at": "2026-08-09",
            "canonical_url": (
                "https://example.com/article-1"
            ),
        },
        {
            "source": "Reuters",
            "published_at": "2026-08-09",
            "canonical_url": (
                "https://example.com/article-1"
            ),
        },
    ]

    result = incremental.filter(
        articles
    )

    assert len(result.new_articles) == 1


def test_different_articles_are_both_processed():

    incremental = IncrementalFilter()

    incremental.watermark_service.repository.save({})

    articles = [
        {
            "source": "Reuters",
            "published_at": "2026-08-09",
            "canonical_url": (
                "https://example.com/article-1"
            ),
        },
        {
            "source": "Reuters",
            "published_at": "2026-08-09",
            "canonical_url": (
                "https://example.com/article-2"
            ),
        },
    ]

    result = incremental.filter(
        articles
    )

    assert len(result.new_articles) == 2