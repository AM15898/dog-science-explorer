from data_pipeline.ingestion.discover import discover_pmids
from data_pipeline.ingestion.fetch import fetch_all_xml
from data_pipeline.parsers.pubmed_parser import parse_pubmed_xml
from data_pipeline.storage.writer import save_papers_json
from pathlib import Path


def main():

    discovery = discover_pmids()

    pmids = sorted(discovery.all_pmids)

    print()
    print(f"Unique PMIDs: {len(pmids)}")

    xml_docs = fetch_all_xml(pmids)

    papers = []

    print()
    print("=" * 60)
    print("Parsing XML")
    print("=" * 60)

    for i, xml in enumerate(xml_docs, start=1):

        parsed = parse_pubmed_xml(xml)
        papers.extend(parsed)

        print(
            f"Batch {i}/{len(xml_docs)} "
            f"| Total papers: {len(papers)}"
        )

    OUTPUT_FILE = Path("storage/processed/papers.json")

    save_papers_json(
        papers,
        OUTPUT_FILE,
        overwrite=True
    )

    print()
    print("=" * 60)
    print("Finished")
    print("=" * 60)
    print(f"Papers saved: {len(papers)}")


if __name__ == "__main__":
    main()