import json
from dataclasses import asdict
from pathlib import Path

from data_pipeline.models.paper import Paper


def save_papers_json(
    papers: list[Paper],
    output_file: str,
):
    Path(output_file).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    paper_dicts = [
        asdict(paper)
        for paper in papers
    ]

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            paper_dicts,
            f,
            indent=2,
            ensure_ascii=False,
        )


def save_raw_xml(
    xml_content: str,
    output_file: str,
):
    Path(output_file).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(xml_content)