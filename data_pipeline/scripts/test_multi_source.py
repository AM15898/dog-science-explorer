from pathlib import Path

from data_pipeline.sources.pubmed.client import (
    search as pubmed_search,
    fetch_details as pubmed_fetch,
)
from data_pipeline.sources.pubmed.parser import (
    parse_pubmed_xml,
)

from data_pipeline.sources.europe_pmc.client import search as epmc_search
from data_pipeline.sources.europe_pmc.parser import parse as parse_epmc

from data_pipeline.storage.writer import save_papers_json


# PubMed
pmids = pubmed_search("dog cognition", retmax=1)
xml = pubmed_fetch(pmids)
pubmed_papers = parse_pubmed_xml(xml)

# Europe PMC
results = epmc_search("dog cognition", page_size=1)
epmc_papers = parse_epmc(results)

papers = pubmed_papers + epmc_papers

save_papers_json(
    papers,
    Path("storage/processed/test_multi_source.json"),
)

print(f"PubMed papers     : {len(pubmed_papers)}")
print(f"Europe PMC papers : {len(epmc_papers)}")
print(f"Total papers      : {len(papers)}")