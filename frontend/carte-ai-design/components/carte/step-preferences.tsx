"use client"

import { Briefcase, Heart, Users, Utensils } from "lucide-react"

type Occasion = "friends" | "family" | "date" | "business"

interface Preferences {
  occasion: Occasion | null
  dietary: string[]
}

interface StepPreferencesProps {
  value: Preferences
  onChange: (prefs: Preferences) => void
}

export function StepPreferences({ value, onChange }: StepPreferencesProps) {
  const occasions = [
    { id: "friends" as Occasion, icon: Users, label: "朋友聚餐" },
    { id: "family" as Occasion, icon: Utensils, label: "家庭聚會" },
    { id: "date" as Occasion, icon: Heart, label: "浪漫約會" },
    { id: "business" as Occasion, icon: Briefcase, label: "商務應酬" },
  ]

  const dietaryOptions = [
    { id: "no-beef", label: "不吃牛" },
    { id: "no-pork", label: "不吃豬" },
    { id: "no-spicy", label: "不吃辣" },
    { id: "vegetarian", label: "全素" },
    { id: "pescatarian", label: "鍋邊素" },
    { id: "low-salt", label: "少油少鹽" },
    { id: "senior", label: "老人友善" },
    { id: "kids", label: "兒童友善" },
    { id: "seafood-allergy", label: "海鮮過敏" },
    { id: "nut-allergy", label: "堅果過敏" },
  ]

  const handleOccasionChange = (occasion: Occasion) => {
    onChange({ ...value, occasion })
  }

  const handleDietaryToggle = (id: string) => {
    const newDietary = value.dietary.includes(id) ? value.dietary.filter((d) => d !== id) : [...value.dietary, id]
    onChange({ ...value, dietary: newDietary })
  }

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="text-center">
        <h2 className="font-serif text-2xl md:text-3xl text-charcoal mb-2">場合與偏好</h2>
        <p className="text-charcoal/60">讓我們更了解這次用餐</p>
      </div>

      {/* Occasion Selection */}
      <div>
        <h3 className="text-sm font-medium text-charcoal/70 mb-3">用餐場合</h3>
        <div className="grid grid-cols-2 gap-3">
          {occasions.map((occ) => {
            const isSelected = value.occasion === occ.id
            const Icon = occ.icon

            return (
              <button
                key={occ.id}
                onClick={() => handleOccasionChange(occ.id)}
                className={`
                  flex items-center gap-3 p-4 rounded-xl transition-all
                  ${
                    isSelected
                      ? "bg-charcoal text-white"
                      : "bg-white border-2 border-charcoal/10 text-charcoal hover:border-caramel/50"
                  }
                `}
              >
                <Icon className={`w-5 h-5 ${isSelected ? "text-caramel" : "text-caramel"}`} />
                <span className="text-sm font-medium">{occ.label}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Dietary Preferences */}
      <div>
        <h3 className="text-sm font-medium text-charcoal/70 mb-3">
          飲食偏好 <span className="text-charcoal/40 font-normal">(可多選)</span>
        </h3>
        <div className="flex flex-wrap gap-2">
          {dietaryOptions.map((option) => {
            const isSelected = value.dietary.includes(option.id)

            return (
              <button
                key={option.id}
                onClick={() => handleDietaryToggle(option.id)}
                className={`
                  px-4 py-2 rounded-full text-sm transition-all
                  ${
                    isSelected
                      ? "bg-terracotta text-white border-2 border-terracotta"
                      : "bg-white text-charcoal/70 border-2 border-charcoal/10 hover:border-terracotta/50"
                  }
                `}
              >
                {option.label}
              </button>
            )
          })}
        </div>
      </div>

      {/* Summary */}
      {(value.occasion || value.dietary.length > 0) && (
        <div className="p-4 bg-caramel/5 rounded-xl">
          <p className="text-sm text-charcoal/70">
            <span className="font-medium">您的選擇：</span>
            {value.occasion && <span className="ml-2">{occasions.find((o) => o.id === value.occasion)?.label}</span>}
            {value.dietary.length > 0 && (
              <span className="ml-2 text-terracotta">+ {value.dietary.length} 項飲食偏好</span>
            )}
          </p>
        </div>
      )}
    </div>
  )
}
