from pathlib import Path

from data_pipeline.parsers.pubmed_parser import parse_pubmed_xml


xml_file = next(
    Path("storage/raw/pubmed").glob("*.xml")
)

xml_content = xml_file.read_text()

papers = parse_pubmed_xml(xml_content)

paper = papers[0]

print("TITLE:")
print(paper.title)

print("\nLANGUAGE:")
print(paper.language)

print("\nPUBLICATION TYPES:")
print(paper.publication_types)

print("\nMESH TERMS:")
print(paper.mesh_terms[:20])