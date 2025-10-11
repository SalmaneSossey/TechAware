import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ArrowLeft, Target, Zap, Brain, Globe } from "lucide-react"
import Link from "next/link"

export default function AboutPage() {
  return (
    <main className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <Button variant="ghost" size="sm" className="mb-6" asChild>
          <Link href="/">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Home
          </Link>
        </Button>

        {/* Hero */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary/20 border-2 border-primary mb-6">
            <div className="w-10 h-10 rounded-full bg-primary animate-pulse" />
          </div>

          <h1 className="text-4xl md:text-5xl font-bold mb-6">About TechAware</h1>

          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance leading-relaxed">
            Your AI-powered research companion—summarizing the latest breakthroughs in AI and software engineering,
            helping students, developers, and scientists stay ahead effortlessly.
          </p>
        </div>

        {/* Mission */}
        <Card className="mb-12 border-primary/20 bg-gradient-to-br from-card to-primary/5">
          <CardContent className="p-8">
            <h2 className="text-3xl font-bold mb-4">Our Mission</h2>
            <p className="text-lg leading-relaxed text-muted-foreground">
              TechAware empowers innovators, researchers, and learners to stay ahead by delivering distilled, actionable
              insights from the world's latest scientific and technological research—all in one accessible platform.
              It's a knowledge companion that understands, summarizes, and contextualizes research: why it matters and
              where it applies.
            </p>
          </CardContent>
        </Card>

        {/* Features */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold mb-8 text-center">What We Offer</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardContent className="p-6">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                  <Brain className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold mb-2">AI-Powered Summaries</h3>
                <p className="text-muted-foreground">
                  Complex research papers distilled into clear, 1-2 sentence summaries that capture the essence of each
                  breakthrough.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                  <Target className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold mb-2">Impact Analysis</h3>
                <p className="text-muted-foreground">
                  Understand where research applies in real-world scenarios—from MLOps to healthcare, education to
                  robotics.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                  <Zap className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold mb-2">Smart Discovery</h3>
                <p className="text-muted-foreground">
                  Advanced search and filtering by categories, tags, and keywords to find exactly what you need.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                  <Globe className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold mb-2">Daily Digests</h3>
                <p className="text-muted-foreground">
                  Stay informed with curated daily digests delivered straight to your Telegram—no information overload.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Taglines */}
        <Card className="mb-12">
          <CardContent className="p-8">
            <h2 className="text-2xl font-bold mb-6 text-center">Our Philosophy</h2>
            <div className="space-y-4 text-center">
              <p className="text-xl font-semibold text-primary">Stay Aware. Stay Ahead.</p>
              <p className="text-lg text-muted-foreground">Your Window to Tomorrow's Tech.</p>
              <p className="text-lg text-muted-foreground">From Research to Real-World Impact.</p>
              <p className="text-lg text-muted-foreground">Discover. Digest. Deploy.</p>
            </div>
          </CardContent>
        </Card>

        {/* CTA */}
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Stay Ahead?</h2>
          <p className="text-lg text-muted-foreground mb-8">Start exploring the latest research breakthroughs today</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild>
              <Link href="/explore">Explore Papers</Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <a href="https://t.me/techaware_bot?start=web" target="_blank" rel="noopener noreferrer">
                Subscribe on Telegram
              </a>
            </Button>
          </div>
        </div>
      </div>
    </main>
  )
}
