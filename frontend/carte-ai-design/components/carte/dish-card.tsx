"use client"

import { useState } from "react"
import { Star, RefreshCw, Users, Sparkles, ChevronDown, ChevronUp } from "lucide-react"

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

interface DishCardProps {
  dish: Dish
  isSelected: boolean
  onToggle: () => void
  onReplace: () => void
}

export function DishCard({ dish, isSelected, onToggle, onReplace }: DishCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div
      className={`
      relative bg-white rounded-2xl overflow-hidden transition-all duration-300
      ${isSelected ? "ring-2 ring-charcoal shadow-lg" : "border border-charcoal/10 hover:shadow-md"}
    `}
    >
      {/* Image Section */}
      <div className="relative h-40 bg-charcoal/5">
        <img
          src={`/.jpg?height=160&width=400&query=${dish.imageQuery}`}
          alt={dish.name}
          className="w-full h-full object-cover"
        />

        {/* Rating Badge */}
        <div className="absolute top-3 right-3 flex items-center gap-1 px-2 py-1 bg-white/90 backdrop-blur-sm rounded-full">
          <Star className="w-3.5 h-3.5 fill-caramel text-caramel" />
          <span className="text-xs font-medium text-charcoal">{dish.rating}</span>
        </div>

        {/* Selection Indicator */}
        {isSelected && (
          <div className="absolute top-3 left-3 w-6 h-6 bg-charcoal rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between mb-2">
          <div>
            <h3 className="font-medium text-charcoal text-lg">{dish.name}</h3>
            <div className="flex items-center gap-3 mt-1 text-sm text-charcoal/60">
              <span className="font-medium text-caramel">${dish.price}</span>
              <span className="flex items-center gap-1">
                <Users className="w-3.5 h-3.5" />
                {dish.servings}
              </span>
            </div>
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-1.5 mb-3">
          {dish.tags.slice(0, 3).map((tag) => (
            <span key={tag} className="px-2 py-0.5 text-xs bg-terracotta/10 text-terracotta rounded-full">
              {tag}
            </span>
          ))}
        </div>

        {/* AI Reason */}
        <div
          className={`
          p-3 bg-caramel/5 rounded-xl transition-all
          ${isExpanded ? "" : "line-clamp-2"}
        `}
        >
          <div className="flex items-start gap-2">
            <Sparkles className="w-4 h-4 text-caramel flex-shrink-0 mt-0.5" />
            <p className="text-sm text-charcoal/70 leading-relaxed">{dish.aiReason}</p>
          </div>
        </div>

        {dish.aiReason.length > 80 && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-1 mt-2 text-xs text-charcoal/50 hover:text-charcoal transition-colors"
          >
            {isExpanded ? (
              <>
                收起 <ChevronUp className="w-3 h-3" />
              </>
            ) : (
              <>
                展開 <ChevronDown className="w-3 h-3" />
              </>
            )}
          </button>
        )}

        {/* Actions */}
        <div className="flex items-center gap-2 mt-4 pt-4 border-t border-charcoal/5">
          <button
            onClick={onToggle}
            className={`
              flex-1 py-2.5 rounded-xl text-sm font-medium transition-all
              ${isSelected ? "bg-charcoal text-white" : "bg-charcoal/5 text-charcoal hover:bg-charcoal/10"}
            `}
          >
            {isSelected ? "已加入" : "加入菜單"}
          </button>
          <button
            onClick={onReplace}
            className="p-2.5 rounded-xl bg-charcoal/5 text-charcoal/60 hover:bg-charcoal/10 hover:text-charcoal transition-all"
            title="替換菜色"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}
