#!/usr/bin/env python3
"""
Test script to trigger arXiv paper ingestion
"""
import sys
import os
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except:
    pass

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

import asyncio
from app.services.scraper import ArxivScraper
from app.services.summarizer import Summarizer
import json

async def test_ingestion():
    """Test the ingestion flow"""
    print("=" * 60)
    print("TECHAWARE ARXIV INGESTION TEST")
    print("=" * 60)
    
    # Initialize services
    scraper = ArxivScraper()
    summarizer = Summarizer()
    
    print("\n📡 Fetching papers from arXiv...")
    print("   Categories: cs.AI, cs.LG, cs.CV, cs.CL")
    print("   Days back: 7")
    print("   Max results: 5")
    
    # Fetch papers
    papers = scraper.fetch_recent_papers(
        categories=["cs.AI", "cs.LG", "cs.CV", "cs.CL"],
        max_results=5,
        days_back=7
    )
    
    print(f"\n✅ Found {len(papers)} papers\n")
    
    if not papers:
        print("❌ No papers found!")
        return
    
    # Process first paper as test
    print("=" * 60)
    print("PROCESSING FIRST PAPER (TEST)")
    print("=" * 60)
    
    paper = papers[0]
    print(f"\n📄 Title: {paper['title']}")
    print(f"👥 Authors: {', '.join(paper['authors'][:3])}...")
    print(f"📅 Published: {paper['published_at']}")
    print(f"📊 Score: {paper['score']}")
    
    print("\n🤖 Generating summary...")
    summary = await summarizer.summarize(paper['abstract'])
    print(f"   Summary: {summary}")
    
    print("\n💡 Extracting tags...")
    tags = await summarizer.extract_tags(paper['title'], paper['abstract'])
    print(f"   Tags: {', '.join(tags)}")
    
    print("\n🎯 Generating impact suggestions...")
    impact = await summarizer.suggest_impact(paper['title'], paper['abstract'])
    for i, suggestion in enumerate(impact, 1):
        print(f"   {i}. {suggestion}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE!")
    print("=" * 60)
    print(f"\nTo ingest all papers, visit: http://localhost:8000/ingest/run")
    print(f"API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    asyncio.run(test_ingestion())
