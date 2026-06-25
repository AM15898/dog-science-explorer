import requests

BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def search(
    query: str,
    page_size: int = 25,
):
    response = requests.get(
        BASE_URL,
        params={
            "query": query,
            "format": "json",
            "pageSize": page_size,
            "resultType": "core",
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("resultList", {}).get("result", [])


def fetch(results):
    """
    Europe PMC search already returns the metadata we need,
    so for now fetching is simply passing the results through.
    """
    return results


def fetch_batched(
    results,
    batch_size=100,
):
    """
    Placeholder to keep the interface consistent with PubMed.
    """
    return fetch(results)