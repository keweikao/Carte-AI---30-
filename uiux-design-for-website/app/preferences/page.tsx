"use client"

import { useState } from "react"
import Header from "@/components/header"
import { Button } from "@/components/ui/button"

export default function PreferencesPage() {
  const [step, setStep] = useState(1)
  const [preferences, setPreferences] = useState({
    mealType: "shared",
    partySize: 2,
    budget: "500-1000",
    dietaryPreferences: [] as string[],
    customBudget: null as number | null,
  })

  const dietaryOptions = [
    { id: "no-beef", label: "不吃牛", icon: "🥩" },
    { id: "no-pork", label: "不吃豬", icon: "🐷" },
    { id: "vegetarian", label: "素食", icon: "🥬" },
    { id: "seafood", label: "海鮮過敏", icon: "🦞" },
    { id: "spicy", label: "愛吃辣", icon: "🌶️" },
    { id: "no-spicy", label: "不吃辣", icon: "🚫" },
    { id: "no-alcohol", label: "想喝酒", icon: "🍺" },
    { id: "kids", label: "有小孩", icon: "👶" },
    { id: "elderly", label: "長輩友善", icon: "👴" },
  ]

  const handlePreferenceChange = (key: string, value: any) => {
    setPreferences((prev) => ({
      ...prev,
      [key]: value,
    }))
  }

  const handleGenerateRecommendation = () => {
    // Send preferences to generate recommendations
    console.log("Generating recommendations with:", preferences)
  }

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header title="自訂你的餐點" />

      <main className="flex-1 p-6 max-w-2xl mx-auto w-full">
        {/* Header Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-foreground mb-2">客製化你的餐點</h1>
          <p className="text-muted-foreground text-lg">告訴我們你的喜好</p>
        </div>

        {/* Meal Type Selection */}
        <div className="mb-10">
          <h2 className="text-xl font-semibold text-foreground mb-4">用餐方式</h2>
          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => handlePreferenceChange("mealType", "shared")}
              className={`p-4 rounded-lg border-2 transition-all ${
                preferences.mealType === "shared"
                  ? "border-primary bg-primary/10"
                  : "border-border bg-card hover:border-primary/30"
              }`}
            >
              <div className="text-2xl mb-2">👥</div>
              <span className="font-medium text-foreground">大家一起分食</span>
            </button>
            <button
              onClick={() => handlePreferenceChange("mealType", "individual")}
              className={`p-4 rounded-lg border-2 transition-all ${
                preferences.mealType === "individual"
                  ? "border-primary bg-primary/10"
                  : "border-border bg-card hover:border-primary/30"
              }`}
            >
              <div className="text-2xl mb-2">🍽️</div>
              <span className="font-medium text-foreground">個人套餐</span>
            </button>
          </div>
        </div>

        {/* Party Size */}
        <div className="mb-10">
          <h2 className="text-xl font-semibold text-foreground mb-4">幾位用餐？</h2>
          <div className="flex items-center justify-center gap-6">
            <button
              onClick={() => handlePreferenceChange("partySize", Math.max(1, preferences.partySize - 1))}
              className="w-12 h-12 rounded-full border-2 border-border hover:border-primary text-foreground hover:text-primary transition-colors flex items-center justify-center text-xl"
            >
              −
            </button>
            <span className="text-4xl font-bold text-foreground min-w-16 text-center">{preferences.partySize}</span>
            <button
              onClick={() => handlePreferenceChange("partySize", preferences.partySize + 1)}
              className="w-12 h-12 rounded-full border-2 border-border hover:border-primary text-foreground hover:text-primary transition-colors flex items-center justify-center text-xl"
            >
              +
            </button>
          </div>
        </div>

        {/* Budget Range */}
        <div className="mb-10">
          <h2 className="text-xl font-semibold text-foreground mb-4">預算範圍</h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              { value: "under-500", label: "500以下" },
              { value: "500-1000", label: "500 - 1000" },
              { value: "over-1000", label: "1000以上" },
              { value: "custom", label: "自訂" },
            ].map((option) => (
              <button
                key={option.value}
                onClick={() => handlePreferenceChange("budget", option.value)}
                className={`p-3 rounded-lg border-2 transition-all font-medium ${
                  preferences.budget === option.value
                    ? "border-primary bg-primary/10 text-primary"
                    : "border-border bg-card text-foreground hover:border-primary/30"
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
          {preferences.budget === "custom" && (
            <input
              type="number"
              placeholder="輸入預算..."
              value={preferences.customBudget || ""}
              onChange={(e) =>
                handlePreferenceChange("customBudget", e.target.value ? Number.parseInt(e.target.value) : null)
              }
              className="mt-3 w-full px-4 py-2 border border-border rounded-lg bg-input text-foreground placeholder:text-muted-foreground"
            />
          )}
        </div>

        {/* Dietary Preferences */}
        <div className="mb-10">
          <h2 className="text-xl font-semibold text-foreground mb-4">飲食偏好</h2>
          <div className="grid grid-cols-3 gap-3">
            {dietaryOptions.map((option) => (
              <button
                key={option.id}
                onClick={() => {
                  setPreferences((prev) => ({
                    ...prev,
                    dietaryPreferences: prev.dietaryPreferences.includes(option.id)
                      ? prev.dietaryPreferences.filter((p) => p !== option.id)
                      : [...prev.dietaryPreferences, option.id],
                  }))
                }}
                className={`p-4 rounded-lg border-2 transition-all text-center ${
                  preferences.dietaryPreferences.includes(option.id)
                    ? "border-primary bg-primary/10"
                    : "border-border bg-card hover:border-primary/30"
                }`}
              >
                <div className="text-3xl mb-2">{option.icon}</div>
                <span className="text-sm font-medium text-foreground">{option.label}</span>
              </button>
            ))}
          </div>
          <p className="text-sm text-muted-foreground mt-4">若你要用自然語言描述課題 AI 更了解你的需求也可以喔...</p>
        </div>

        {/* CTA Button */}
        <Button
          onClick={handleGenerateRecommendation}
          className="w-full bg-primary text-primary-foreground hover:bg-primary/90 py-6 text-lg font-semibold"
        >
          開始生成推薦
        </Button>
      </main>
    </div>
  )
}
