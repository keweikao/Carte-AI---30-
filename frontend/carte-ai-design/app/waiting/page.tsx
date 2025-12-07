"use client"

import { useEffect, useState, startTransition } from "react"
import { useRouter } from "next/navigation"
import { Search, Filter, ChefHat } from "lucide-react"

interface StreamMessage {
  id: number
  text: string
  phase: "perception" | "filtering" | "decision"
}

const streamMessages: StreamMessage[] = [
  { id: 1, text: "正在搜尋餐廳菜單...", phase: "perception" },
  { id: 2, text: "讀取 Google 評論資料...", phase: "perception" },
  { id: 3, text: "分析 328 則評論...", phase: "perception" },
  { id: 4, text: "識別招牌菜與隱藏美食...", phase: "perception" },
  { id: 5, text: "根據人數計算份量...", phase: "filtering" },
  { id: 6, text: "移除不符合飲食偏好的菜色...", phase: "filtering" },
  { id: 7, text: "篩選適合聚餐的菜色...", phase: "filtering" },
  { id: 8, text: "平衡口味與價格...", phase: "decision" },
  { id: 9, text: "生成個人化推薦菜單...", phase: "decision" },
  { id: 10, text: "完成!準備呈現您的推薦...", phase: "decision" },
]

const phases = [
  { id: "perception", label: "探索中", icon: Search, color: "caramel" },
  { id: "filtering", label: "篩選中", icon: Filter, color: "terracotta" },
  { id: "decision", label: "生成中", icon: ChefHat, color: "charcoal" },
]

export default function WaitingPage() {
  const router = useRouter()
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0)
  const [displayedMessages, setDisplayedMessages] = useState<StreamMessage[]>([])
  const [progress, setProgress] = useState(0)
  const [currentPhase, setCurrentPhase] = useState<"perception" | "filtering" | "decision">("perception")

  useEffect(() => {
    const messageInterval = setInterval(() => {
      setCurrentMessageIndex((prev) => {
        const next = prev + 1
        if (next >= streamMessages.length) {
          clearInterval(messageInterval)
          // Navigate to recommendation page after completion
          setTimeout(() => router.push("/recommendation"), 1000)
          return prev
        }
        return next
      })
    }, 800)

    return () => clearInterval(messageInterval)
  }, [router])

  useEffect(() => {
    if (currentMessageIndex < streamMessages.length) {
      const message = streamMessages[currentMessageIndex]
      // Batch state updates using startTransition to avoid cascading renders
      startTransition(() => {
        setDisplayedMessages((prev) => [...prev.slice(-4), message])
        setCurrentPhase(message.phase)
        setProgress(((currentMessageIndex + 1) / streamMessages.length) * 100)
      })
    }
  }, [currentMessageIndex])

  const getPhaseColor = (phase: string, type: "bg" | "text" | "border") => {
    const colors = {
      perception: { bg: "bg-caramel", text: "text-caramel", border: "border-caramel" },
      filtering: { bg: "bg-terracotta", text: "text-terracotta", border: "border-terracotta" },
      decision: { bg: "bg-charcoal", text: "text-charcoal", border: "border-charcoal" },
    }
    return colors[phase as keyof typeof colors]?.[type] || colors.perception[type]
  }

  const currentPhaseData = phases.find((p) => p.id === currentPhase)
  const PhaseIcon = currentPhaseData?.icon || Search

  return (
    <div className="min-h-screen bg-cream flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-12">
          <span className="font-serif text-3xl text-charcoal">Carte</span>
          <span className="ml-2 text-sm text-caramel">AI</span>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-[2rem] shadow-floating p-8">
          {/* Phase Icon */}
          <div className="flex justify-center mb-8">
            <div
              className={`
              w-20 h-20 rounded-full flex items-center justify-center
              ${getPhaseColor(currentPhase, "bg")} 
              transition-colors duration-500
              animate-pulse
            `}
            >
              <PhaseIcon className="w-10 h-10 text-white" />
            </div>
          </div>

          {/* Phase Label */}
          <div className="text-center mb-6">
            <h2
              className={`
              font-serif text-2xl transition-colors duration-500
              ${getPhaseColor(currentPhase, "text")}
            `}
            >
              {currentPhaseData?.label}
            </h2>
            <p className="text-sm text-charcoal/50 mt-2">AI 正在為您分析最佳菜色組合</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="h-2 bg-charcoal/5 rounded-full overflow-hidden">
              <div
                className={`
                  h-full rounded-full transition-all duration-500 ease-out
                  ${getPhaseColor(currentPhase, "bg")}
                `}
                style={{ width: `${progress}%` }}
              />
            </div>
            <div className="flex justify-between mt-2 text-xs text-charcoal/40">
              <span>分析中...</span>
              <span>{Math.round(progress)}%</span>
            </div>
          </div>

          {/* Phase Indicators */}
          <div className="flex justify-center gap-4 mb-8">
            {phases.map((phase, index) => {
              const isActive = phase.id === currentPhase
              const isPast = phases.findIndex((p) => p.id === currentPhase) > index
              const Icon = phase.icon

              return (
                <div key={phase.id} className="flex flex-col items-center gap-2">
                  <div
                    className={`
                    w-10 h-10 rounded-full flex items-center justify-center
                    transition-all duration-300
                    ${isPast
                        ? "bg-charcoal text-white"
                        : isActive
                          ? `${getPhaseColor(phase.id, "bg")} text-white scale-110`
                          : "bg-charcoal/10 text-charcoal/30"
                      }
                  `}
                  >
                    {isPast ? (
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      <Icon className="w-5 h-5" />
                    )}
                  </div>
                  <span
                    className={`
                    text-xs transition-colors
                    ${isActive ? getPhaseColor(phase.id, "text") : "text-charcoal/40"}
                  `}
                  >
                    {phase.label}
                  </span>
                </div>
              )
            })}
          </div>

          {/* Message Stream */}
          <div className="space-y-2 min-h-[120px]">
            {displayedMessages.map((message, index) => {
              const isLatest = index === displayedMessages.length - 1
              return (
                <div
                  key={message.id}
                  className={`
                    flex items-center gap-3 p-3 rounded-xl transition-all duration-300
                    ${isLatest
                      ? `${getPhaseColor(message.phase, "bg")}/10 ${getPhaseColor(message.phase, "border")} border`
                      : "opacity-40"
                    }
                  `}
                >
                  <div
                    className={`
                    w-2 h-2 rounded-full flex-shrink-0
                    ${isLatest ? getPhaseColor(message.phase, "bg") : "bg-charcoal/20"}
                    ${isLatest ? "animate-pulse" : ""}
                  `}
                  />
                  <span
                    className={`
                    text-sm
                    ${isLatest ? getPhaseColor(message.phase, "text") : "text-charcoal/40"}
                  `}
                  >
                    {message.text}
                  </span>
                </div>
              )
            })}
          </div>
        </div>

        {/* Footer Text */}
        <p className="text-center text-xs text-charcoal/40 mt-8">通常需要 10-15 秒完成分析</p>
      </div>
    </div>
  )
}
