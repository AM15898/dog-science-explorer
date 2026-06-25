from pathlib import Path

QUERY_DIR = Path(__file__).parent / "queries"


def load_query_registry() -> dict[str, list[str]]:
    """
    Load all query files.

    Returns
    -------
    {
        "behavior": [...],
        "genetics": [...],
        ...
    }
    """

    registry = {}

    for file in sorted(QUERY_DIR.glob("*.txt")):
        queries = []

        with open(file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                queries.append(line)

        registry[file.stem] = queries

    return registry