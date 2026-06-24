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
    save_raw_xml,
)


def main():
    all_pmids = set()

    query_count = 0

    print("\nDog Science Explorer")
    print("========================")

    for category, queries in SEED_QUERIES.items():
        print(f"\n[{category.upper()}]")

        for query in queries:
            query_count += 1

            print(f"Searching: {query}")

            pmids = search(
                query=query,
                retmax=50,
            )

            print(
                f"Found {len(pmids)} PMIDs"
            )

            all_pmids.update(pmids)

    print("\n========================")
    print(
        f"Unique PMIDs collected: {len(all_pmids)}"
    )

    if not all_pmids:
        raise ValueError(
            "No PMIDs were collected."
        )

    xml = fetch_details(
        list(all_pmids)
    )

    save_raw_xml(
        xml,
        "storage/raw/pubmed/canine_corpus.xml",
    )

    papers = parse_pubmed_xml(xml)

    if not papers:
        raise ValueError(
            "No papers were parsed."
        )

    save_papers_json(
        papers,
        "storage/processed/papers.json",
    )

    missing_abstracts = sum(
        1
        for paper in papers
        if not paper.abstract
    )

    missing_doi = sum(
        1
        for paper in papers
        if not paper.doi
    )

    journals = len(
        {
            paper.journal
            for paper in papers
            if paper.journal
        }
    )

    print("\n========================")
    print("Dog Science Explorer")
    print("========================")
    print(f"Queries Run: {query_count}")
    print(f"Unique PMIDs: {len(all_pmids)}")
    print(f"Papers Parsed: {len(papers)}")
    print(f"Missing Abstracts: {missing_abstracts}")
    print(f"Missing DOI: {missing_doi}")
    print(f"Journals: {journals}")
    print()
    print("Saved Dataset:")
    print("storage/processed/papers.json")
    print()
    print("Saved Raw XML:")
    print("storage/raw/pubmed/")
    print("========================")


if __name__ == "__main__":
    main()