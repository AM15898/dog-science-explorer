from data_pipeline.analysis import load_papers
from data_pipeline.config import PROCESSED_DIR
from data_pipeline.merge import merge_corpora
from data_pipeline.storage.corpus import save_corpus


pubmed = load_papers(PROCESSED_DIR / "papers.json")

merged = merge_corpora(pubmed)

output = save_corpus(
    merged,
    "merged.json",
)

print(f"Merged {len(merged)} papers")
print(output)