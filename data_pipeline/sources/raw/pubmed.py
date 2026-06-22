import requests


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search(query: str, retmax: int = 10):
    """
    Search PubMed and return PMIDs.
    """

    response = requests.get(
        f"{BASE_URL}/esearch.fcgi",
        params={
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": retmax,
        },
    )

    response.raise_for_status()

    data = response.json()

    return data["esearchresult"]["idlist"]