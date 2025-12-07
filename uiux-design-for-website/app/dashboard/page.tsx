"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/lib/auth-context"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"

export default function DashboardPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (mounted && !loading && !user) {
      router.push("/")
    }
  }, [user, loading, mounted, router])

  if (loading || !mounted) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-12">
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-foreground text-balance">不知道點什麼？</h1>
          <p className="mt-2 text-muted-foreground">用 Carte 讓 AI 為你決定</p>
        </div>

        {/* Main CTA */}
        <div className="rounded-lg border border-border bg-card p-12 text-center">
          <div className="mb-6 text-6xl">🍽️</div>
          <h2 className="mb-4 text-3xl font-bold text-foreground">開始新的查詢</h2>
          <p className="mb-8 text-lg text-muted-foreground">選擇餐廳、設定偏好，讓 AI 為你推薦最適合的菜色</p>
          <Button
            size="lg"
            className="bg-primary text-primary-foreground hover:bg-primary/90"
            onClick={() => router.push("/dashboard/order")}
          >
            開始查詢
          </Button>
        </div>
      </div>
    </div>
  )
}
