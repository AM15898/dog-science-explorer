from data_pipeline.analysis.loader import load_papers


pubmed = load_papers("storage/processed/test_papers.json")
openalex = load_papers("storage/processed/test_openalex.json")


pubmed_dois = {
    p.doi.lower()
    for p in pubmed
    if p.doi
}

openalex_dois = {
    p.doi.lower()
    for p in openalex
    if p.doi
}

overlap = pubmed_dois & openalex_dois

print("=" * 60)
print("PUBMED vs OPENALEX")
print("=" * 60)

print(f"PubMed papers      : {len(pubmed)}")
print(f"OpenAlex papers    : {len(openalex)}")
print()

print(f"Shared DOI         : {len(overlap)}")
print(f"PubMed only        : {len(pubmed_dois-openalex_dois)}")
print(f"OpenAlex only      : {len(openalex_dois-pubmed_dois)}")

print()

print(
    f"OpenAlex overlap : "
    f"{len(overlap)/len(openalex_dois)*100:.1f}%"
)