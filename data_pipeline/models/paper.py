from dataclasses import dataclass, field
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
    keywords: List[str] = field(default_factory=list)
    language: list[str] = field(default_factory=list)
    publication_types: list[str] = field(default_factory=list)
    mesh_terms: list[str] = field(default_factory=list)
    source: str = "pubmed"