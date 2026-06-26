from data_pipeline.models.paper import Paper
from data_pipeline.sources.base import BaseSource

from .client import search, fetch_details
from .parser import parse_pubmed_xml


class PubMedSource(BaseSource):

    name = "PubMed"

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

        xml = fetch_details(identifiers)

        return parse_pubmed_xml(xml)