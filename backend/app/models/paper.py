from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Paper(BaseModel):
    id: str
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    category: str
    published_at: str
    pdf_url: str
    summary_short: str
    impact_suggestions: List[str]
    tags: List[str]
    score: float

class PaperResponse(BaseModel):
    paper: Paper

class PapersListResponse(BaseModel):
    papers: List[Paper]
    total: int
    page: int
    limit: int
    pages: int
