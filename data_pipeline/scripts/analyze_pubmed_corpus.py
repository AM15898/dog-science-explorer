from collections import Counter
from pathlib import Path
import json


DATASET_PATH = Path("storage/processed/papers.json")

REPORT_DIR = Path("storage/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_papers():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    papers = load_papers()

    total_papers = len(papers)

    journals = Counter()
    authors = Counter()
    keywords = Counter()
    years = Counter()

    missing_abstract = 0
    missing_doi = 0

    for paper in papers:

        if not paper.get("abstract"):
            missing_abstract += 1

        if not paper.get("doi"):
            missing_doi += 1

        if paper.get("journal"):
            journals[paper["journal"]] += 1

        for author in paper.get("authors", []):
            authors[author] += 1

        for keyword in paper.get("keywords", []):
            keywords[keyword] += 1

        publication_date = paper.get("publication_date")

        if publication_date:
            year = str(publication_date)[:4]
            years[year] += 1

    report = {
        "total_papers": total_papers,
        "unique_journals": len(journals),
        "missing_abstracts": missing_abstract,
        "missing_doi": missing_doi,
        "top_journals": journals.most_common(20),
        "top_authors": authors.most_common(20),
        "top_keywords": keywords.most_common(20),
        "publication_years": dict(sorted(years.items())),
    }

    json_report = REPORT_DIR / "corpus_report.json"

    with open(json_report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    txt_report = REPORT_DIR / "corpus_report.txt"

    with open(txt_report, "w", encoding="utf-8") as f:

        f.write("DOG SCIENCE EXPLORER CORPUS REPORT\n")
        f.write("=" * 40 + "\n\n")

        f.write(f"Total Papers: {total_papers}\n")
        f.write(f"Unique Journals: {len(journals)}\n")
        f.write(f"Missing Abstracts: {missing_abstract}\n")
        f.write(f"Missing DOI: {missing_doi}\n\n")

        f.write("Top Journals\n")
        f.write("-" * 20 + "\n")

        for journal, count in journals.most_common(20):
            f.write(f"{count:5d} {journal}\n")

    print(f"Saved {json_report}")
    print(f"Saved {txt_report}")


if __name__ == "__main__":
    main()