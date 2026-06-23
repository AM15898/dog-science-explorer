from pathlib import Path


def save_raw_pubmed(query: str, content: str):
    filename = query.lower().replace(" ", "-")

    path = Path("storage/raw/pubmed")

    path.mkdir(parents=True, exist_ok=True)

    file_path = path / f"{filename}.xml"

    file_path.write_text(content)

    return file_path