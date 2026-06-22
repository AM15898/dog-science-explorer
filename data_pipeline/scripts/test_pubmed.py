from pathlib import Path
import sys

from data_pipeline.sources.pubmed import search, fetch_details
from data_pipeline.storage.writer import save_raw_pubmed

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from data_pipeline.sources.raw.pubmed import search, fetch_details


def main():
    pmids = search("golden retriever")

    print("\nFound PMIDs:\n")

    for pmid in pmids:
        print(pmid)

    print("\nFetching details...\n")

    xml = fetch_details(pmids)

    print(xml[:2000])


if __name__ == "__main__":
    main()