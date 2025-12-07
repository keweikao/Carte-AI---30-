"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

interface AnalysisStep {
  name: string
  progress: number
  status: "pending" | "loading" | "complete"
}

export default function AnalyzingPage({ params }: { params: { sessionId: string } }) {
  const router = useRouter()
  const [steps, setSteps] = useState<AnalysisStep[]>([
    { name: "爬梳 Google 評論", progress: 0, status: "loading" },
    { name: "分析食記", progress: 0, status: "pending" },
    { name: "計算最佳組合", progress: 0, status: "pending" },
  ])

  useEffect(() => {
    // Simulate progress
    const interval = setInterval(() => {
      setSteps((prev) => {
        const newSteps = [...prev]
        let allComplete = false

        for (let i = 0; i < newSteps.length; i++) {
          if (newSteps[i].status === "loading") {
            newSteps[i].progress += Math.random() * 30
            if (newSteps[i].progress >= 100) {
              newSteps[i].progress = 100
              newSteps[i].status = "complete"
              if (i + 1 < newSteps.length) {
                newSteps[i + 1].status = "loading"
              }
            }
            break
          }
        }

        if (newSteps.every((s) => s.status === "complete")) {
          allComplete = true
        }

        return newSteps
      })
    }, 500)

    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (steps.every((s) => s.status === "complete")) {
      setTimeout(() => {
        router.push(`/dashboard/result/${params.sessionId}`)
      }, 1000)
    }
  }, [steps, params.sessionId, router])

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="w-full max-w-md px-4 text-center">
        <div className="mb-8">
          <div className="text-5xl">🔍</div>
        </div>
        <h2 className="mb-2 text-2xl font-semibold text-foreground">正在分析推薦...</h2>
        <p className="mb-8 text-muted-foreground">AI 正在為你尋找最適合的菜色</p>

        <div className="space-y-4">
          {steps.map((step, index) => (
            <div key={index} className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-foreground">{step.name}</span>
                <span className="text-xs text-muted-foreground">{Math.round(step.progress)}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-secondary">
                <div className="h-full bg-primary transition-all duration-300" style={{ width: `${step.progress}%` }} />
              </div>
            </div>
          ))}
        </div>

        <p className="mt-8 text-xs text-muted-foreground">預計 3-5 秒完成</p>
      </div>
    </div>
  )
}
