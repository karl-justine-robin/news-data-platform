from src.framework.analytics.analytics_service import (
    AnalyticsService,
)


def test_articles_by_source():

    service = AnalyticsService()

    results = service.articles_by_source()

    assert isinstance(results, list)

    assert len(results) > 0

    for result in results:

        assert result.source
        assert result.article_count > 0


def test_articles_by_date():

    service = AnalyticsService()

    results = service.articles_by_date()

    assert isinstance(results, list)

    assert len(results) > 0

    for result in results:

        assert result.date
        assert result.article_count > 0


def test_articles_by_month():

    service = AnalyticsService()

    results = service.articles_by_month()

    assert isinstance(results, list)

    assert len(results) > 0

    for result in results:

        assert result.year
        assert result.month
        assert result.month_name
        assert result.article_count > 0


def test_articles_by_day_of_week():

    service = AnalyticsService()

    results = service.articles_by_day_of_week()

    assert isinstance(results, list)

    assert len(results) > 0

    for result in results:

        assert result.day_of_week
        assert result.article_count > 0


def test_summary():

    service = AnalyticsService()

    result = service.summary()

    assert isinstance(result, dict)

    assert "articles_by_source" in result
    assert "articles_by_date" in result
    assert "articles_by_month" in result
    assert "articles_by_day_of_week" in result

    assert len(result["articles_by_source"]) > 0
    assert len(result["articles_by_date"]) > 0
    assert len(result["articles_by_month"]) > 0
    assert len(result["articles_by_day_of_week"]) > 0