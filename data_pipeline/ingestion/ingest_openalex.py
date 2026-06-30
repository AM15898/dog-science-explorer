from pathlib import Path

from data_pipeline.config import SEED_QUERIES
from data_pipeline.sources.openalex.client import OpenAlexClient
from data_pipeline.sources.openalex.parser import parse_work
from data_pipeline.storage.writer import save_papers_json


def main(test_mode: bool = False):

    client = OpenAlexClient()

    papers = []

    per_query = 1 if test_mode else 200

    print()
    print("=" * 60)
    print("OpenAlex")
    print("=" * 60)

    papers = []

    for topic, queries in SEED_QUERIES.items():

        print()
        print("=" * 60)
        print(f"Topic: {topic}")
        print("=" * 60)

        for query in queries:

            print(f"Searching: {query}")

            response = client.search(
                query=query,
                per_page=5 if test_mode else 200,
            )

            works = response["results"]

            print(f"Retrieved: {len(works)}")

            for work in works:
                papers.append(parse_work(work))

    output_file = (
        Path("storage/processed/test_openalex.json")
        if test_mode
        else Path("storage/processed/openalex.json")
    )

    save_papers_json(
        papers,
        output_file,
    )

    print()
    print("=" * 60)
    print("Finished")
    print("=" * 60)
    print(f"Papers saved : {len(papers)}")
    print(f"Output       : {output_file}")


if __name__ == "__main__":
    main(test_mode=True)