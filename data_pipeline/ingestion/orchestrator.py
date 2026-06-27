from data_pipeline.models.paper import Paper
from data_pipeline.storage.corpus import save_corpus


class IngestionOrchestrator:
    """
    Runs ingestion for one or more literature sources.
    """

    def ingest_source(
        self,
        source,
        queries: list[str],
        output_file: str,
        retmax: int = 500,
    ) -> list[Paper]:

        print(f"\n{'=' * 70}")
        print(source.name)
        print(f"{'=' * 70}")

        papers = []

        for query in queries:

            print(f"Searching: {query}")

            query_papers = source.search_and_fetch(
                query,
                retmax=retmax,
            )

            papers.extend(query_papers)

            print(f"Retrieved {len(query_papers)} papers")

        save_corpus(
            papers,
            output_file,
        )

        print()
        print(f"Saved {len(papers)} papers")
        print(output_file)

        return papers