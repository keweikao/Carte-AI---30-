"use client"

import { Minus, Plus, Users } from "lucide-react"

interface StepPartySizeProps {
  value: number
  onChange: (size: number) => void
}

export function StepPartySize({ value, onChange }: StepPartySizeProps) {
  const quickSelects = [2, 4, 6, 8]
  const minSize = 1
  const maxSize = 20

  const handleIncrement = () => {
    if (value < maxSize) onChange(value + 1)
  }

  const handleDecrement = () => {
    if (value > minSize) onChange(value - 1)
  }

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="text-center">
        <h2 className="font-serif text-2xl md:text-3xl text-charcoal mb-2">用餐人數</h2>
        <p className="text-charcoal/60">我們會根據人數推薦適合的份量</p>
      </div>

      {/* Counter */}
      <div className="flex items-center justify-center gap-6">
        {/* Decrement Button */}
        <button
          onClick={handleDecrement}
          disabled={value <= minSize}
          className={`
            w-14 h-14 rounded-full flex items-center justify-center
            transition-all duration-200
            ${
              value <= minSize
                ? "bg-charcoal/5 text-charcoal/20 cursor-not-allowed"
                : "bg-white border-2 border-charcoal/10 text-charcoal hover:border-charcoal hover:bg-charcoal hover:text-white"
            }
          `}
          aria-label="減少人數"
        >
          <Minus className="w-6 h-6" />
        </button>

        {/* Counter Display */}
        <div className="w-32 text-center">
          <div className="font-serif text-6xl md:text-7xl text-charcoal">{value}</div>
          <div className="flex items-center justify-center gap-2 mt-2 text-charcoal/50">
            <Users className="w-4 h-4" />
            <span className="text-sm">位用餐</span>
          </div>
        </div>

        {/* Increment Button */}
        <button
          onClick={handleIncrement}
          disabled={value >= maxSize}
          className={`
            w-14 h-14 rounded-full flex items-center justify-center
            transition-all duration-200
            ${
              value >= maxSize
                ? "bg-charcoal/5 text-charcoal/20 cursor-not-allowed"
                : "bg-white border-2 border-charcoal/10 text-charcoal hover:border-charcoal hover:bg-charcoal hover:text-white"
            }
          `}
          aria-label="增加人數"
        >
          <Plus className="w-6 h-6" />
        </button>
      </div>

      {/* Quick Select Buttons */}
      <div className="flex items-center justify-center gap-3">
        {quickSelects.map((size) => (
          <button
            key={size}
            onClick={() => onChange(size)}
            className={`
              px-5 py-2.5 rounded-full text-sm font-medium transition-all
              ${
                value === size
                  ? "bg-charcoal text-white"
                  : "bg-white border-2 border-charcoal/10 text-charcoal/70 hover:border-caramel/50"
              }
            `}
          >
            {size} 人
          </button>
        ))}
      </div>

      {/* Helper Text */}
      <p className="text-center text-xs text-charcoal/40">
        可選擇 {minSize} - {maxSize} 人
      </p>
    </div>
  )
}
