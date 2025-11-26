"use client"

import { useSearchParams } from "next/navigation"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"

export default function JoinPage() {
  const searchParams = useSearchParams()
  const referralCode = searchParams.get("ref")
  const { user, login, loading } = useAuth()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  // If user is logged in, claim the referral
  if (user && referralCode) {
    // Auto-claim referral
    fetch("/api/referrals/claim", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ referral_code: referralCode, user_id: user.id }),
    }).catch(console.error)
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-background to-primary/5">
      <div className="w-full max-w-md px-4 text-center">
        <div className="mb-8">
          <div className="text-6xl">🍽️</div>
        </div>

        <h1 className="mb-2 text-3xl font-bold text-foreground">Carte</h1>
        <p className="mb-6 text-muted-foreground">{referralCode ? "朋友邀請了你加入 Carte" : "一起用 AI 決定吃什麼"}</p>

        <div className="mb-6 space-y-3 rounded-lg border border-border bg-card p-6">
          <h2 className="font-semibold text-foreground">核心優勢</h2>
          <ul className="space-y-2 text-left text-sm text-muted-foreground">
            <li className="flex items-center gap-2">
              <span className="text-primary">✓</span> 分析 Google 評論尋找人氣菜色
            </li>
            <li className="flex items-center gap-2">
              <span className="text-primary">✓</span> 符合你的預算和飲食偏好
            </li>
            <li className="flex items-center gap-2">
              <span className="text-primary">✓</span> 30 秒快速決定吃什麼
            </li>
          </ul>
        </div>

        {referralCode && (
          <div className="mb-6 rounded-lg border border-primary/30 bg-primary/5 p-4">
            <p className="text-sm font-medium text-foreground">邀請獎勵：完成註冊後獲得 +1 搜尋次數！</p>
          </div>
        )}

        {!user ? (
          <Button
            className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
            onClick={login}
            disabled={loading}
          >
            {loading ? "載入中..." : "用 Google 登入"}
          </Button>
        ) : (
          <div className="space-y-2">
            <p className="text-sm text-foreground">歡迎回來，{user.name}！</p>
            <Button
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
              onClick={() => (window.location.href = "/dashboard")}
            >
              進入 Carte
            </Button>
          </div>
        )}

        <p className="mt-6 text-xs text-muted-foreground">• 免費使用 • 邀請朋友獲得更多搜尋次數 • 無廣告</p>
      </div>
    </div>
  )
}
