from pprint import pprint

from data_pipeline.sources.europe_pmc.client import search
from data_pipeline.sources.europe_pmc.parser import parse

results = search(
    "dog cognition",
    page_size=2,
)

papers = parse(results)

print(f"Parsed {len(papers)} papers\n")

pprint(papers[0])