from data_pipeline.analysis import load_papers

papers = load_papers()

print(f"Papers loaded: {len(papers)}")

paper = papers[0]

print()
print(paper.title)
print(paper.publication_date)
print(paper.journal)
print(paper.retrievals)