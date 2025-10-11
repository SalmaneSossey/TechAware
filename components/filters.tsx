"use client"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { X } from "lucide-react"
import { useState } from "react"

const categories = [
  "All Categories",
  "Machine Learning",
  "Computer Vision",
  "Natural Language Processing",
  "Robotics",
  "Privacy & Security",
  "Data Science",
]

const tags = [
  "LLM",
  "Attention",
  "Efficiency",
  "Federated Learning",
  "Privacy",
  "Computer Vision",
  "Edge Computing",
  "Real-Time",
]

export function Filters() {
  const [selectedCategory, setSelectedCategory] = useState("All Categories")
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [sortBy, setSortBy] = useState("recent")

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) => (prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]))
  }

  const clearFilters = () => {
    setSelectedCategory("All Categories")
    setSelectedTags([])
    setSortBy("recent")
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-4">
        {/* Category */}
        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            {categories.map((category) => (
              <SelectItem key={category} value={category}>
                {category}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Sort */}
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="recent">Most Recent</SelectItem>
            <SelectItem value="relevant">Most Relevant</SelectItem>
            <SelectItem value="cited">Most Cited</SelectItem>
          </SelectContent>
        </Select>

        {/* Clear filters */}
        {(selectedCategory !== "All Categories" || selectedTags.length > 0 || sortBy !== "recent") && (
          <Button variant="ghost" size="sm" onClick={clearFilters}>
            <X className="h-4 w-4 mr-2" />
            Clear Filters
          </Button>
        )}
      </div>

      {/* Tags */}
      <div className="space-y-2">
        <p className="text-sm font-medium text-muted-foreground">Filter by tags:</p>
        <div className="flex flex-wrap gap-2">
          {tags.map((tag) => (
            <Badge
              key={tag}
              variant={selectedTags.includes(tag) ? "default" : "outline"}
              className="cursor-pointer hover:bg-primary/80 transition-colors"
              onClick={() => toggleTag(tag)}
            >
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      {/* Active filters */}
      {selectedTags.length > 0 && (
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span>Active filters:</span>
          {selectedTags.map((tag) => (
            <Badge key={tag} variant="secondary" className="gap-1">
              {tag}
              <X className="h-3 w-3 cursor-pointer hover:text-foreground" onClick={() => toggleTag(tag)} />
            </Badge>
          ))}
        </div>
      )}
    </div>
  )
}
