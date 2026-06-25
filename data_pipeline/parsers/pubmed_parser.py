import xml.etree.ElementTree as ET

from data_pipeline.models.paper import Paper


def extract_language(article):
    return [
        lang.text.strip()
        for lang in article.findall(".//Language")
        if lang.text
    ]


def extract_publication_types(article):
    return [
        p.text.strip()
        for p in article.findall(".//PublicationType")
        if p.text
    ]


def extract_mesh_terms(article):
    results = []

    for item in article.findall(".//MeshHeading"):
        descriptor = item.find("DescriptorName")

        if descriptor is not None and descriptor.text:
            results.append(descriptor.text.strip())

    return results


def parse_pubmed_xml(xml_content: str) -> list[Paper]:
    root = ET.fromstring(xml_content)

    papers = []

    for article in root.findall(".//PubmedArticle"):

        pmid = article.findtext(".//PMID", default="")

        title = article.findtext(
            ".//ArticleTitle",
            default=""
        )

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

        publication_date = year or ""

        doi = ""

        for article_id in article.findall(".//ArticleId"):
            if article_id.get("IdType") == "doi":
                doi = article_id.text or ""
                break

        keywords = []

        for keyword in article.findall(".//Keyword"):
            if keyword.text:
                keywords.append(
                    keyword.text.strip()
                )

        languages = extract_language(article)

        publication_types = extract_publication_types(article)

        mesh_terms = extract_mesh_terms(article)

        paper = Paper(
            paper_id=pmid,
            title=title,
            abstract=abstract,
            authors=authors,
            journal=journal,
            publication_date=publication_date,
            doi=doi,
            keywords=keywords,
            language=languages,
            publication_types=publication_types,
            mesh_terms=mesh_terms,
            source="pubmed",
        )

        papers.append(paper)

    return papers