"use client"

import { Search, UtensilsCrossed, MessageSquare } from "lucide-react"
import Link from "next/link"

type EmptyStateType = "no-results" | "no-reviews" | "no-menu" | "no-selection"

interface EmptyStateProps {
  type: EmptyStateType
  restaurantName?: string
  onRetry?: () => void
}

const states = {
  "no-results": {
    icon: Search,
    title: "找不到餐廳",
    description: "我們找不到符合的餐廳，請試試其他關鍵字或確認餐廳名稱是否正確。",
    action: "重新搜尋",
    actionType: "link" as const,
    actionHref: "/input",
  },
  "no-reviews": {
    icon: MessageSquare,
    title: "評論資料不足",
    description: "這間餐廳的評論數量較少，AI 可能無法提供最準確的推薦。您可以繼續，或選擇其他餐廳。",
    action: "仍要繼續",
    actionType: "button" as const,
  },
  "no-menu": {
    icon: UtensilsCrossed,
    title: "無法取得菜單",
    description: "很抱歉，我們目前無法取得這間餐廳的菜單資料。請稍後再試或選擇其他餐廳。",
    action: "選擇其他餐廳",
    actionType: "link" as const,
    actionHref: "/input",
  },
  "no-selection": {
    icon: UtensilsCrossed,
    title: "尚未選擇菜色",
    description: "您還沒有選擇任何菜色。瀏覽下方推薦，點選加入您的菜單。",
    action: "查看推薦",
    actionType: "button" as const,
  },
}

export function EmptyState({ type, restaurantName, onRetry }: EmptyStateProps) {
  const state = states[type]
  const Icon = state.icon

  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      {/* Icon */}
      <div className="w-20 h-20 rounded-full bg-charcoal/5 flex items-center justify-center mb-6">
        <Icon className="w-10 h-10 text-charcoal/30" />
      </div>

      {/* Content */}
      <h3 className="font-serif text-xl text-charcoal mb-2">{state.title}</h3>
      {restaurantName && <p className="text-sm text-caramel mb-2">{restaurantName}</p>}
      <p className="text-charcoal/60 max-w-md mb-8">{state.description}</p>

      {/* Action */}
      {state.actionType === "link" ? (
        <Link
          href={state.actionHref || "/"}
          className="inline-flex items-center gap-2 px-6 py-3 bg-charcoal text-white rounded-full font-medium hover:bg-charcoal/90 transition-all"
        >
          {state.action}
        </Link>
      ) : (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-6 py-3 bg-charcoal text-white rounded-full font-medium hover:bg-charcoal/90 transition-all"
        >
          {state.action}
        </button>
      )}
    </div>
  )
}
