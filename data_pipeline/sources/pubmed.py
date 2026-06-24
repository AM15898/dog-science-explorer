import requests

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

def fetch_details_batched(
    pmids,
    batch_size=100,
):
    all_xml = []

    for i in range(
        0,
        len(pmids),
        batch_size,
    ):
        batch = pmids[
            i : i + batch_size
        ]

        print(
            f"Fetching batch "
            f"{i // batch_size + 1}"
        )

        xml = fetch_details(batch)

        all_xml.append(xml)

    return all_xml