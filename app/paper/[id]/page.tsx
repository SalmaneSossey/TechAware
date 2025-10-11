import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { ArrowLeft, ExternalLink, FileText, Lightbulb, Calendar, Users } from "lucide-react"
import Link from "next/link"
import { ShareButtons } from "@/components/share-buttons"

// Mock data - in production, fetch from API
const mockPaper = {
  id: "1",
  arxiv_id: "2401.12345",
  title: "Efficient Attention Mechanisms for Large Language Models",
  authors: ["Smith, J.", "Johnson, A.", "Williams, R."],
  abstract:
    "We propose a novel attention mechanism that reduces computational complexity while maintaining model performance. Our approach achieves 40% faster training times on large-scale language models without sacrificing accuracy. The key innovation lies in a sparse attention pattern that leverages the inherent structure of natural language to reduce the quadratic complexity of standard attention mechanisms. We demonstrate the effectiveness of our approach on multiple benchmarks including GLUE, SuperGLUE, and various domain-specific tasks. Our method is compatible with existing transformer architectures and can be easily integrated into popular frameworks. Extensive ablation studies show that our approach maintains strong performance across different model sizes and training regimes.",
  category: "Machine Learning",
  published_at: "2024-01-15",
  pdf_url: "https://arxiv.org/pdf/2401.12345",
  summary_short:
    "Novel attention mechanism reduces LLM training time by 40% while maintaining accuracy through sparse attention patterns that leverage natural language structure.",
  impact_suggestions: [
    "MLOps: Faster model training and deployment cycles, reducing infrastructure costs",
    "Research: New baseline for efficient transformer architectures",
    "Industry: Enables training larger models on existing hardware",
    "Education: More accessible experimentation for students and researchers",
  ],
  tags: ["LLM", "Attention", "Efficiency", "Transformers", "Deep Learning"],
  score: 95,
}

interface PageProps {
  params: {
    id: string
  }
}

export default function PaperDetailPage({ params }: PageProps) {
  const paper = mockPaper // In production: await fetchPaper(params.id)

  const formattedDate = new Date(paper.published_at).toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  })

  return (
    <main className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        {/* Back button */}
        <Button variant="ghost" size="sm" className="mb-6" asChild>
          <Link href="/explore">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Explore
          </Link>
        </Button>

        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-wrap items-center gap-3 mb-4">
            <Badge variant="secondary" className="text-sm">
              {paper.category}
            </Badge>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Calendar className="h-4 w-4" />
              <span>{formattedDate}</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <FileText className="h-4 w-4" />
              <span>arXiv:{paper.arxiv_id}</span>
            </div>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold mb-6 text-balance leading-tight">{paper.title}</h1>

          <div className="flex items-center gap-2 text-muted-foreground mb-6">
            <Users className="h-5 w-5" />
            <p className="text-lg">{paper.authors.join(", ")}</p>
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap gap-3">
            <Button size="lg" asChild>
              <a href={paper.pdf_url} target="_blank" rel="noopener noreferrer">
                <FileText className="h-5 w-5 mr-2" />
                Read PDF
              </a>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <a href={`https://arxiv.org/abs/${paper.arxiv_id}`} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="h-5 w-5 mr-2" />
                View on arXiv
              </a>
            </Button>
            <ShareButtons paper={paper} />
          </div>
        </div>

        <Separator className="my-8" />

        {/* AI Summary */}
        <Card className="mb-8 border-primary/20 bg-gradient-to-br from-card to-primary/5">
          <CardHeader>
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-full bg-primary/20 border-2 border-primary flex items-center justify-center">
                <div className="w-5 h-5 rounded-full bg-primary animate-pulse" />
              </div>
              <h2 className="text-2xl font-bold">AI-Generated Summary</h2>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-lg leading-relaxed">{paper.summary_short}</p>
          </CardContent>
        </Card>

        {/* Impact Suggestions */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Lightbulb className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-bold">Where It Helps</h2>
            </div>
            <p className="text-muted-foreground">Real-world applications and impact areas</p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {paper.impact_suggestions.map((suggestion, idx) => {
                const [area, description] = suggestion.split(":")
                return (
                  <div key={idx} className="flex gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                      {idx + 1}
                    </div>
                    <div>
                      <p className="font-semibold text-primary">{area}</p>
                      <p className="text-muted-foreground">{description}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Abstract */}
        <Card className="mb-8">
          <CardHeader>
            <h2 className="text-2xl font-bold">Abstract</h2>
          </CardHeader>
          <CardContent>
            <p className="text-base leading-relaxed text-muted-foreground">{paper.abstract}</p>
          </CardContent>
        </Card>

        {/* Tags */}
        <Card className="mb-8">
          <CardHeader>
            <h2 className="text-2xl font-bold">Topics & Keywords</h2>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {paper.tags.map((tag) => (
                <Badge key={tag} variant="outline" className="text-sm px-3 py-1">
                  {tag}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* CTA */}
        <Card className="border-primary/20 bg-gradient-to-br from-card via-card to-primary/5">
          <CardContent className="p-8 text-center">
            <h3 className="text-2xl font-bold mb-3">Stay Updated</h3>
            <p className="text-muted-foreground mb-6">
              Get daily digests of breakthrough research like this delivered to your Telegram
            </p>
            <Button size="lg" asChild>
              <a href="https://t.me/techaware_bot?start=web" target="_blank" rel="noopener noreferrer">
                Subscribe on Telegram
              </a>
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
