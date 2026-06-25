from data_pipeline.config import SEED_QUERIES

from data_pipeline.sources.europe_pmc.client import search
from data_pipeline.sources.europe_pmc.parser import parse

from data_pipeline.storage.writer import save_papers_json


def main():

    all_results = {}

    query_count = 0

    print("\nDog Science Explorer")
    print("========================")
    print("Europe PMC Ingestion")

    for category, queries in SEED_QUERIES.items():

        print(f"\n[{category.upper()}]")

        for query in queries:

            query_count += 1

            print(f"Searching: {query}")

            results = search(
                query=query,
                page_size=500,
            )

            new_results = 0

            for result in results:

                pmid = result.get("pmid") or result.get("id")

                if pmid and pmid not in all_results:
                    all_results[pmid] = result
                    new_results += 1

            print(
                f"Found {len(results)} results "
                f"({new_results} new)"
            )

    # Parse once after deduplication
    papers = parse(list(all_results.values()))

    save_papers_json(
        papers,
        "storage/processed/europe_pmc_papers.json",
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

    keyword_count = sum(
        1
        for paper in papers
        if paper.keywords
    )

    mesh_count = sum(
        1
        for paper in papers
        if paper.mesh_terms
    )

    print()
    print(f"Papers with keywords : {keyword_count}")
    print(f"Papers with MeSH     : {mesh_count}")

    print("\n========================")
    print("Europe PMC Summary")
    print("========================")
    print(f"Queries Run: {query_count}")
    print(f"Unique Results: {len(all_results)}")
    print(f"Papers Parsed: {len(papers)}")
    print(f"Missing Abstracts: {missing_abstracts}")
    print(f"Missing DOI: {missing_doi}")
    print(f"Journals: {journals}")
    print()
    print("Saved Dataset:")
    print("storage/processed/europe_pmc_papers.json")
    print("========================")


if __name__ == "__main__":
    main()