from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.paper import Paper, PaperResponse, PapersListResponse
from app.services.paper_service import PaperService

router = APIRouter()
paper_service = PaperService()

@router.get("", response_model=PapersListResponse)
async def get_papers(
    search: Optional[str] = Query(None, description="Search query"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    category: Optional[str] = Query(None, description="Category filter"),
    since: Optional[str] = Query(None, description="Date filter (YYYY-MM-DD)"),
    sort: Optional[str] = Query("recent", description="Sort by: recent, relevant, score"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Get paginated list of papers with optional filters"""
    return await paper_service.get_papers(
        search=search,
        tags=tags.split(",") if tags else None,
        category=category,
        since=since,
        sort=sort,
        page=page,
        limit=limit
    )

@router.get("/{paper_id}", response_model=PaperResponse)
async def get_paper(paper_id: str):
    """Get a single paper by ID or arXiv ID"""
    return await paper_service.get_paper(paper_id)

@router.get("/daily/top", response_model=List[Paper])
async def get_daily_top(n: int = Query(3, ge=1, le=10)):
    """Get top N papers for the day"""
    return await paper_service.get_daily_top(n)
