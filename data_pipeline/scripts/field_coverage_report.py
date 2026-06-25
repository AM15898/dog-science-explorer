import json


def load(path):
    with open(path) as f:
        return json.load(f)


def pct(n, total):
    return 100 * n / total if total else 0


def report(name, papers):

    total = len(papers)

    abstracts = sum(bool(p["abstract"]) for p in papers)
    dois = sum(bool(p["doi"]) for p in papers)
    authors = sum(bool(p["authors"]) for p in papers)
    journals = sum(bool(p["journal"]) for p in papers)
    dates = sum(bool(p["publication_date"]) for p in papers)
    keywords = sum(bool(p["keywords"]) for p in papers)
    mesh = sum(bool(p["mesh_terms"]) for p in papers)

    avg_authors = (
        sum(len(p["authors"]) for p in papers) / total
        if total else 0
    )

    avg_abstract_len = (
        sum(len(p["abstract"]) for p in papers if p["abstract"]) / abstracts
        if abstracts else 0
    )

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Total papers        : {total:,}")
    print(f"Abstracts           : {pct(abstracts,total):6.1f}%")
    print(f"DOIs                : {pct(dois,total):6.1f}%")
    print(f"Authors             : {pct(authors,total):6.1f}%")
    print(f"Journal             : {pct(journals,total):6.1f}%")
    print(f"Publication Date    : {pct(dates,total):6.1f}%")
    print(f"Keywords            : {pct(keywords,total):6.1f}%")
    print(f"MeSH Terms          : {pct(mesh,total):6.1f}%")
    print(f"Avg Authors         : {avg_authors:.2f}")
    print(f"Avg Abstract Length : {avg_abstract_len:.0f} chars")


pubmed = load("storage/processed/papers.json")
epmc = load("storage/processed/europe_pmc_papers.json")

report("PubMed", pubmed)
report("Europe PMC", epmc)