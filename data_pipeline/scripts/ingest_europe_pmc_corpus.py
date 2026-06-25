from data_pipeline.config import SEED_QUERIES

from data_pipeline.sources.europe_pmc.client import search
from data_pipeline.sources.europe_pmc.parser import parse

from data_pipeline.storage.writer import save_papers_json


def main():

    all_papers = []

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
                page_size=50,
            )

            papers = parse(results)

            print(
                f"Parsed {len(papers)} papers"
            )

            all_papers.extend(papers)

    save_papers_json(
        all_papers,
        "storage/processed/europe_pmc_papers.json",
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

    keyword_count = sum(
        1
        for paper in all_papers
        if paper.keywords
    )

    mesh_count = sum(
        1
        for paper in all_papers
        if paper.mesh_terms
    )

    print(f"Papers with keywords : {keyword_count}")
    print(f"Papers with MeSH     : {mesh_count}")

    print("\n========================")
    print("Europe PMC Summary")
    print("========================")
    print(f"Queries Run: {query_count}")
    print(f"Papers Parsed: {len(all_papers)}")
    print(f"Missing Abstracts: {missing_abstracts}")
    print(f"Missing DOI: {missing_doi}")
    print(f"Journals: {journals}")
    print()
    print("Saved Dataset:")
    print("storage/processed/europe_pmc_papers.json")
    print("========================")


if __name__ == "__main__":
    main()