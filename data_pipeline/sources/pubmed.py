import requests
import xml.etree.ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search(query: str, retmax: int = 10):
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


def fetch_details(pmids):
    """
    Fetch detailed paper information.
    """

    ids = ",".join(pmids)

    response = requests.get(
        f"{BASE_URL}/efetch.fcgi",
        params={
            "db": "pubmed",
            "id": ids,
            "retmode": "xml",
        },
    )

    response.raise_for_status()

    return response.text