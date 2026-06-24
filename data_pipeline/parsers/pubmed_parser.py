import xml.etree.ElementTree as ET

from data_pipeline.models.paper import Paper


def parse_pubmed_xml(xml_content: str) -> list[Paper]:
    root = ET.fromstring(xml_content)

    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID", default="")

        title = article.findtext(".//ArticleTitle", default="")

        abstract_parts = article.findall(".//AbstractText")

        abstract = " ".join(
            part.text or ""
            for part in abstract_parts
        ).strip()

        journal = article.findtext(
            ".//Journal/Title",
            default=""
        )

        authors = []

        for author in article.findall(".//Author"):
            lastname = author.findtext(
                "LastName",
                default=""
            )

            firstname = author.findtext(
                "ForeName",
                default=""
            )

            full_name = (
                f"{firstname} {lastname}"
            ).strip()

            if full_name:
                authors.append(full_name)
        
                year = article.findtext(
            ".//PubDate/Year",
            default=""
        )

        publication_date = (
            year if year else None
        )

        doi = article.findtext(
            ".//ArticleId[@IdType='doi']"
        )

        keywords = []

        for keyword in article.findall(".//Keyword"):
            if keyword.text:
                keywords.append(
                    keyword.text.strip()
                )

        paper = Paper(
            paper_id=pmid,
            title=title,
            abstract=abstract,
            authors=authors,
            journal=journal,
            publication_date=publication_date,
            doi=doi,
            keywords=keywords
        )

        papers.append(paper)

    return papers