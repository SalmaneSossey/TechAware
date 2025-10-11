"use client"

import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Share2, Twitter, Linkedin, Mail, LinkIcon } from "lucide-react"
import { useState } from "react"

interface ShareButtonsProps {
  paper: {
    id: string
    title: string
    arxiv_id: string
  }
}

export function ShareButtons({ paper }: ShareButtonsProps) {
  const [copied, setCopied] = useState(false)

  const url = typeof window !== "undefined" ? `${window.location.origin}/paper/${paper.id}` : ""
  const text = `Check out this research: ${paper.title}`

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(url)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("[v0] Failed to copy:", err)
    }
  }

  const shareLinks = {
    twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`,
    email: `mailto:?subject=${encodeURIComponent(paper.title)}&body=${encodeURIComponent(`${text}\n\n${url}`)}`,
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button size="lg" variant="outline">
          <Share2 className="h-5 w-5 mr-2" />
          Share
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48">
        <DropdownMenuItem asChild>
          <a href={shareLinks.twitter} target="_blank" rel="noopener noreferrer" className="cursor-pointer">
            <Twitter className="h-4 w-4 mr-2" />
            Share on Twitter
          </a>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <a href={shareLinks.linkedin} target="_blank" rel="noopener noreferrer" className="cursor-pointer">
            <Linkedin className="h-4 w-4 mr-2" />
            Share on LinkedIn
          </a>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <a href={shareLinks.email} className="cursor-pointer">
            <Mail className="h-4 w-4 mr-2" />
            Share via Email
          </a>
        </DropdownMenuItem>
        <DropdownMenuItem onClick={handleCopyLink} className="cursor-pointer">
          <LinkIcon className="h-4 w-4 mr-2" />
          {copied ? "Copied!" : "Copy Link"}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
