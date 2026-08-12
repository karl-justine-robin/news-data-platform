import requests


API_URL = "http://127.0.0.1:8000"


def test_dashboard_sources_endpoint():

    response = requests.get(
        f"{API_URL}/api/v1/analytics/warehouse/sources",
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0


def test_dashboard_dates_endpoint():

    response = requests.get(
        f"{API_URL}/api/v1/analytics/warehouse/dates",
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0


def test_dashboard_months_endpoint():

    response = requests.get(
        f"{API_URL}/api/v1/analytics/warehouse/months",
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0


def test_dashboard_days_endpoint():

    response = requests.get(
        f"{API_URL}/api/v1/analytics/warehouse/days-of-week",
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0



