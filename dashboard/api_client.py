import requests


class APIClient:

    def __init__(
        self,
        base_url,
        timeout=10,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_articles(
        self,
        params=None,
    ):

        response = requests.get(
            f"{self.base_url}/api/v1/articles",
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def search_articles(
        self,
        query,
    ):

        response = requests.get(
            f"{self.base_url}/api/v1/search",
            params={
                "q": query,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_warehouse_sources(self):

        response = requests.get(
            f"{self.base_url}/api/v1/analytics/warehouse/sources",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_warehouse_dates(self):

        response = requests.get(
            f"{self.base_url}/api/v1/analytics/warehouse/dates",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_warehouse_months(self):

        response = requests.get(
            f"{self.base_url}/api/v1/analytics/warehouse/months",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_warehouse_days_of_week(self):

        response = requests.get(
            f"{self.base_url}/api/v1/analytics/warehouse/days-of-week",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()