"use client"

import { AlertTriangle, RefreshCw, Wifi, Server, Clock } from "lucide-react"
import Link from "next/link"

type ErrorType = "network" | "server" | "timeout" | "generic"

interface ErrorStateProps {
  type: ErrorType
  onRetry?: () => void
}

const errors = {
  network: {
    icon: Wifi,
    title: "網路連線問題",
    description: "請檢查您的網路連線後再試一次。",
    suggestion: "確認 Wi-Fi 或行動數據已開啟",
  },
  server: {
    icon: Server,
    title: "伺服器忙碌中",
    description: "系統目前較為繁忙，請稍後再試。",
    suggestion: "通常幾分鐘後就會恢復正常",
  },
  timeout: {
    icon: Clock,
    title: "請求逾時",
    description: "分析時間過長，請重新嘗試。",
    suggestion: "可能是餐廳資料較多，需要更多時間",
  },
  generic: {
    icon: AlertTriangle,
    title: "發生錯誤",
    description: "很抱歉，發生了一些問題。請重新嘗試。",
    suggestion: "如果問題持續發生，請聯繫我們",
  },
}

export function ErrorState({ type, onRetry }: ErrorStateProps) {
  const error = errors[type]
  const Icon = error.icon

  return (
    <div className="min-h-screen bg-cream flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Card */}
        <div className="bg-white rounded-[2rem] shadow-floating p-8 text-center">
          {/* Icon */}
          <div className="w-20 h-20 rounded-full bg-terracotta/10 flex items-center justify-center mx-auto mb-6">
            <Icon className="w-10 h-10 text-terracotta" />
          </div>

          {/* Content */}
          <h2 className="font-serif text-2xl text-charcoal mb-2">{error.title}</h2>
          <p className="text-charcoal/60 mb-2">{error.description}</p>
          <p className="text-sm text-charcoal/40 mb-8">{error.suggestion}</p>

          {/* Actions */}
          <div className="flex flex-col gap-3">
            <button
              onClick={onRetry}
              className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 bg-charcoal text-white rounded-full font-medium hover:bg-charcoal/90 transition-all"
            >
              <RefreshCw className="w-4 h-4" />
              重新嘗試
            </button>
            <Link
              href="/"
              className="w-full inline-flex items-center justify-center px-6 py-3 text-charcoal/60 hover:text-charcoal transition-colors"
            >
              返回首頁
            </Link>
          </div>
        </div>

        {/* Help Link */}
        <p className="text-center text-sm text-charcoal/40 mt-6">
          需要協助？
          <a href="mailto:support@carte.tw" className="text-caramel hover:underline ml-1">
            聯繫客服
          </a>
        </p>
      </div>
    </div>
  )
}
