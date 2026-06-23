from pathlib import Path

from data_pipeline.parsers.pubmed_parser import (
    parse_pubmed_xml,
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


if __name__ == "__main__":
    main()