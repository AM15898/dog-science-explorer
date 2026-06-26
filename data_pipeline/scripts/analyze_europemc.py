import json

with open("storage/processed/europe_pmc_papers.json") as f:
    papers = json.load(f)

keyword_count = sum(bool(p["keywords"]) for p in papers)
mesh_count = sum(bool(p["mesh_terms"]) for p in papers)

print(f"Total papers      : {len(papers)}")
print(f"With keywords     : {keyword_count}")
print(f"With MeSH terms   : {mesh_count}")