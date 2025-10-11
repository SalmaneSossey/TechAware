import { Button } from "@/components/ui/button"
import { ArrowRight, Search } from "lucide-react"
import Link from "next/link"

export function Hero() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage:
            "url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-wuUy0BwanhO4fEmPeSg34RI82YYoSY.png')",
        }}
      />

      {/* Light overlay to ensure text readability */}
      <div className="absolute inset-0 bg-white/80 backdrop-blur-sm" />

      <div className="container relative z-10 px-4 mx-auto text-center">
        {/* Logo/Brand */}
        <div className="mb-8 flex items-center justify-center gap-3">
          <div className="w-12 h-12 rounded-full bg-primary/20 border-2 border-primary flex items-center justify-center">
            <div className="w-6 h-6 rounded-full bg-primary animate-pulse" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight">TechAware</h1>
        </div>

        {/* Main headline */}
        <h2 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 text-balance">
          Unleash the Power of <span className="text-primary">AI Research</span>
        </h2>

        {/* Subheadline */}
        <p className="text-xl md:text-2xl text-muted-foreground mb-12 max-w-3xl mx-auto text-balance leading-relaxed">
          Your AI-powered research companion—summarizing the latest breakthroughs in AI and software engineering,
          helping students, developers, and scientists stay ahead effortlessly.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button size="lg" className="text-lg px-8 py-6 rounded-xl" asChild>
            <Link href="/explore">
              Explore Papers
              <Search className="ml-2 h-5 w-5" />
            </Link>
          </Button>
          <Button size="lg" variant="outline" className="text-lg px-8 py-6 rounded-xl bg-transparent" asChild>
            <Link href="#latest">
              View Latest
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>

        {/* Tagline */}
        <p className="mt-12 text-sm text-muted-foreground font-medium tracking-wide uppercase">
          Stay Aware. Stay Ahead.
        </p>
      </div>
    </section>
  )
}
