import { SearchBar } from "@/components/search-bar"
import { Filters } from "@/components/filters"
import { PaperCard } from "@/components/paper-card"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { ArrowLeft } from "lucide-react"

// Mock data - will be replaced with API calls
const mockPapers = [
  {
    id: "1",
    arxiv_id: "2401.12345",
    title: "Efficient Attention Mechanisms for Large Language Models",
    authors: ["Smith, J.", "Johnson, A.", "Williams, R."],
    abstract: "We propose a novel attention mechanism that reduces computational complexity...",
    category: "Machine Learning",
    published_at: "2024-01-15",
    pdf_url: "https://arxiv.org/pdf/2401.12345",
    summary_short: "Novel attention mechanism reduces LLM training time by 40% while maintaining accuracy.",
    impact_suggestions: [
      "MLOps: Faster model training and deployment cycles",
      "Research: New baseline for efficient transformer architectures",
    ],
    tags: ["LLM", "Attention", "Efficiency"],
    score: 95,
  },
  {
    id: "2",
    arxiv_id: "2401.23456",
    title: "Federated Learning with Differential Privacy Guarantees",
    authors: ["Chen, L.", "Kumar, P."],
    abstract: "This paper introduces a framework for federated learning with provable privacy...",
    category: "Privacy & Security",
    published_at: "2024-01-14",
    pdf_url: "https://arxiv.org/pdf/2401.23456",
    summary_short: "Framework enables privacy-preserving distributed ML with mathematical guarantees.",
    impact_suggestions: [
      "Healthcare: Secure collaborative model training across hospitals",
      "Finance: Privacy-compliant fraud detection systems",
    ],
    tags: ["Federated Learning", "Privacy", "Security"],
    score: 88,
  },
  {
    id: "3",
    arxiv_id: "2401.34567",
    title: "Real-Time Object Detection on Edge Devices",
    authors: ["Park, S.", "Lee, M.", "Kim, H."],
    abstract: "We present an optimized architecture for real-time object detection...",
    category: "Computer Vision",
    published_at: "2024-01-13",
    pdf_url: "https://arxiv.org/pdf/2401.34567",
    summary_short: "Lightweight model achieves 60 FPS object detection on mobile devices.",
    impact_suggestions: [
      "IoT: Real-time monitoring for smart cities and surveillance",
      "Robotics: Enhanced perception for autonomous navigation",
    ],
    tags: ["Computer Vision", "Edge Computing", "Real-Time"],
    score: 82,
  },
]

export default function ExplorePage() {
  return (
    <main className="min-h-screen py-12 px-4">
      <div className="container mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Button variant="ghost" size="sm" className="mb-4" asChild>
            <Link href="/">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Link>
          </Button>

          <h1 className="text-4xl md:text-5xl font-bold mb-4">Explore Research</h1>
          <p className="text-xl text-muted-foreground">
            Search and filter through the latest AI and tech breakthroughs
          </p>
        </div>

        {/* Search and Filters */}
        <div className="mb-8 space-y-6">
          <SearchBar />
          <Filters />
        </div>

        {/* Results */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockPapers.map((paper) => (
            <PaperCard key={paper.id} paper={paper} />
          ))}
        </div>

        {/* Pagination placeholder */}
        <div className="mt-12 flex justify-center gap-2">
          <Button variant="outline" disabled>
            Previous
          </Button>
          <Button variant="outline">1</Button>
          <Button variant="outline">2</Button>
          <Button variant="outline">3</Button>
          <Button variant="outline">Next</Button>
        </div>
      </div>
    </main>
  )
}
