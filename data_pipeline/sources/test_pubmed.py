from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from data_pipeline.sources.raw.pubmed import search


def main():
    pmids = search("golden retriever")

    print("\nPubMed Results\n")

    for pmid in pmids:
        print(pmid)


if __name__ == "__main__":
    main()