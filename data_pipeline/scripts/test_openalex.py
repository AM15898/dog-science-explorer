from data_pipeline.sources.openalex.client import OpenAlexClient
from data_pipeline.sources.openalex.parser import parse_work


client = OpenAlexClient()

# response = client.search(
#     "dog osteoarthritis",
#     per_page=5,
# )

# for work in response["results"]:

#     paper = parse_work(work)

#     print("=" * 80)
#     print(paper.paper_id)
#     print(paper.title)
#     print(paper.journal)
#     print(paper.doi)

import json

response = client.search("dog osteoarthritis", per_page=1)

with open("sample_openalex.json", "w") as f:
    json.dump(response["results"][0], f, indent=2)