import json
from dataclasses import asdict
from pathlib import Path

from data_pipeline.models.paper import Paper
from data_pipeline.config import PROCESSED_DIR


def save_corpus(
    papers: list[Paper],
    filename: str,
) -> Path:
    """
    Save a paper corpus to the processed directory.
    """

    output_path = PROCESSED_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            [asdict(p) for p in papers],
            f,
            indent=2,
            ensure_ascii=False,
        )

    return output_path