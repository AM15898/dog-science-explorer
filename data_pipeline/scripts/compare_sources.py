import json


with open("storage/processed/pubmed.json") as f:
    pubmed = json.load(f)

with open("storage/processed/europemc.json") as f:
    europe_pmc = json.load(f)


pubmed_pmids = {
    paper["paper_id"]
    for paper in pubmed
}

epmc_pmids = {
    paper["paper_id"]
    for paper in europe_pmc
}


overlap = pubmed_pmids & epmc_pmids
pubmed_only = pubmed_pmids - epmc_pmids
epmc_only = epmc_pmids - pubmed_pmids


print("Corpus Comparison")
print("=" * 50)

print(f"PubMed papers      : {len(pubmed_pmids):>6}")
print(f"Europe PMC papers  : {len(epmc_pmids):>6}")
print()

print(f"Overlap            : {len(overlap):>6}")
print(f"PubMed only        : {len(pubmed_only):>6}")
print(f"Europe PMC only    : {len(epmc_only):>6}")

print()
print(f"Overlap % of Europe PMC : {100 * len(overlap) / len(epmc_pmids):.1f}%")
print(f"New papers from Europe PMC : {100 * len(epmc_only) / len(epmc_pmids):.1f}%")