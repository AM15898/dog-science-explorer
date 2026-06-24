from data_pipeline.config import SEED_QUERIES

from data_pipeline.sources.pubmed import (
    search,
    fetch_details,
    fetch_details_batched
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

    
    all_papers = []

    xml_batches = fetch_details_batched(
        list(all_pmids),
        batch_size=100,
    )

    for xml in xml_batches:
        papers = parse_pubmed_xml(xml)

    all_papers.extend(papers)

    save_raw_xml(
        xml,
        "storage/raw/pubmed/canine_corpus.xml",
    )

    all_papers = parse_pubmed_xml(xml)

    if not all_papers:
        raise ValueError(
            "No papers were parsed."
        )

    save_papers_json(
        all_papers,
        "storage/processed/papers.json",
    )

    missing_abstracts = sum(
        1
        for paper in all_papers
        if not paper.abstract
    )

    missing_doi = sum(
        1
        for paper in all_papers
        if not paper.doi
    )

    journals = len(
        {
            paper.journal
            for paper in all_papers
            if paper.journal
        }
    )

    print("\n========================")
    print("Dog Science Explorer")
    print("========================")
    print(f"Queries Run: {query_count}")
    print(f"Unique PMIDs: {len(all_pmids)}")
    print(f"Papers Parsed: {len(all_papers)}")
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