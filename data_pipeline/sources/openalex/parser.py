from data_pipeline.models.paper import Paper


def parse_work(work: dict) -> Paper:

    # -------------------------
    # Authors
    # -------------------------

    authors = []

    for authorship in work.get("authorships", []):

        author = authorship.get("author")

        if author and author.get("display_name"):
            authors.append(author["display_name"])

    # -------------------------
    # DOI
    # -------------------------

    doi = work.get("doi")

    if doi:
        doi = doi.replace("https://doi.org/", "")

    # -------------------------
    # Journal
    #
    # Prefer a real journal over repositories like PubMed
    # -------------------------

    journal = None

    for location in work.get("locations", []):

        source = location.get("source")

        if (
            source
            and source.get("type") == "journal"
            and source.get("display_name")
        ):
            journal = source["display_name"]
            break

    if journal is None:

        primary = work.get("primary_location")

        if primary:

            source = primary.get("source")

            if source:
                journal = source.get("display_name")

    # -------------------------
    # Keywords
    # -------------------------

    keywords = [
        k["display_name"]
        for k in work.get("keywords", [])
        if k.get("display_name")
    ]

    # -------------------------
    # Concepts
    #
    # Store in keywords for now
    # since Paper has no concepts field
    # -------------------------

    keywords.extend(

        c["display_name"]

        for c in work.get("concepts", [])

        if c.get("display_name")
    )

    keywords = sorted(set(keywords))

    # -------------------------
    # MeSH
    # -------------------------

    mesh_terms = []

    for mesh in work.get("mesh", []):

        descriptor = mesh.get("descriptor_name")

        qualifier = mesh.get("qualifier_name")

        if descriptor:

            if qualifier:
                mesh_terms.append(f"{descriptor} ({qualifier})")

            else:
                mesh_terms.append(descriptor)

    mesh_terms = sorted(set(mesh_terms))

    # -------------------------
    # Publication type
    # -------------------------

    publication_types = []

    if work.get("type"):
        publication_types.append(work["type"])

    # -------------------------
    # Language
    # -------------------------

    language = work.get("language")

    # -------------------------
    # Abstract
    # -------------------------

    abstract = None

    # OpenAlex only provides an abstract for some papers.
    # Reconstruct it if available.

    inverted = work.get("abstract_inverted_index")

    if inverted:

        words = []

        max_pos = max(
            pos
            for positions in inverted.values()
            for pos in positions
        )

        words = [""] * (max_pos + 1)

        for word, positions in inverted.items():

            for pos in positions:
                words[pos] = word

        abstract = " ".join(words)

    return Paper(
        paper_id=work["id"].split("/")[-1],
        title=work.get("title"),
        abstract=abstract,
        authors=authors,
        journal=journal,
        publication_date=str(work.get("publication_year")),
        doi=doi,
        keywords=keywords,
        language=language,
        publication_types=publication_types,
        mesh_terms=mesh_terms,
        source="OpenAlex",
        retrievals=[],
    )