from fastapi import APIRouter
from typing import List
from app.services.paper_service import PaperService

router = APIRouter()
paper_service = PaperService()

@router.get("", response_model=List[str])
async def get_tags():
    """Get all available tags"""
    return await paper_service.get_all_tags()
