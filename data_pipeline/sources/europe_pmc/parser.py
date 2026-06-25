from data_pipeline.models.paper import Paper


def parse(results) -> list[Paper]:
    papers = []

    for article in results:
        authors = [
            author["fullName"]
            for author in article.get("authorList", {}).get("author", [])
            if "fullName" in author
        ]

        mesh_terms = [
            mesh["descriptorName"]
            for mesh in article.get("meshHeadingList", {}).get("meshHeading", [])
        ]

        publication_types = article.get("pubTypeList", {}).get("pubType", [])

        paper = Paper(
            paper_id=article.get("pmid", article.get("id", "")),
            title=article.get("title", ""),
            abstract=article.get("abstractText", ""),
            authors=authors,
            journal=article.get("journalInfo", {})
                          .get("journal", {})
                          .get("title", ""),
            publication_date=article.get("firstPublicationDate", ""),
            doi=article.get("doi", ""),
            keywords=[],
            language=[article["language"]] if article.get("language") else [],
            publication_types=publication_types,
            mesh_terms=mesh_terms,
            source="europe_pmc",
        )

        papers.append(paper)

    return papers