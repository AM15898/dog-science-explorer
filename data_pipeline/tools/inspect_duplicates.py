from collections import defaultdict
import json
from pathlib import Path

DATASET = Path("storage/processed/merged.json")


def load_corpus():
    with open(DATASET, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_title(title: str | None) -> str:
    """
    Normalize titles for duplicate inspection.

    This is intentionally lightweight.
    A future normalizer.py will become more sophisticated.
    """

    if not title:
        return ""

    return " ".join(title.lower().strip().split())


def inspect_duplicates(papers):

    by_pmid = defaultdict(list)
    by_doi = defaultdict(list)
    by_title = defaultdict(list)
    by_title_year = defaultdict(list)

    missing_doi = 0

    for paper in papers:

        #
        # PMID
        #

        if paper.get("paper_id"):
            by_pmid[paper["paper_id"]].append(paper)

        #
        # DOI
        #

        doi = paper.get("doi")

        if doi:

            doi = doi.lower().strip()

            by_doi[doi].append(paper)

        else:
            missing_doi += 1

        #
        # Title
        #

        title = normalize_title(paper.get("title"))

        if title:
            by_title[title].append(paper)

        #
        # Title + Year
        #

        year = ""

        if paper.get("publication_date"):
            year = str(paper["publication_date"])[:4]

        if title and year:
            by_title_year[(title, year)].append(paper)

    return {

        "pmid_duplicates":
            {k: v for k, v in by_pmid.items() if len(v) > 1},

        "doi_duplicates":
            {k: v for k, v in by_doi.items() if len(v) > 1},

        "title_duplicates":
            {k: v for k, v in by_title.items() if len(v) > 1},

        "title_year_duplicates":
            {k: v for k, v in by_title_year.items() if len(v) > 1},

        "missing_doi": missing_doi
    }


def print_examples(title, duplicates, limit=20):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

    if not duplicates:
        print("None")
        return

    shown = 0

    for key, papers in duplicates.items():

        print()
        print(f"Key: {key}")
        print("-" * 50)

        for paper in papers:

            retrievals = paper.get("retrievals", [])

            sources = sorted(
                {
                    r["source"]
                    for r in retrievals
                }
            )

            print(f"Paper ID : {paper.get('paper_id')}")
            print(f"Journal  : {paper.get('journal')}")
            print(f"Sources  : {', '.join(sources)}")
            print()

        shown += 1

        if shown >= limit:
            break


def main():

    papers = load_corpus()

    results = inspect_duplicates(papers)

    print("\nCorpus Summary")
    print("=" * 70)

    print(f"Total papers                : {len(papers)}")
    print(f"Missing DOI                 : {results['missing_doi']}")

    print(f"\nDuplicate PMID groups       : {len(results['pmid_duplicates'])}")
    print(f"Duplicate DOI groups        : {len(results['doi_duplicates'])}")
    print(f"Duplicate Title groups      : {len(results['title_duplicates'])}")
    print(f"Duplicate Title+Year groups : {len(results['title_year_duplicates'])}")

    print_examples(
        "Duplicate DOI",
        results["doi_duplicates"],
    )

    print_examples(
        "Duplicate Titles",
        results["title_duplicates"],
    )

    print_examples(
        "Duplicate Title + Year",
        results["title_year_duplicates"],
    )


if __name__ == "__main__":
    main()