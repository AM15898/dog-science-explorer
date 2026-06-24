from data_pipeline.sources.pubmed import (
    search,
    fetch_details,
)


def main():
    print("Fetching one paper...\n")

    pmids = search(
        query="dog",
        retmax=1,
    )

    print(f"PMID: {pmids[0]}\n")

    xml = fetch_details(pmids)

    print(xml)


if __name__ == "__main__":
    main()