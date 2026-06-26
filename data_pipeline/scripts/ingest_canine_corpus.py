from data_pipeline.config import SEED_QUERIES
from collections import defaultdict

from data_pipeline.models.paper import RetrievalRecord

from data_pipeline.sources.pubmed.client import (
    search,
    fetch_details,
    fetch_details_batched
)

from data_pipeline.sources.pubmed.parser import (
    parse_pubmed_xml,
)

from data_pipeline.storage.writer import (
    save_papers_json,
    save_raw_xml,
)

#######Turn ON for testing#########

TEST_MODE = False

###################################


def main():
    all_pmids = set()

    query_hits = defaultdict(set)

    query_count = 0

    print("\nDog Science Explorer")
    print("========================")

    for category, queries in list(SEED_QUERIES.items())[:1 if TEST_MODE else None]:
        print(f"\n[{category.upper()}]")

        for query in queries[:1 if TEST_MODE else None]:
            query_count += 1

            print(f"Searching: {query}")

            pmids = search(
                query=query,
                retmax=1 if TEST_MODE else 500,
            )

            print(
                f"Found {len(pmids)} PMIDs"
            )

            for pmid in pmids:
                all_pmids.add(pmid)
                query_hits[str(pmid)].add(query)

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

    for i, xml in enumerate(xml_batches):
        papers = parse_pubmed_xml(xml)

        print(
            f"Batch {i + 1}: "
            f"{len(papers)} papers"
        )

        all_papers.extend(papers)

    print("\n========================")
    print("DEBUG")
    print("========================")
    print("Query hits:")
    print(dict(query_hits))

    for paper in all_papers:

        print(f"\nPaper ID: {paper.paper_id}")

        matching_queries = query_hits.get(str(paper.paper_id), set())

        print(f"Matching queries: {matching_queries}")

        for query in matching_queries:

            paper.retrievals.append(
                RetrievalRecord(
                    source="PubMed",
                    query=query,
                )
            )

        print(f"Retrievals: {paper.retrievals}")

    save_raw_xml(
        xml_batches[-1],
        "storage/raw/pubmed/canine_corpus.xml",
    )

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