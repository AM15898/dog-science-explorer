import json
import random

with open("storage/processed/papers.json") as f:
    pubmed = json.load(f)

with open("storage/processed/europe_pmc_papers.json") as f:
    epmc = json.load(f)

pubmed_ids = {
    p["paper_id"]
    for p in pubmed
}

europe_only = [
    p
    for p in epmc
    if p["paper_id"] not in pubmed_ids
]

print(f"Europe-only papers: {len(europe_only)}")

print()

for paper in random.sample(europe_only, 10):
    print("=" * 80)
    print(paper["paper_id"])
    print(paper["title"])
    print(paper["journal"])
    print(paper["publication_date"])
    print(paper["doi"])
    print(paper["abstract"][:300])
    print()