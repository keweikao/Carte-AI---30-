"use client"

import React from "react"
import { useState } from "react"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import { RatingModal } from "@/components/rating-modal"
import { useRouter } from "next/navigation"

interface Dish {
  name: string
  quantity: number
  price: number
  reason: string
  mention_count: number
}

interface RecommendationResult {
  restaurant: string
  rating: number
  review_count: number
  dishes: Dish[]
  total_price: number
  meal_type: string
  people_count: number
}

export default function ResultPage({ params }: { params: { sessionId: string } }) {
  const { user } = useAuth()
  const router = useRouter()
  const [result, setResult] = useState<RecommendationResult | null>(null)
  const [showRatingModal, setShowRatingModal] = useState(false)
  const [loading, setLoading] = useState(true)

  React.useEffect(() => {
    const fetchResult = async () => {
      try {
        const response = await fetch(`/api/searches/${params.sessionId}`)
        if (response.ok) {
          const data = await response.json()
          setResult(data)
        }
      } catch (error) {
        console.error("Failed to fetch result:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchResult()
  }, [params.sessionId])

  if (loading || !result) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">{result.restaurant}</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          ⭐ {result.rating} 分 • {result.review_count} 則評論
        </p>
      </div>

      {/* Dishes - Card based layout */}
      <div className="mb-8 space-y-4">
        {result.dishes.map((dish, index) => (
          <div
            key={index}
            className="rounded-lg border border-border bg-card p-6 hover:border-primary/30 transition-all hover:shadow-md"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h3 className="text-lg font-semibold text-foreground">{dish.name}</h3>
                  <span className="text-sm text-muted-foreground">× {dish.quantity}</span>
                </div>
                <div className="inline-block bg-accent/10 text-accent px-3 py-1 rounded-full">
                  <p className="text-sm font-medium">
                    {dish.mention_count} 則評論提到「{dish.reason}」
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-semibold text-primary">NT$ {dish.price}</p>
              </div>
            </div>
            <Button
              variant="outline"
              className="mt-3 text-xs border-accent/30 text-accent hover:bg-accent/5 bg-transparent"
              size="sm"
            >
              ↻ 換一道
            </Button>
          </div>
        ))}
      </div>

      {/* Total Budget Summary */}
      <div className="mb-8 rounded-lg border border-primary/20 bg-primary/5 p-6">
        <div className="flex items-center justify-between">
          <span className="font-medium text-foreground">總預算</span>
          <span className="text-2xl font-bold text-primary">NT$ {result.total_price}</span>
        </div>
        <p className="mt-2 text-xs text-muted-foreground">
          {result.people_count} 人 • {result.meal_type === "shared" ? "分食" : "個人套餐"}
        </p>
      </div>

      {/* CTAs */}
      <div className="space-y-3">
        <Button
          className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
          onClick={() => setShowRatingModal(true)}
        >
          ⭐ 評分這個推薦
        </Button>
        <Button
          variant="outline"
          className="w-full border-border text-foreground hover:bg-secondary bg-transparent"
          onClick={() => {
            navigator.clipboard.writeText(result.dishes.map((d) => `${d.name} × ${d.quantity}`).join("\n"))
          }}
        >
          📋 複製清單
        </Button>
        <Button
          variant="outline"
          className="w-full border-border text-foreground hover:bg-secondary bg-transparent"
          onClick={() => router.push("/dashboard/order")}
        >
          ✚ 新增查詢
        </Button>
      </div>

      {/* Modals */}
      <RatingModal isOpen={showRatingModal} onClose={() => setShowRatingModal(false)} sessionId={params.sessionId} />
    </div>
  )
}
