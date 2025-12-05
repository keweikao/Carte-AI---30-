"use client"

import { Users, Sparkles, Receipt } from "lucide-react"

interface Dish {
  id: string
  name: string
  price: number
  servings: string
}

interface MenuSummaryProps {
  dishes: Dish[]
  partySize: number
  onConfirm: () => void
  onAddMore: () => void
}

export function MenuSummary({ dishes, partySize, onConfirm, onAddMore }: MenuSummaryProps) {
  const totalPrice = dishes.reduce((sum, dish) => sum + dish.price, 0)
  const pricePerPerson = Math.round(totalPrice / partySize)

  return (
    <div className="bg-white rounded-2xl shadow-floating p-6 sticky top-24">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-serif text-xl text-charcoal">您的菜單</h3>
        <span className="text-sm text-charcoal/50">{dishes.length} 道菜</span>
      </div>

      {/* Dish List */}
      {dishes.length > 0 ? (
        <div className="space-y-3 mb-6 max-h-[300px] overflow-y-auto">
          {dishes.map((dish) => (
            <div
              key={dish.id}
              className="flex items-center justify-between py-2 border-b border-charcoal/5 last:border-0"
            >
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-charcoal truncate">{dish.name}</p>
                <p className="text-xs text-charcoal/50">{dish.servings}</p>
              </div>
              <span className="text-sm font-medium text-charcoal ml-3">${dish.price}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="py-8 text-center">
          <Receipt className="w-12 h-12 text-charcoal/20 mx-auto mb-3" />
          <p className="text-sm text-charcoal/50">尚未選擇菜色</p>
          <p className="text-xs text-charcoal/30 mt-1">點選下方菜色加入菜單</p>
        </div>
      )}

      {/* Summary */}
      {dishes.length > 0 && (
        <div className="p-4 bg-cream rounded-xl mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-charcoal/60">總計</span>
            <span className="text-lg font-semibold text-charcoal">${totalPrice}</span>
          </div>
          <div className="flex justify-between items-center text-sm">
            <span className="flex items-center gap-1 text-charcoal/50">
              <Users className="w-3.5 h-3.5" />
              {partySize} 人
            </span>
            <span className="text-charcoal/60">約 ${pricePerPerson}/人</span>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="space-y-3">
        <button
          onClick={onConfirm}
          disabled={dishes.length === 0}
          className={`
            w-full py-3.5 rounded-full font-semibold transition-all
            flex items-center justify-center gap-2
            ${
              dishes.length > 0
                ? "gradient-primary text-white shadow-lg hover:shadow-xl hover:scale-[1.02]"
                : "bg-charcoal/10 text-charcoal/30 cursor-not-allowed"
            }
          `}
        >
          <Sparkles className="w-4 h-4" />
          確認菜單
        </button>
        <button
          onClick={onAddMore}
          className="w-full py-3 rounded-full text-sm font-medium text-charcoal/60 
            hover:text-charcoal hover:bg-charcoal/5 transition-all"
        >
          想再加點別的
        </button>
      </div>

      {/* AI Tip */}
      <div className="mt-6 p-3 bg-caramel/5 rounded-xl">
        <div className="flex items-start gap-2">
          <Sparkles className="w-4 h-4 text-caramel flex-shrink-0 mt-0.5" />
          <p className="text-xs text-charcoal/60 leading-relaxed">
            AI 已根據 {partySize} 人份量、口味平衡與評論熱度為您精選這些菜色
          </p>
        </div>
      </div>
    </div>
  )
}
