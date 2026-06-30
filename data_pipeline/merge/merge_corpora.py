from data_pipeline.models.paper import Paper


def _merge_lists(existing: list[str], incoming: list[str]) -> list[str]:
    """
    Merge two lists while preserving order and uniqueness.
    """
    seen = set(existing)
    merged = existing.copy()

    for item in incoming:
        if item not in seen:
            merged.append(item)
            seen.add(item)

    return merged


def _prefer(existing, incoming):
    """
    Prefer an existing value unless it is empty.
    """
    if existing in (None, "", []):
        return incoming
    return existing


def merge_papers(existing: Paper, incoming: Paper) -> Paper:
    """
    Merge metadata from two representations of the same paper.
    """

    existing.title = _prefer(existing.title, incoming.title)
    existing.abstract = _prefer(existing.abstract, incoming.abstract)
    existing.journal = _prefer(existing.journal, incoming.journal)
    existing.publication_date = _prefer(
        existing.publication_date,
        incoming.publication_date,
    )
    existing.doi = _prefer(existing.doi, incoming.doi)

    existing.authors = _merge_lists(
        existing.authors,
        incoming.authors,
    )

    existing.keywords = _merge_lists(
        existing.keywords,
        incoming.keywords,
    )

    existing.language = _merge_lists(
        existing.language,
        incoming.language,
    )

    existing.mesh_terms = _merge_lists(
        existing.mesh_terms,
        incoming.mesh_terms,
    )

    existing.publication_types = _merge_lists(
        existing.publication_types,
        incoming.publication_types,
    )

    for retrieval in incoming.retrievals:
        if retrieval not in existing.retrievals:
            existing.retrievals.append(retrieval)

    return existing


def merge_corpora(*corpora: list[Paper]) -> list[Paper]:
    """
    Merge multiple corpora into one.

    Duplicate papers are identified by paper_id.
    Metadata is enriched rather than overwritten.
    """

    merged: dict[str, Paper] = {}

    for corpus in corpora:

        for paper in corpus:

            if paper.paper_id not in merged:
                merged[paper.paper_id] = paper
                continue

            merge_papers(
                merged[paper.paper_id],
                paper,
            )

    return list(merged.values())