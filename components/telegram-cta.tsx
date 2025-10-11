import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Send } from "lucide-react"

export function TelegramCTA() {
  return (
    <section className="py-24 px-4">
      <div className="container mx-auto">
        <Card className="relative overflow-hidden border-primary/20 bg-gradient-to-br from-card via-card to-primary/5">
          {/* Ambient glow */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-primary/20 rounded-full blur-[100px] opacity-30" />

          <div className="relative z-10 p-12 text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/20 border-2 border-primary mb-6">
              <Send className="h-8 w-8 text-primary" />
            </div>

            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-balance">Never Miss a Breakthrough</h2>

            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto text-balance">
              Get daily digests of the most impactful research papers delivered straight to your Telegram. Stay informed
              without the information overload.
            </p>

            <Button size="lg" className="text-lg px-8 py-6 rounded-xl" asChild>
              <a href="https://t.me/techaware_bot?start=web" target="_blank" rel="noopener noreferrer">
                Subscribe on Telegram
                <Send className="ml-2 h-5 w-5" />
              </a>
            </Button>
          </div>
        </Card>
      </div>
    </section>
  )
}
