from collections import defaultdict

from data_pipeline.models.paper import Paper


def merge_corpora(*corpora: list[Paper]) -> list[Paper]:
    """
    Merge multiple paper corpora.

    Papers are deduplicated by PMID.

    Retrieval provenance is preserved.
    """

    merged: dict[str, Paper] = {}

    for corpus in corpora:

        for paper in corpus:

            if paper.paper_id not in merged:
                merged[paper.paper_id] = paper
                continue

            existing = merged[paper.paper_id]
            # Merge provenance

            existing.retrievals.extend(
                r
                for r in paper.retrievals
                if r not in existing.retrievals
            )

    return list(merged.values())