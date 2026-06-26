import time
import requests

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
BATCH_SIZE = 90
REQUEST_DELAY = 0.34  # ~3 requests/second


def search(query: str, retmax: int = 10):
    response = requests.get(
        f"{BASE_URL}/esearch.fcgi",
        params={
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": retmax,
        },
        timeout=REQUEST_TIMEOUT,
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
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.text


def fetch_details_batched(
    pmids,
    batch_size=BATCH_SIZE,
):
    all_xml = []

    total_batches = (len(pmids) + batch_size - 1) // batch_size

    for i in range(0, len(pmids), batch_size):

        batch = pmids[i : i + batch_size]

        batch_number = i // batch_size + 1

        print(
            f"Fetching batch "
            f"{batch_number}/{total_batches}"
        )

        for attempt in range(MAX_RETRIES):

            try:
                xml = fetch_details(batch)

                all_xml.append(xml)

                # Be polite to NCBI
                time.sleep(REQUEST_DELAY)

                break

            except requests.RequestException as e:

                print(
                    f"  Attempt {attempt + 1}/{MAX_RETRIES} failed:"
                )
                print(f"  {e}")

                if attempt == MAX_RETRIES - 1:
                    raise

                wait = 2 ** attempt

                print(
                    f"  Retrying in {wait} seconds..."
                )

                time.sleep(wait)

    return all_xml