from itertools import islice

from data_pipeline.sources.pubmed import fetch_details


def chunks(iterable, size):

    iterable = iter(iterable)

    while True:

        batch = list(islice(iterable, size))

        if not batch:
            return

        yield batch


def fetch_all_xml(pmids, batch_size=200):

    xml_documents = []

    total = len(pmids)

    print()
    print("=" * 60)
    print("Fetching XML")
    print("=" * 60)

    for i, batch in enumerate(chunks(pmids, batch_size), start=1):

        print(
            f"Batch {i} "
            f"({len(batch)} papers)"
        )

        xml = fetch_details(batch)

        xml_documents.append(xml)

    print()
    print(f"Fetched {total} papers")

    return xml_documents