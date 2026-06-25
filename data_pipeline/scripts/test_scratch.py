import json

with open("storage/processed/papers.json") as f:
    papers = json.load(f)

print(papers[0].keys())
