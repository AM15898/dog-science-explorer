from collections import Counter
from pathlib import Path
import json

from data_pipeline.models import paper


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

    mesh_terms = Counter()
    publication_types = Counter()
    languages = Counter()

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

        for mesh in paper.get("mesh_terms", []):
            mesh_terms[mesh] += 1

        for pub_type in paper.get("publication_types", []):
            publication_types[pub_type] += 1

        for language in paper.get("language", []):
            languages[language] += 1

        publication_date = paper.get("publication_date")

        if publication_date:
            year = str(publication_date)[:4]
            years[year] += 1
    
    earliest_year = min(years.keys())
    latest_year = max(years.keys()) 

    report = {
        "total_papers": total_papers,
        "unique_journals": len(journals),
        "missing_abstracts": missing_abstract,
        "missing_doi": missing_doi,
        "top_journals": journals.most_common(20),
        "top_authors": authors.most_common(20),
        "top_keywords": keywords.most_common(20),
        "publication_years": dict(sorted(years.items())),
        "top_mesh_terms": mesh_terms.most_common(50),
        "publication_types": publication_types.most_common(),
        "languages": languages.most_common()
    }

    json_report = REPORT_DIR / "corpus_report.json"

    with open(json_report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    txt_report = REPORT_DIR / "corpus_report.txt"

    with open(txt_report, "w", encoding="utf-8") as f:

        f.write("DOG SCIENCE EXPLORER CORPUS REPORT\n")
        f.write("=" * 40 + "\n\n")

        print("Mesh Terms:", sum(mesh_terms.values()))
        print("Publication Types:", sum(publication_types.values()))
        print("Languages:", sum(languages.values()))
        
        f.write(f"Total Papers: {total_papers}\n")
        f.write(f"Unique Journals: {len(journals)}\n")
        f.write(f"Missing Abstracts: {missing_abstract}\n")
        f.write(f"Missing DOI: {missing_doi}\n")

        f.write(f"\nCoverage: {earliest_year} - {latest_year}\n")

        #
        # TOP JOURNALS
        #
        f.write("\n\nTop Journals\n")
        f.write("-" * 20 + "\n")

        for journal, count in journals.most_common(20):
            f.write(f"{count:5d} {journal}\n")

        #
        # TOP MESH TERMS
        #
        f.write("\n\nTop MeSH Terms\n")
        f.write("-" * 20 + "\n")

        for term, count in mesh_terms.most_common(30):
            f.write(f"{count:5d} {term}\n")

        #
        # PUBLICATION TYPES
        #
        f.write("\n\nPublication Types\n")
        f.write("-" * 20 + "\n")

        for pub_type, count in publication_types.most_common():
            f.write(f"{count:5d} {pub_type}\n")

        #
        # LANGUAGES
        #
        f.write("\n\nLanguages\n")
        f.write("-" * 20 + "\n")

        for language, count in languages.most_common():
            f.write(f"{count:5d} {language}\n")

        #
        # YEARS
        #
        f.write("\n\nPublication Years\n")
        f.write("-" * 20 + "\n")

        for year, count in sorted(years.items()):
            f.write(f"{year}: {count}\n")

    print(f"Saved {json_report}")
    print(f"Saved {txt_report}")


if __name__ == "__main__":
    main()