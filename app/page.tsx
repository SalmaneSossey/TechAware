import { Hero } from "@/components/hero"
import { LatestPapers } from "@/components/latest-papers"
import { TelegramCTA } from "@/components/telegram-cta"
import { Footer } from "@/components/footer"

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <Hero />
      <LatestPapers />
      <TelegramCTA />
      <Footer />
    </main>
  )
}
