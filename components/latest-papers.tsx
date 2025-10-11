import { PaperCard } from "@/components/paper-card"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"
import Link from "next/link"

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

export function LatestPapers() {
  return (
    <section id="latest" className="py-24 px-4">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-balance">Latest Research Breakthroughs</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
            Discover cutting-edge papers with AI-powered summaries and real-world impact analysis
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {mockPapers.map((paper) => (
            <PaperCard key={paper.id} paper={paper} />
          ))}
        </div>

        <div className="text-center">
          <Button size="lg" variant="outline" className="rounded-xl bg-transparent" asChild>
            <Link href="/explore">
              Explore All Papers
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  )
}
