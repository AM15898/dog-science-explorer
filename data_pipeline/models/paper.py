from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Paper:
    paper_id: str
    title: str
    abstract: Optional[str]
    authors: List[str]
    journal: Optional[str]
    publication_date: Optional[str]
    doi: Optional[str]
    source: str = "pubmed"