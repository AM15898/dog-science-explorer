from collections import Counter


def collect_metrics(papers):

    journals = Counter()
    authors = Counter()
    keywords = Counter()
    years = Counter()

    mesh_terms = Counter()
    publication_types = Counter()
    languages = Counter()

    missing_abstract = 0
    missing_doi = 0
    missing_journal = 0
    missing_publication_date = 0
    missing_authors = 0

    pubmed_only = 0
    europemc_only = 0
    multi_source = 0

    abstract_lengths = []

    for paper in papers:

        #
        # Missing fields
        #

        if not paper.get("abstract"):
            missing_abstract += 1
        else:
            abstract_lengths.append(len(paper["abstract"]))

        if not paper.get("doi"):
            missing_doi += 1

        if not paper.get("journal"):
            missing_journal += 1

        if not paper.get("publication_date"):
            missing_publication_date += 1

        if not paper.get("authors"):
            missing_authors += 1

        #
        # Counters
        #

        if paper.get("journal"):
            journals[paper["journal"]] += 1

        authors.update(paper.get("authors", []))
        keywords.update(paper.get("keywords", []))
        mesh_terms.update(paper.get("mesh_terms", []))
        publication_types.update(paper.get("publication_types", []))
        languages.update(paper.get("language", []))

        #
        # Years
        #

        publication_date = paper.get("publication_date")

        if publication_date:
            years[str(publication_date)[:4]] += 1

        #
        # Source overlap
        #

        retrievals = paper.get("retrievals", [])

        sources = {r["source"] for r in retrievals}

        if len(sources) == 1:

            source = next(iter(sources))

            if source == "pubmed":
                pubmed_only += 1

            elif source == "europe_pmc":
                europemc_only += 1

        elif len(sources) > 1:
            multi_source += 1

    return {

        "total_papers": len(papers),

        "unique_journals": len(journals),

        "coverage":

        {
            "earliest": min(years) if years else None,
            "latest": max(years) if years else None,
        },

        "missing":

        {
            "abstract": missing_abstract,
            "doi": missing_doi,
            "journal": missing_journal,
            "publication_date": missing_publication_date,
            "authors": missing_authors,
        },

        "top_journals": journals.most_common(20),

        "top_mesh_terms": mesh_terms.most_common(30),

        "publication_types": publication_types.most_common(),

        "languages": languages.most_common(),

        "publication_years": dict(sorted(years.items())),

        "average_abstract_length":

        sum(abstract_lengths) / len(abstract_lengths)
        if abstract_lengths else 0,

        "average_authors":

        sum(authors.values()) / len(papers),

        "retrieval":

        {
            "pubmed_only": pubmed_only,
            "europemc_only": europemc_only,
            "multi_source": multi_source,
        }
    }