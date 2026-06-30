import requests
import time

BASE_URL = "https://api.openalex.org/works"


class OpenAlexClient:
    def __init__(self, email: str | None = None):
        self.session = requests.Session()

        self.params = {}

        # OpenAlex recommends providing your email
        if email:
            self.params["mailto"] = email

    def search(
        self,
        query: str,
        per_page: int = 200,
        cursor: str = "*",
    ):
        params = {
            **self.params,
            "search": query,
            "per-page": per_page,
            "cursor": cursor,
        }

        response = self.session.get(
            BASE_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        time.sleep(0.1)

        return response.json()