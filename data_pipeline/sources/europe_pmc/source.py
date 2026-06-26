from data_pipeline.models.paper import Paper
from data_pipeline.sources.base import BaseSource

from .client import search, fetch, fetch_batched
from .parser import parse


class EuropePMCSource(BaseSource):

    name = "Europe PMC"

    def search(
        self,
        query: str,
        retmax: int = 100,
    ) -> list[str]:

        return search(query, retmax)

    def fetch(
        self,
        identifiers: list[str],
    ) -> list[Paper]:

        raw = fetch_batched(identifiers)

        return parse(raw)