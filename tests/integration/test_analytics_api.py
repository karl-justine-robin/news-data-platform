from fastapi.testclient import TestClient

from api.app.main import app


client = TestClient(app)


def test_warehouse_sources():

    response = client.get(
        "/api/v1/analytics/warehouse/sources"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        assert "source" in item
        assert "article_count" in item
        assert item["article_count"] > 0


def test_warehouse_dates():

    response = client.get(
        "/api/v1/analytics/warehouse/dates"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        assert "date" in item
        assert "article_count" in item
        assert item["article_count"] > 0


def test_warehouse_months():

    response = client.get(
        "/api/v1/analytics/warehouse/months"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        assert "year" in item
        assert "month" in item
        assert "month_name" in item
        assert "article_count" in item
        assert item["article_count"] > 0


def test_warehouse_days_of_week():

    response = client.get(
        "/api/v1/analytics/warehouse/days-of-week"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        assert "day_of_week" in item
        assert "article_count" in item
        assert item["article_count"] > 0