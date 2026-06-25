from collections import defaultdict

from data_pipeline.query_registry import load_query_registry
from data_pipeline.sources.pubmed import search


class DiscoveryResult:
    def __init__(self):
        self.by_family = defaultdict(set)

    @property
    def all_pmids(self):
        pmids = set()

        for values in self.by_family.values():
            pmids.update(values)

        return pmids


def discover_pmids(retmax: int = 500) -> DiscoveryResult:
    """
    Discover PMIDs across every query family.

    Returns
    -------
    DiscoveryResult
    """

    registry = load_query_registry()

    result = DiscoveryResult()

    print()
    print("=" * 60)
    print("PubMed Discovery")
    print("=" * 60)

    for family, queries in registry.items():

        print(f"\n[{family}]")

        for query in queries:

            print(f"  Searching: {query}")

            try:
                pmids = search(query=query, retmax=retmax)

                result.by_family[family].update(pmids)

                print(f"     {len(pmids)} PMIDs")

            except Exception as e:
                print(f"     ERROR: {e}")

    return result