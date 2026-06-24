from data_pipeline.config import SEED_QUERIES

from data_pipeline.sources.pubmed import (
    search,
    fetch_details,
)

from data_pipeline.parsers.pubmed_parser import (
    parse_pubmed_xml,
)

from data_pipeline.storage.writer import (
    save_papers_json,
)

def main():
    all_pmids = set()

    for query in SEED_QUERIES:
        print(f"\nSearching: {query}")

        pmids = search(
            query=query,
            retmax=20,
        )

        print(
            f"Found {len(pmids)} PMIDs"
        )

        all_pmids.update(pmids)

    print("\n================")

    print(
        f"Unique PMIDs: {len(all_pmids)}"
    )

    xml = fetch_details(
        list(all_pmids)
    )
    
    papers = parse_pubmed_xml(xml)

    print(
        f"Parsed papers: {len(papers)}"
    )

    save_papers_json(
        papers,
        "storage/processed/papers.json",
    )

    print(
        "\nSaved dataset:"
    )

    print(
        "storage/processed/papers.json"
    )

if __name__ == "__main__":
    main()