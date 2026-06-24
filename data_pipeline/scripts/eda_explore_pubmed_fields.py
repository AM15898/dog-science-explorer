import xml.etree.ElementTree as ET

from data_pipeline.sources.pubmed import (
    search,
    fetch_details,
)


def main():
    pmids = search("dog", retmax=1)

    xml = fetch_details(pmids)

    root = ET.fromstring(xml)

    article = root.find(".//PubmedArticle")

    print("\nTITLE")
    print(article.findtext(".//ArticleTitle"))

    print("\nDOI")
    doi = article.findtext(
        ".//ArticleId[@IdType='doi']"
    )
    print(doi)

    print("\nLANGUAGE")
    print(
        article.findtext(".//Language")
    )

    print("\nYEAR")
    print(
        article.findtext(
            ".//PubDate/Year"
        )
    )

    print("\nKEYWORDS")
    keywords = article.findall(
        ".//Keyword"
    )

    for keyword in keywords:
        print("-", keyword.text)

    print("\nMESH TERMS")
    mesh_terms = article.findall(
        ".//MeshHeading"
    )

    for mesh in mesh_terms[:20]:
        descriptor = mesh.find(
            "DescriptorName"
        )

        if descriptor is not None:
            print("-", descriptor.text)


if __name__ == "__main__":
    main()