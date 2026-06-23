from typing import List, Optional
from pydantic import BaseModel


class Paper(BaseModel):
    paper_id: str

    title: str

    abstract: Optional[str] = None

    authors: List[str] = []

    journal: Optional[str] = None

    publication_date: Optional[str] = None

    doi: Optional[str] = None

    source: str = "pubmed"