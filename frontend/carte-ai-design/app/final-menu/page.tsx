"use client"

import { useState } from "react"
import Link from "next/link"
import { ArrowLeft, Share2, CheckCircle2, MapPin, Users, Clock, Sparkles, Copy, ExternalLink, Plus } from "lucide-react"

interface Dish {
  id: string
  name: string
  price: number
  servings: string
  quantity: number
}

const selectedDishes: Dish[] = [
  { id: "1", name: "小籠包", price: 220, servings: "2-3人份", quantity: 2 },
  { id: "2", name: "蝦仁炒飯", price: 280, servings: "2-3人份", quantity: 1 },
  { id: "4", name: "蒜泥白肉", price: 260, servings: "2-3人份", quantity: 1 },
]

export default function FinalMenuPage() {
  const [showShareModal, setShowShareModal] = useState(false)
  const [copied, setCopied] = useState(false)

  const partySize = 4
  const restaurantName = "鼎泰豐 (信義店)"
  const totalPrice = selectedDishes.reduce((sum, d) => sum + d.price * d.quantity, 0)
  const pricePerPerson = Math.round(totalPrice / partySize)

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${restaurantName} - 推薦菜單`,
          text: `Carte AI 為 ${partySize} 人推薦的菜單`,
          url: window.location.href,
        })
      } catch {
        setShowShareModal(true)
      }
    } else {
      setShowShareModal(true)
    }
  }

  return (
    <div className="min-h-screen bg-cream">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-cream/80 backdrop-blur-md border-b border-charcoal/5">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link
            href="/recommendation"
            className="flex items-center gap-2 text-charcoal/60 hover:text-charcoal transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="text-sm">修改菜單</span>
          </Link>
          <button
            onClick={handleShare}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-charcoal bg-white rounded-full border border-charcoal/10 hover:border-charcoal/20 transition-all"
          >
            <Share2 className="w-4 h-4" />
            分享
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-32 px-4">
        <div className="max-w-xl mx-auto">
          {/* Success Header */}
          <div className="text-center mb-8">
            <div className="w-16 h-16 rounded-full bg-caramel/10 flex items-center justify-center mx-auto mb-4">
              <CheckCircle2 className="w-8 h-8 text-caramel" />
            </div>
            <h1 className="font-serif text-3xl text-charcoal mb-2">菜單已完成</h1>
            <p className="text-charcoal/60">您可以截圖或分享這份菜單</p>
          </div>

          {/* Menu Card */}
          <div className="bg-white rounded-[2rem] shadow-floating overflow-hidden">
            {/* Restaurant Header */}
            <div className="p-6 border-b border-charcoal/5">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="font-serif text-xl text-charcoal">{restaurantName}</h2>
                  <div className="flex items-center gap-4 mt-2 text-sm text-charcoal/50">
                    <span className="flex items-center gap-1">
                      <Users className="w-4 h-4" />
                      {partySize} 人
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      朋友聚餐
                    </span>
                  </div>
                </div>
                <div className="p-2 bg-caramel/10 rounded-xl">
                  <Sparkles className="w-5 h-5 text-caramel" />
                </div>
              </div>
            </div>

            {/* Dish List */}
            <div className="p-6">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-charcoal/40 mb-4">推薦菜色</h3>
              <div className="space-y-4">
                {selectedDishes.map((dish) => (
                  <div
                    key={dish.id}
                    className="flex items-center justify-between py-3 border-b border-charcoal/5 last:border-0"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-8 h-8 rounded-lg bg-charcoal/5 flex items-center justify-center text-sm font-medium text-charcoal">
                        {dish.quantity}x
                      </div>
                      <div>
                        <p className="font-medium text-charcoal">{dish.name}</p>
                        <p className="text-xs text-charcoal/50">{dish.servings}</p>
                      </div>
                    </div>
                    <span className="font-medium text-charcoal">${dish.price * dish.quantity}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Summary */}
            <div className="p-6 bg-cream">
              <div className="flex items-center justify-between mb-2">
                <span className="text-charcoal/60">總計</span>
                <span className="text-2xl font-semibold text-charcoal">${totalPrice}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-charcoal/50">{partySize} 人用餐</span>
                <span className="text-charcoal/60">約 ${pricePerPerson}/人</span>
              </div>
            </div>

            {/* Footer */}
            <div className="p-4 bg-charcoal/5 text-center">
              <p className="text-xs text-charcoal/40">由 Carte AI 根據評論與偏好推薦</p>
            </div>
          </div>

          {/* Actions */}
          <div className="mt-8 space-y-3">
            <Link
              href="/input"
              className="w-full flex items-center justify-center gap-2 py-4 rounded-full font-semibold text-white gradient-primary shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all"
            >
              <Plus className="w-5 h-5" />
              規劃下一餐
            </Link>
            <a
              href={`https://www.google.com/maps/search/${encodeURIComponent(restaurantName)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full flex items-center justify-center gap-2 py-4 rounded-full font-medium text-charcoal bg-white border-2 border-charcoal/10 hover:border-charcoal/20 transition-all"
            >
              <MapPin className="w-5 h-5" />在 Google Maps 開啟
              <ExternalLink className="w-4 h-4 text-charcoal/40" />
            </a>
          </div>

          {/* AI Attribution */}
          <div className="mt-8 p-4 bg-caramel/5 rounded-xl">
            <div className="flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-caramel flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm text-charcoal/70 leading-relaxed">
                  這份菜單是根據 328 則 Google 評論、您的 {partySize} 人用餐需求、
                  以及「朋友聚餐」場合精心推薦。祝您用餐愉快！
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Share Modal */}
      {showShareModal && (
        <div className="fixed inset-0 z-50 bg-charcoal/50 backdrop-blur-sm flex items-end sm:items-center justify-center p-4">
          <div className="w-full max-w-md bg-white rounded-t-[2rem] sm:rounded-[2rem] p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-serif text-xl text-charcoal">分享菜單</h3>
              <button
                onClick={() => setShowShareModal(false)}
                className="p-2 text-charcoal/40 hover:text-charcoal transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
            </div>

            {/* Share Options */}
            <div className="space-y-3">
              <button
                onClick={handleCopyLink}
                className="w-full flex items-center gap-4 p-4 bg-charcoal/5 rounded-xl hover:bg-charcoal/10 transition-colors"
              >
                <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center">
                  <Copy className="w-5 h-5 text-charcoal" />
                </div>
                <div className="text-left flex-1">
                  <p className="font-medium text-charcoal">複製連結</p>
                  <p className="text-xs text-charcoal/50">分享此頁面連結</p>
                </div>
                {copied && <span className="text-xs text-caramel font-medium">已複製！</span>}
              </button>

              <a
                href={`https://line.me/R/share?text=${encodeURIComponent(`${restaurantName} 推薦菜單 - Carte AI`)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full flex items-center gap-4 p-4 bg-[#06C755]/10 rounded-xl hover:bg-[#06C755]/20 transition-colors"
              >
                <div className="w-10 h-10 rounded-full bg-[#06C755] flex items-center justify-center">
                  <span className="text-white font-bold text-sm">LINE</span>
                </div>
                <div className="text-left">
                  <p className="font-medium text-charcoal">分享到 LINE</p>
                  <p className="text-xs text-charcoal/50">傳送給朋友</p>
                </div>
              </a>
            </div>

            <button
              onClick={() => setShowShareModal(false)}
              className="w-full mt-6 py-3 text-charcoal/60 hover:text-charcoal transition-colors"
            >
              取消
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
