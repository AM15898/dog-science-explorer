from pathlib import Path

from data_pipeline.parsers.pubmed_parser import (
    parse_pubmed_xml,
)

from data_pipeline.storage.writer import (
    save_papers_json
)


def main():
    xml_path = Path(
        "storage/raw/pubmed/sample.xml"
    )

    xml_content = xml_path.read_text(
        encoding="utf-8"
    )

    papers = parse_pubmed_xml(xml_content)

    print(
        f"Parsed {len(papers)} papers"
    )

    if papers:
        print()
        print("First paper:")
        print(papers[0])
    
    save_papers_json(
        papers,
        "storage/processed/papers.json",
    )

    print(
        "\nSaved dataset to storage/processed/papers.json"
    )


if __name__ == "__main__":
    main()