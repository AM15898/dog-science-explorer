from pprint import pprint

from data_pipeline.sources.europe_pmc.client import search

results = search(
    "dog cognition",
    page_size=1,
)

paper = results[0]

print(f"{len(paper.keys())} fields\n")

for key in sorted(paper.keys()):
    print(key)