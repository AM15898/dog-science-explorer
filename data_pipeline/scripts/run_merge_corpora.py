from data_pipeline.analysis.loader import load_papers as load_corpus
from data_pipeline.merge.merge_corpora import merge_corpora
from data_pipeline.storage.writer import save_papers_json


def main():

    pubmed = load_corpus("storage/processed/pubmed.json")
    europepmc = load_corpus("storage/processed/europemc.json")

    merged = merge_corpora(pubmed, europepmc)

    save_papers_json(
        merged,
        "storage/processed/merged.json",
    )

    print(f"PubMed      : {len(pubmed):>6}")
    print(f"Europe PMC  : {len(europepmc):>6}")
    print("-" * 30)
    print(f"Merged      : {len(merged):>6}")


if __name__ == "__main__":
    main()