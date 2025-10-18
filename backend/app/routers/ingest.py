"""
Ingest router for fetching and processing papers from arXiv
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.scraper import ArxivScraper
from app.services.summarizer import Summarizer
from app.services.paper_service import PaperService
from app.models.paper import Paper
import json
import os
from datetime import datetime

router = APIRouter()
scraper = ArxivScraper()
summarizer = Summarizer()
paper_service = PaperService()

# Data file path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")

def ensure_data_dir():
    """Ensure data directory exists"""
    os.makedirs(DATA_DIR, exist_ok=True)

def load_papers():
    """Load papers from JSON file"""
    ensure_data_dir()
    if os.path.exists(PAPERS_FILE):
        with open(PAPERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_papers(papers):
    """Save papers to JSON file"""
    ensure_data_dir()
    with open(PAPERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

def categorize_arxiv(category_code: str) -> str:
    """Map arXiv category codes to human-readable categories"""
    category_map = {
        "cs.AI": "Artificial Intelligence",
        "cs.LG": "Machine Learning",
        "cs.CV": "Computer Vision",
        "cs.CL": "Natural Language Processing",
        "cs.NE": "Neural Networks",
        "cs.RO": "Robotics",
        "cs.CR": "Privacy & Security",
        "cs.DC": "Distributed Computing",
        "cs.SE": "Software Engineering",
    }
    return category_map.get(category_code, "Computer Science")

@router.post("/run")
async def run_ingestion(
    max_results: int = 20,
    days_back: int = 7,
    categories: Optional[str] = None
):
    """
    Fetch papers from arXiv, generate summaries, and store them
    
    Args:
        max_results: Maximum number of papers to fetch
        days_back: How many days back to search
        categories: Comma-separated arXiv categories (e.g., "cs.AI,cs.LG")
    """
    try:
        # Parse categories
        if categories:
            category_list = [c.strip() for c in categories.split(",")]
        else:
            category_list = ["cs.AI", "cs.LG", "cs.CV", "cs.CL"]
        
        print(f"📡 Fetching papers from arXiv...")
        print(f"   Categories: {category_list}")
        print(f"   Days back: {days_back}")
        print(f"   Max results: {max_results}")
        
        # Fetch papers from arXiv
        raw_papers = scraper.fetch_recent_papers(
            categories=category_list,
            max_results=max_results,
            days_back=days_back
        )
        
        if not raw_papers:
            return {
                "message": "No papers found",
                "count": 0,
                "papers": []
            }
        
        print(f"✅ Found {len(raw_papers)} papers")
        print(f"🤖 Generating summaries and impact suggestions...")
        
        # Load existing papers
        existing_papers = load_papers()
        existing_ids = {p.get("arxiv_id") for p in existing_papers}
        
        # Process papers
        processed_papers = []
        new_count = 0
        
        for idx, raw_paper in enumerate(raw_papers, 1):
            arxiv_id = raw_paper["arxiv_id"]
            
            # Skip if already processed
            if arxiv_id in existing_ids:
                continue
            
            print(f"   [{idx}/{len(raw_papers)}] Processing: {raw_paper['title'][:50]}...")
            
            # Generate summary
            summary = await summarizer.summarize(raw_paper["abstract"])
            
            # Generate impact suggestions
            impact = await summarizer.suggest_impact(
                raw_paper["title"],
                raw_paper["abstract"]
            )
            
            # Extract tags from title and abstract
            tags = await summarizer.extract_tags(
                raw_paper["title"],
                raw_paper["abstract"]
            )
            
            # Create paper object
            paper = {
                "id": arxiv_id,
                "arxiv_id": arxiv_id,
                "title": raw_paper["title"],
                "authors": raw_paper["authors"],
                "abstract": raw_paper["abstract"],
                "category": categorize_arxiv(raw_paper["category"]),
                "published_at": raw_paper["published_at"],
                "pdf_url": raw_paper["pdf_url"],
                "summary_short": summary,
                "impact_suggestions": impact,
                "tags": tags,
                "score": raw_paper["score"]
            }
            
            processed_papers.append(paper)
            new_count += 1
        
        # Add new papers to existing ones
        all_papers = existing_papers + processed_papers
        
        # Sort by published date (newest first) and limit to most recent 100
        all_papers.sort(key=lambda p: p["published_at"], reverse=True)
        all_papers = all_papers[:100]
        
        # Save to file
        save_papers(all_papers)
        
        # Update paper service
        paper_service.reload_papers()
        
        print(f"✅ Ingestion complete!")
        print(f"   New papers: {new_count}")
        print(f"   Total papers: {len(all_papers)}")
        
        return {
            "message": "Papers ingested successfully",
            "new_papers": new_count,
            "total_papers": len(all_papers),
            "papers": processed_papers[:5]  # Return first 5 as sample
        }
        
    except Exception as e:
        print(f"❌ Error during ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@router.get("/status")
async def get_ingestion_status():
    """Get status of ingested papers"""
    papers = load_papers()
    
    if not papers:
        return {
            "papers_count": 0,
            "latest_paper": None,
            "categories": [],
            "date_range": None
        }
    
    # Get statistics
    categories = list(set(p["category"] for p in papers))
    dates = [p["published_at"] for p in papers]
    
    return {
        "papers_count": len(papers),
        "latest_paper": papers[0]["title"] if papers else None,
        "categories": categories,
        "date_range": {
            "earliest": min(dates),
            "latest": max(dates)
        }
    }
