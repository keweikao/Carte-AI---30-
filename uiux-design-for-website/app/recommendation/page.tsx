"use client"

import { useState, useEffect } from "react"
import Header from "@/components/header"
import { Check } from "lucide-react"

export default function RecommendationPage() {
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState("analyzing")

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          setStatus("complete")
          return 100
        }
        return prev + Math.random() * 30
      })
    }, 500)

    return () => clearInterval(interval)
  }, [])

  const analysisSteps = [
    { label: "鎖定海底撈的人氣菜色", completed: progress > 30 },
    { label: "過濾：不吃豬", completed: progress > 60 },
    { label: "為 2 人量配餐", completed: progress > 80 },
    { label: "計算最佳 CP 值組合", completed: progress > 90 },
  ]

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header title="正在生成推薦" />

      <main className="flex-1 p-6 max-w-2xl mx-auto w-full flex flex-col justify-center items-center">
        {status === "analyzing" ? (
          <>
            {/* Loading Indicator */}
            <div className="mb-8">
              <div className="w-24 h-24 rounded-full border-4 border-border border-t-primary animate-spin flex items-center justify-center">
                <span className="text-3xl">⚜️</span>
              </div>
            </div>

            <h1 className="text-3xl font-bold text-foreground text-center mb-2">正在爬梳 132 則 Google 評論...</h1>
            <p className="text-muted-foreground text-center mb-8">AI 正在分析 海底撈 的老餐推薦關鍵字</p>

            {/* Analysis Steps */}
            <div className="w-full space-y-3 mb-8">
              {analysisSteps.map((step) => (
                <div
                  key={step.label}
                  className={`flex items-center gap-3 p-3 rounded-lg ${
                    step.completed ? "bg-primary/10 border border-primary/30" : "bg-secondary border border-border"
                  }`}
                >
                  <div
                    className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 ${
                      step.completed ? "bg-primary text-primary-foreground" : "bg-muted"
                    }`}
                  >
                    {step.completed && <Check className="w-4 h-4" />}
                  </div>
                  <span
                    className={`text-sm font-medium ${step.completed ? "text-foreground" : "text-muted-foreground"}`}
                  >
                    {step.label}
                  </span>
                </div>
              ))}
            </div>

            {/* Progress Bar */}
            <div className="w-full">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs text-muted-foreground">進度</span>
                <span className="text-sm font-semibold text-foreground">{Math.round(progress)}%</span>
              </div>
              <div className="h-2 bg-secondary rounded-full overflow-hidden">
                <div className="h-full bg-primary transition-all duration-300" style={{ width: `${progress}%` }} />
              </div>
            </div>
          </>
        ) : (
          <>
            {/* Completed State */}
            <div className="mb-8">
              <div className="w-24 h-24 rounded-full bg-primary/10 border-4 border-primary flex items-center justify-center">
                <Check className="w-12 h-12 text-primary" />
              </div>
            </div>

            <h1 className="text-3xl font-bold text-foreground text-center mb-4">推薦完成</h1>
            <p className="text-muted-foreground text-center">我們已為你精選最適合的菜色組合</p>
          </>
        )}
      </main>
    </div>
  )
}
