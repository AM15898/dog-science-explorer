from collections import Counter
from statistics import mean

from data_pipeline.analysis.loader import load_papers


papers = load_papers("storage/processed/test_openalex.json")

print("=" * 60)
print("OPENALEX FIELD COVERAGE")
print("=" * 60)

print(f"Total papers : {len(papers)}")

fields = {
    "Abstract": lambda p: bool(p.abstract),
    "DOI": lambda p: bool(p.doi),
    "Authors": lambda p: len(p.authors) > 0,
    "Journal": lambda p: bool(p.journal),
    "Publication Date": lambda p: bool(p.publication_date),
    "Keywords": lambda p: len(p.keywords) > 0,
    "Mesh Terms": lambda p: len(p.mesh_terms) > 0,
}

print()

for field, fn in fields.items():

    count = sum(fn(p) for p in papers)

    print(
        f"{field:<20}"
        f"{count:>6}/{len(papers)} "
        f"({count/len(papers)*100:.1f}%)"
    )

print()

years = [
    int(p.publication_date[:4])
    for p in papers
    if p.publication_date
]

print(f"Coverage : {min(years)} - {max(years)}")

print(f"Unique Journals : {len(set(p.journal for p in papers if p.journal))}")

print(f"Average Authors : {mean(len(p.authors) for p in papers):.2f}")

print()

print("Top Journals")

counter = Counter(
    p.journal
    for p in papers
    if p.journal
)

for journal, count in counter.most_common(10):
    print(f"{count:>4} {journal}")