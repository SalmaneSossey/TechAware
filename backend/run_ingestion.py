#!/usr/bin/env python3
"""
Run full ingestion via API endpoint
"""
import requests
import json

print("=" * 70)
print("RUNNING FULL ARXIV INGESTION")
print("=" * 70)

url = "http://localhost:8000/ingest/run"
params = {
    "max_results": 15,
    "days_back": 7,
    "categories": "cs.AI,cs.LG,cs.CV,cs.CL"
}

print(f"\n📡 Sending request to {url}")
print(f"   Parameters: {params}\n")

try:
    response = requests.post(url, params=params, timeout=300)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ INGESTION SUCCESSFUL!")
        print("=" * 70)
        print(f"New papers ingested: {data.get('new_papers', 0)}")
        print(f"Total papers in database: {data.get('total_papers', 0)}")
        
        if 'papers' in data and data['papers']:
            print(f"\n📚 Sample papers (first {len(data['papers'])}):")
            print("-" * 70)
            for i, paper in enumerate(data['papers'][:3], 1):
                print(f"\n{i}. {paper['title']}")
                print(f"   📅 {paper['published_at']} | 📊 Score: {paper['score']}")
                print(f"   🏷️  {', '.join(paper['tags'])}")
                print(f"   📝 {paper['summary_short'][:120]}...")
        
        print("\n" + "=" * 70)
        print("✅ You can now view papers at:")
        print("   Frontend: http://localhost:3000")
        print("   API: http://localhost:8000/papers")
        print("=" * 70)
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("\n⏱️  Request timed out. This is normal for first ingestion.")
    print("   The model download and summarization takes time.")
    print("   Check backend logs for progress.")
except Exception as e:
    print(f"\n❌ Error: {e}")
