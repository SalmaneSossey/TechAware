import { Github, Twitter, Mail } from "lucide-react"
import Link from "next/link"

export function Footer() {
  return (
    <footer className="border-t py-12 px-4">
      <div className="container mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-primary/20 border-2 border-primary flex items-center justify-center">
                <div className="w-4 h-4 rounded-full bg-primary" />
              </div>
              <span className="font-bold text-lg">TechAware</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Your window to tomorrow's tech. Empowering innovators with distilled research insights.
            </p>
          </div>

          {/* Features */}
          <div>
            <h3 className="font-semibold mb-4">Features</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/explore" className="hover:text-foreground transition-colors">
                  Browse Papers
                </Link>
              </li>
              <li>
                <Link href="/explore" className="hover:text-foreground transition-colors">
                  AI Summaries
                </Link>
              </li>
              <li>
                <Link href="/explore" className="hover:text-foreground transition-colors">
                  Impact Analysis
                </Link>
              </li>
              <li>
                <Link href="#telegram" className="hover:text-foreground transition-colors">
                  Telegram Bot
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-semibold mb-4">Resources</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/about" className="hover:text-foreground transition-colors">
                  About
                </Link>
              </li>
              <li>
                <Link href="/about" className="hover:text-foreground transition-colors">
                  Mission
                </Link>
              </li>
              <li>
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-foreground transition-colors"
                >
                  GitHub
                </a>
              </li>
              <li>
                <a
                  href="https://arxiv.org"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-foreground transition-colors"
                >
                  arXiv
                </a>
              </li>
            </ul>
          </div>

          {/* Connect */}
          <div>
            <h3 className="font-semibold mb-4">Connect</h3>
            <div className="flex gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a
                href="mailto:hello@techaware.ai"
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="pt-8 border-t text-center text-sm text-muted-foreground">
          <p>© {new Date().getFullYear()} TechAware. Built by Eng. Sossey Salmane</p>
        </div>
      </div>
    </footer>
  )
}
