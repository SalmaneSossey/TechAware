import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader } from "@/components/ui/card"

export default function Loading() {
  return (
    <main className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <Skeleton className="h-10 w-32 mb-6" />

        <div className="mb-8">
          <div className="flex gap-3 mb-4">
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-6 w-40" />
          </div>

          <Skeleton className="h-16 w-full mb-6" />
          <Skeleton className="h-6 w-3/4 mb-6" />

          <div className="flex gap-3">
            <Skeleton className="h-12 w-32" />
            <Skeleton className="h-12 w-40" />
            <Skeleton className="h-12 w-32" />
          </div>
        </div>

        <Card className="mb-8">
          <CardHeader>
            <Skeleton className="h-8 w-64" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-24 w-full" />
          </CardContent>
        </Card>

        <Card className="mb-8">
          <CardHeader>
            <Skeleton className="h-8 w-48" />
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-16 w-full" />
            <Skeleton className="h-16 w-full" />
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
