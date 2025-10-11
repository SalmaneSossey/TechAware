import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ExternalLink, FileText, Lightbulb } from "lucide-react"
import Link from "next/link"

interface Paper {
  id: string
  arxiv_id: string
  title: string
  authors: string[]
  abstract: string
  category: string
  published_at: string
  pdf_url: string
  summary_short: string
  impact_suggestions: string[]
  tags: string[]
  score: number
}

interface PaperCardProps {
  paper: Paper
}

export function PaperCard({ paper }: PaperCardProps) {
  const formattedDate = new Date(paper.published_at).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })

  return (
    <Card className="group hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:shadow-primary/10 flex flex-col h-full">
      <CardHeader className="space-y-3">
        <div className="flex items-start justify-between gap-2">
          <Badge variant="secondary" className="text-xs">
            {paper.category}
          </Badge>
          <span className="text-xs text-muted-foreground">{formattedDate}</span>
        </div>

        <Link href={`/paper/${paper.id}`} className="group/title">
          <h3 className="font-bold text-lg leading-tight group-hover/title:text-primary transition-colors line-clamp-2">
            {paper.title}
          </h3>
        </Link>

        <p className="text-sm text-muted-foreground line-clamp-1">{paper.authors.join(", ")}</p>
      </CardHeader>

      <CardContent className="space-y-4 flex-1">
        <p className="text-sm leading-relaxed line-clamp-3">{paper.summary_short}</p>

        {paper.impact_suggestions.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
              <Lightbulb className="h-3.5 w-3.5" />
              <span>Where it helps</span>
            </div>
            <div className="space-y-1">
              {paper.impact_suggestions.slice(0, 2).map((suggestion, idx) => (
                <p key={idx} className="text-xs text-muted-foreground pl-5">
                  • {suggestion}
                </p>
              ))}
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-2">
          {paper.tags.slice(0, 3).map((tag) => (
            <Badge key={tag} variant="outline" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>

      <CardFooter className="flex gap-2 pt-4 border-t">
        <Button size="sm" variant="outline" className="flex-1 bg-transparent" asChild>
          <Link href={`/paper/${paper.id}`}>
            <FileText className="h-4 w-4 mr-2" />
            Details
          </Link>
        </Button>
        <Button size="sm" variant="ghost" asChild>
          <a href={paper.pdf_url} target="_blank" rel="noopener noreferrer">
            <ExternalLink className="h-4 w-4" />
          </a>
        </Button>
      </CardFooter>
    </Card>
  )
}
