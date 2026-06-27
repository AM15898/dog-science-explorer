import re


def normalize_doi(doi: str | None) -> str | None:
    """
    Normalize DOI strings into canonical form.

    Examples

    DOI:10.1000/ABC123
    https://doi.org/10.1000/ABC123

    →

    10.1000/abc123
    """

    if not doi:
        return None

    doi = doi.strip().lower()

    doi = doi.replace("https://doi.org/", "")
    doi = doi.replace("http://doi.org/", "")
    doi = doi.replace("doi:", "")

    return doi.strip()


def normalize_title(title: str | None) -> str |None:
    if not title:
        return None

    title = re.sub(r"\s+", " ", title)

    return title.strip()


def normalize_journal(journal: str | None) -> str | None:
    if not journal:
        return None

    journal = re.sub(r"\s+", " ", journal)

    return journal.strip()


def normalize_language(language: str | None) -> str | None:
    if not language:
        return None

    return language.lower().strip()