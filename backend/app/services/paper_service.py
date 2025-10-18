from typing import List, Optional
from app.models.paper import Paper, PapersListResponse
from app.services.summarizer import Summarizer
import math
import json
import os

class PaperService:
    def __init__(self):
        self.summarizer = Summarizer()
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        self.papers_file = os.path.join(self.data_dir, "papers.json")
        # Load papers from file or use mock data as fallback
        self.papers = self._load_papers()
    
    def _load_papers(self) -> List[Paper]:
        """Load papers from JSON file or return mock data"""
        try:
            if os.path.exists(self.papers_file):
                with open(self.papers_file, 'r', encoding='utf-8') as f:
                    papers_data = json.load(f)
                    # Convert dict to Paper objects
                    return [Paper(**paper) for paper in papers_data]
        except Exception as e:
            print(f"⚠️  Could not load papers from file: {e}")
        
        # Return mock data as fallback
        print("ℹ️  Using mock data (no papers.json found)")
        return self._get_mock_papers()
    
    def reload_papers(self):
        """Reload papers from file"""
        self.papers = self._load_papers()
        print(f"✅ Reloaded {len(self.papers)} papers")
    
    def _get_mock_papers(self) -> List[Paper]:
        """Generate mock papers for demo"""
        return [
            Paper(
                id="1",
                arxiv_id="2401.12345",
                title="Efficient Attention Mechanisms for Large Language Models",
                authors=["Smith, J.", "Johnson, A.", "Williams, R."],
                abstract="We propose a novel attention mechanism that reduces computational complexity while maintaining model performance. Our approach achieves 40% faster training times on large-scale language models.",
                category="Machine Learning",
                published_at="2024-01-15",
                pdf_url="https://arxiv.org/pdf/2401.12345",
                summary_short="Novel attention mechanism reduces LLM training time by 40% while maintaining accuracy.",
                impact_suggestions=[
                    "MLOps: Faster model training and deployment cycles",
                    "Research: New baseline for efficient transformer architectures"
                ],
                tags=["LLM", "Attention", "Efficiency"],
                score=95.0
            ),
            Paper(
                id="2",
                arxiv_id="2401.23456",
                title="Federated Learning with Differential Privacy Guarantees",
                authors=["Chen, L.", "Kumar, P."],
                abstract="This paper introduces a framework for federated learning with provable privacy guarantees using differential privacy techniques.",
                category="Privacy & Security",
                published_at="2024-01-14",
                pdf_url="https://arxiv.org/pdf/2401.23456",
                summary_short="Framework enables privacy-preserving distributed ML with mathematical guarantees.",
                impact_suggestions=[
                    "Healthcare: Secure collaborative model training across hospitals",
                    "Finance: Privacy-compliant fraud detection systems"
                ],
                tags=["Federated Learning", "Privacy", "Security"],
                score=88.0
            ),
            Paper(
                id="3",
                arxiv_id="2401.34567",
                title="Real-Time Object Detection on Edge Devices",
                authors=["Park, S.", "Lee, M.", "Kim, H."],
                abstract="We present an optimized architecture for real-time object detection on resource-constrained edge devices.",
                category="Computer Vision",
                published_at="2024-01-13",
                pdf_url="https://arxiv.org/pdf/2401.34567",
                summary_short="Lightweight model achieves 60 FPS object detection on mobile devices.",
                impact_suggestions=[
                    "IoT: Real-time monitoring for smart cities and surveillance",
                    "Robotics: Enhanced perception for autonomous navigation"
                ],
                tags=["Computer Vision", "Edge Computing", "Real-Time"],
                score=82.0
            )
        ]
    
    async def get_papers(
        self,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        since: Optional[str] = None,
        sort: str = "recent",
        page: int = 1,
        limit: int = 10
    ) -> PapersListResponse:
        """Get filtered and paginated papers"""
        filtered_papers = self.papers.copy()
        
        # Apply filters
        if search:
            search_lower = search.lower()
            filtered_papers = [
                p for p in filtered_papers
                if search_lower in p.title.lower() or search_lower in p.abstract.lower()
            ]
        
        if tags:
            filtered_papers = [
                p for p in filtered_papers
                if any(tag in p.tags for tag in tags)
            ]
        
        if category and category != "All Categories":
            filtered_papers = [p for p in filtered_papers if p.category == category]
        
        # Sort
        if sort == "recent":
            filtered_papers.sort(key=lambda p: p.published_at, reverse=True)
        elif sort == "score":
            filtered_papers.sort(key=lambda p: p.score, reverse=True)
        
        # Paginate
        total = len(filtered_papers)
        pages = math.ceil(total / limit)
        start = (page - 1) * limit
        end = start + limit
        
        return PapersListResponse(
            papers=filtered_papers[start:end],
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )
    
    async def get_paper(self, paper_id: str) -> Paper:
        """Get a single paper by ID"""
        for paper in self.papers:
            if paper.id == paper_id or paper.arxiv_id == paper_id:
                return paper
        raise ValueError(f"Paper not found: {paper_id}")
    
    async def get_daily_top(self, n: int = 3) -> List[Paper]:
        """Get top N papers for the day"""
        sorted_papers = sorted(self.papers, key=lambda p: p.score, reverse=True)
        return sorted_papers[:n]
    
    async def get_all_tags(self) -> List[str]:
        """Get all unique tags"""
        tags = set()
        for paper in self.papers:
            tags.update(paper.tags)
        return sorted(list(tags))
