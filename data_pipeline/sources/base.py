from abc import ABC, abstractmethod

from data_pipeline.models.paper import Paper


class BaseSource(ABC):
    """
    Base interface for all literature sources.
    """

    name: str

    @abstractmethod
    def search(self, query: str, retmax: int = 100) -> list[str]:
        """
        Search the source and return identifiers.
        """
        ...

    @abstractmethod
    def fetch(self, identifiers: list[str]) -> list[Paper]:
        """
        Fetch papers given identifiers.
        """
        ...

    def search_and_fetch(
        self,
        query: str,
        retmax: int = 100,
    ) -> list[Paper]:
        """
        Default implementation shared by every source.
        """

        identifiers = self.search(query, retmax)

        if not identifiers:
            return []

        return self.fetch(identifiers)