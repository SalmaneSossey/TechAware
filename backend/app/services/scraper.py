"""
arXiv paper scraper service
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import arxiv

class ArxivScraper:
    def __init__(self):
        self.client = arxiv.Client()
    
    def fetch_recent_papers(
        self,
        categories: List[str] = ["cs.AI", "cs.LG", "cs.CV"],
        max_results: int = 50,
        days_back: int = 7
    ) -> List[Dict]:
        """
        Fetch recent papers from arXiv
        
        Args:
            categories: List of arXiv category codes
            max_results: Maximum number of papers to fetch
            days_back: How many days back to search
            
        Returns:
            List of paper dictionaries
        """
        # Build search query
        category_query = " OR ".join([f"cat:{cat}" for cat in categories])
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Search arXiv
        search = arxiv.Search(
            query=category_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for result in self.client.results(search):
            # Filter by date
            if result.published.replace(tzinfo=None) < start_date:
                continue
            
            paper = {
                "arxiv_id": result.entry_id.split("/")[-1],
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "abstract": result.summary,
                "category": result.primary_category,
                "published_at": result.published.strftime("%Y-%m-%d"),
                "pdf_url": result.pdf_url,
                "score": self._calculate_score(result)
            }
            papers.append(paper)
        
        return papers
    
    def _calculate_score(self, paper: arxiv.Result) -> float:
        """
        Calculate relevance score for a paper
        
        Simple heuristic based on:
        - Recency (newer = higher score)
        - Number of authors (more = slightly higher)
        - Abstract length (reasonable length = higher)
        
        Args:
            paper: arXiv paper result
            
        Returns:
            Score between 0-100
        """
        score = 50.0  # Base score
        
        # Recency bonus (up to +30)
        days_old = (datetime.now() - paper.published.replace(tzinfo=None)).days
        recency_bonus = max(0, 30 - days_old)
        score += recency_bonus
        
        # Author count bonus (up to +10)
        author_bonus = min(10, len(paper.authors) * 2)
        score += author_bonus
        
        # Abstract length bonus (up to +10)
        abstract_len = len(paper.summary)
        if 500 <= abstract_len <= 2000:
            score += 10
        elif abstract_len < 500:
            score += 5
        
        return min(100, score)
    
    def get_daily_top(self, n: int = 3) -> List[Dict]:
        """
        Get top N papers from today
        
        Args:
            n: Number of papers to return
            
        Returns:
            List of top papers
        """
        papers = self.fetch_recent_papers(days_back=1, max_results=20)
        papers.sort(key=lambda p: p["score"], reverse=True)
        return papers[:n]
