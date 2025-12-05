"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { ArrowLeft, SlidersHorizontal } from "lucide-react"
import { DishCard } from "@/components/carte/dish-card"
import { MenuSummary } from "@/components/carte/menu-summary"

interface Dish {
  id: string
  name: string
  price: number
  servings: string
  rating: number
  reviewCount: number
  aiReason: string
  tags: string[]
  imageQuery: string
}

const mockDishes: Dish[] = [
  {
    id: "1",
    name: "小籠包",
    price: 220,
    servings: "2-3人份",
    rating: 4.9,
    reviewCount: 1203,
    aiReason: "鼎泰豐招牌必點！皮薄餡多，湯汁鮮美。評論中有 89% 的顧客推薦作為聚餐首選。",
    tags: ["招牌", "必點", "蒸籠"],
    imageQuery: "xiaolongbao steamed dumplings",
  },
  {
    id: "2",
    name: "蝦仁炒飯",
    price: 280,
    servings: "2-3人份",
    rating: 4.7,
    reviewCount: 856,
    aiReason: "米飯粒粒分明，蝦仁新鮮彈牙。多位評論提到份量適合 2-3 人分享。",
    tags: ["主食", "分享", "人氣"],
    imageQuery: "shrimp fried rice chinese",
  },
  {
    id: "3",
    name: "紅燒牛肉麵",
    price: 320,
    servings: "1人份",
    rating: 4.8,
    reviewCount: 672,
    aiReason: "湯頭濃郁不膩，牛肉軟嫩入味。適合喜歡重口味的朋友。",
    tags: ["湯品", "牛肉", "經典"],
    imageQuery: "taiwanese beef noodle soup",
  },
  {
    id: "4",
    name: "蒜泥白肉",
    price: 260,
    servings: "2-3人份",
    rating: 4.6,
    reviewCount: 445,
    aiReason: "肉片薄切，蒜味香濃。清爽開胃，很適合配飯或作為前菜。",
    tags: ["前菜", "開胃", "豬肉"],
    imageQuery: "garlic pork slices chinese cold dish",
  },
  {
    id: "5",
    name: "酸辣湯",
    price: 180,
    servings: "2-3人份",
    rating: 4.5,
    reviewCount: 389,
    aiReason: "酸辣適中，配料豐富。評論提到這道湯品可以平衡其他重口味菜色。",
    tags: ["湯品", "酸辣", "暖胃"],
    imageQuery: "hot and sour soup chinese",
  },
  {
    id: "6",
    name: "清炒時蔬",
    price: 160,
    servings: "2-3人份",
    rating: 4.4,
    reviewCount: 234,
    aiReason: "新鮮蔬菜清炒，清爽解膩。建議搭配其他肉類菜色一起點。",
    tags: ["蔬菜", "清淡", "健康"],
    imageQuery: "stir fried vegetables chinese",
  },
]

export default function RecommendationPage() {
  const router = useRouter()
  const [selectedIds, setSelectedIds] = useState<string[]>(["1", "2", "4"])
  const partySize = 4 // Would come from previous form

  const selectedDishes = mockDishes.filter((d) => selectedIds.includes(d.id))

  const handleToggle = (id: string) => {
    setSelectedIds((prev) => (prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]))
  }

  const handleReplace = (id: string) => {
    // In real app, this would fetch alternative dishes
    console.log("Replace dish:", id)
  }

  const handleConfirm = () => {
    router.push("/final-menu")
  }

  const handleAddMore = () => {
    // Scroll to dish list or show modal
    window.scrollTo({ top: 400, behavior: "smooth" })
  }

  return (
    <div className="min-h-screen bg-cream">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-cream/80 backdrop-blur-md border-b border-charcoal/5">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link
            href="/input"
            className="flex items-center gap-2 text-charcoal/60 hover:text-charcoal transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="text-sm">重新選擇</span>
          </Link>
          <div className="text-center">
            <p className="font-serif text-lg text-charcoal">鼎泰豐 (信義店)</p>
            <p className="text-xs text-charcoal/50">{partySize} 人用餐 · 朋友聚餐</p>
          </div>
          <button className="flex items-center gap-2 px-3 py-1.5 text-sm text-charcoal/60 hover:text-charcoal hover:bg-charcoal/5 rounded-full transition-all">
            <SlidersHorizontal className="w-4 h-4" />
            <span className="hidden sm:inline">篩選</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-8 px-4">
        <div className="max-w-6xl mx-auto">
          {/* Page Title */}
          <div className="mb-8">
            <h1 className="font-serif text-3xl md:text-4xl text-charcoal mb-2">為您推薦</h1>
            <p className="text-charcoal/60">根據您的偏好與 328 則評論精選，點選加入菜單</p>
          </div>

          {/* Content Grid */}
          <div className="flex flex-col lg:flex-row gap-8">
            {/* Dish Grid */}
            <div className="flex-1">
              {/* Category Tabs */}
              <div className="flex items-center gap-2 mb-6 overflow-x-auto pb-2">
                <button className="px-4 py-2 text-sm font-medium text-white bg-charcoal rounded-full whitespace-nowrap">
                  全部推薦
                </button>
                <button className="px-4 py-2 text-sm text-charcoal/60 hover:text-charcoal bg-white rounded-full border border-charcoal/10 whitespace-nowrap">
                  招牌必點
                </button>
                <button className="px-4 py-2 text-sm text-charcoal/60 hover:text-charcoal bg-white rounded-full border border-charcoal/10 whitespace-nowrap">
                  主食
                </button>
                <button className="px-4 py-2 text-sm text-charcoal/60 hover:text-charcoal bg-white rounded-full border border-charcoal/10 whitespace-nowrap">
                  湯品
                </button>
                <button className="px-4 py-2 text-sm text-charcoal/60 hover:text-charcoal bg-white rounded-full border border-charcoal/10 whitespace-nowrap">
                  蔬菜
                </button>
              </div>

              {/* Dish Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {mockDishes.map((dish) => (
                  <DishCard
                    key={dish.id}
                    dish={dish}
                    isSelected={selectedIds.includes(dish.id)}
                    onToggle={() => handleToggle(dish.id)}
                    onReplace={() => handleReplace(dish.id)}
                  />
                ))}
              </div>
            </div>

            {/* Sidebar - Desktop */}
            <div className="hidden lg:block w-80">
              <MenuSummary
                dishes={selectedDishes}
                partySize={partySize}
                onConfirm={handleConfirm}
                onAddMore={handleAddMore}
              />
            </div>
          </div>
        </div>
      </main>

      {/* Mobile Bottom Bar */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-md border-t border-charcoal/10 p-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-charcoal">{selectedDishes.length} 道菜</p>
            <p className="text-xs text-charcoal/50">
              ${selectedDishes.reduce((sum, d) => sum + d.price, 0)} · 約 $
              {Math.round(selectedDishes.reduce((sum, d) => sum + d.price, 0) / partySize)}/人
            </p>
          </div>
          <button
            onClick={handleConfirm}
            disabled={selectedDishes.length === 0}
            className={`
              px-6 py-3 rounded-full font-semibold transition-all
              ${selectedDishes.length > 0 ? "gradient-primary text-white" : "bg-charcoal/10 text-charcoal/30"}
            `}
          >
            確認菜單
          </button>
        </div>
      </div>
    </div>
  )
}
