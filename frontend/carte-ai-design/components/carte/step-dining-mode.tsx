"use client"

import { UtensilsCrossed, User } from "lucide-react"

type DiningMode = "sharing" | "individual"

interface StepDiningModeProps {
  value: DiningMode | null
  onChange: (mode: DiningMode) => void
}

export function StepDiningMode({ value, onChange }: StepDiningModeProps) {
  const modes = [
    {
      id: "sharing" as DiningMode,
      icon: UtensilsCrossed,
      title: "分食合菜",
      description: "多道菜一起享用，適合聚餐",
      examples: "合菜、桌菜、家庭聚餐",
    },
    {
      id: "individual" as DiningMode,
      icon: User,
      title: "個人套餐",
      description: "每人各點各的，獨立享用",
      examples: "定食、套餐、個人餐點",
    },
  ]

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="text-center">
        <h2 className="font-serif text-2xl md:text-3xl text-charcoal mb-2">用餐方式</h2>
        <p className="text-charcoal/60">選擇您的用餐模式，讓推薦更精準</p>
      </div>

      {/* Mode Options */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {modes.map((mode) => {
          const isSelected = value === mode.id
          const Icon = mode.icon

          return (
            <button
              key={mode.id}
              onClick={() => onChange(mode.id)}
              className={`
                relative p-6 rounded-2xl text-left transition-all duration-300
                ${
                  isSelected
                    ? "bg-charcoal text-white shadow-lg scale-[1.02]"
                    : "bg-white border-2 border-charcoal/10 hover:border-caramel/50 hover:bg-caramel/5"
                }
              `}
            >
              {/* Selection Indicator */}
              {isSelected && (
                <div className="absolute top-4 right-4 w-6 h-6 bg-white rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-charcoal" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              )}

              {/* Icon */}
              <div
                className={`
                w-12 h-12 rounded-xl flex items-center justify-center mb-4
                ${isSelected ? "bg-white/20" : "bg-caramel/10"}
              `}
              >
                <Icon className={`w-6 h-6 ${isSelected ? "text-white" : "text-caramel"}`} />
              </div>

              {/* Content */}
              <h3 className={`font-medium text-lg mb-1 ${isSelected ? "text-white" : "text-charcoal"}`}>
                {mode.title}
              </h3>
              <p className={`text-sm mb-3 ${isSelected ? "text-white/70" : "text-charcoal/60"}`}>{mode.description}</p>
              <p className={`text-xs ${isSelected ? "text-white/50" : "text-charcoal/40"}`}>{mode.examples}</p>
            </button>
          )
        })}
      </div>
    </div>
  )
}
