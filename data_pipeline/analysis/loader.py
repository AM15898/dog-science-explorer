from pathlib import Path
import json

from data_pipeline.models.paper import Paper

DEFAULT_PATH = (
    Path(__file__).resolve().parents[2]
    / "storage"
    / "processed"
    / "papers.json"
)


def load_papers(path: Path | None = None) -> list[Paper]:
    """
    Load Paper objects from the processed JSON corpus.
    """

    path = path or DEFAULT_PATH

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Paper(**paper) for paper in data]