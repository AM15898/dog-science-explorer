from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from data_pipeline.sources.pubmed import search, fetch_details
from data_pipeline.storage.writer import save_raw_pubmed

def main():
    query = "golden retriever"

    print(f"\nSearching PubMed for: {query}")

    pmids = search(query)

    print(f"Found {len(pmids)} papers")

    xml = fetch_details(pmids)

    file_path = save_raw_pubmed(query, xml)

    print(f"\nSaved raw XML to:")
    print(file_path)


if __name__ == "__main__":
    main()