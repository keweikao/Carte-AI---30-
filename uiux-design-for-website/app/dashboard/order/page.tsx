"use client"

import { useState, type FormEvent } from "react"
import { useAuth } from "@/lib/auth-context"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function OrderPage() {
  const { user } = useAuth()
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const [formData, setFormData] = useState({
    restaurant: "",
    mealType: "shared",
    people: 2,
    budget: "500-1000",
    preferences: [] as string[],
  })

  const preferences = ["不吃牛", "不吃豬", "不吃辣", "素食", "海鮮過敏", "要喝酒", "有長輩", "有小孩"]

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch("/api/searches/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        const data = await response.json()
        router.push(`/dashboard/analyzing/${data.session_id}`)
      }
    } catch (error) {
      console.error("Failed to submit order:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-foreground text-balance">幫我決定吃什麼</h1>
        <p className="mt-2 text-muted-foreground">告訴我們你的喜好</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8 rounded-lg border border-border bg-card p-8">
        {/* Restaurant Selection */}
        <div className="space-y-3">
          <Label className="text-base font-medium text-foreground">1. 餐廳名稱</Label>
          <Input
            placeholder="搜尋餐廳..."
            value={formData.restaurant}
            onChange={(e) => setFormData({ ...formData, restaurant: e.target.value })}
            className="border-border bg-input text-foreground placeholder:text-muted-foreground focus:ring-primary"
            required
          />
        </div>

        {/* Meal Type */}
        <div className="space-y-3">
          <Label className="text-base font-medium text-foreground">2. 用餐方式</Label>
          <div className="grid grid-cols-2 gap-3">
            {[
              { value: "shared", label: "大家分食", icon: "👥" },
              { value: "personal", label: "個人套餐", icon: "🍽️" },
            ].map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setFormData({ ...formData, mealType: option.value })}
                className={`rounded-lg border-2 px-6 py-4 text-center transition-all ${
                  formData.mealType === option.value
                    ? "border-primary bg-primary/5 text-foreground"
                    : "border-border text-foreground hover:border-primary/50"
                }`}
              >
                <span className="mb-2 block text-2xl">{option.icon}</span>
                <span className="text-sm font-medium">{option.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* People Count */}
        <div className="space-y-3">
          <Label className="text-base font-medium text-foreground">3. 幾位用餐？</Label>
          <div className="flex items-center justify-center gap-4">
            <button
              type="button"
              onClick={() => setFormData({ ...formData, people: Math.max(1, formData.people - 1) })}
              className="flex h-10 w-10 items-center justify-center rounded-full border border-border text-foreground hover:bg-secondary transition-colors"
            >
              −
            </button>
            <span className="w-8 text-center text-2xl font-semibold text-foreground">{formData.people}</span>
            <button
              type="button"
              onClick={() => setFormData({ ...formData, people: formData.people + 1 })}
              className="flex h-10 w-10 items-center justify-center rounded-full border border-border text-foreground hover:bg-secondary transition-colors"
            >
              +
            </button>
          </div>
        </div>

        {/* Budget */}
        <div className="space-y-3">
          <Label className="text-base font-medium text-foreground">4. 人均預算</Label>
          <div className="grid grid-cols-2 gap-2 md:grid-cols-4">
            {["500以下", "500-1000", "1000以上", "自訂"].map((budget) => (
              <button
                key={budget}
                type="button"
                onClick={() => setFormData({ ...formData, budget })}
                className={`rounded-lg border px-3 py-2 text-sm font-medium transition-all ${
                  formData.budget === budget
                    ? "border-primary bg-primary text-primary-foreground"
                    : "border-border text-foreground hover:border-primary/50"
                }`}
              >
                {budget}
              </button>
            ))}
          </div>
        </div>

        {/* Preferences */}
        <div className="space-y-3">
          <Label className="text-base font-medium text-foreground">5. 飲食偏好</Label>
          <div className="grid grid-cols-3 gap-2">
            {preferences.map((pref) => (
              <button
                key={pref}
                type="button"
                onClick={() =>
                  setFormData((prev) => ({
                    ...prev,
                    preferences: prev.preferences.includes(pref)
                      ? prev.preferences.filter((p) => p !== pref)
                      : [...prev.preferences, pref],
                  }))
                }
                className={`rounded-lg border-2 px-3 py-2 text-xs font-medium transition-all ${
                  formData.preferences.includes(pref)
                    ? "border-primary bg-primary/5 text-foreground"
                    : "border-border text-foreground hover:border-primary/50"
                }`}
              >
                {pref}
              </button>
            ))}
          </div>
        </div>

        {/* Submit */}
        <Button
          type="submit"
          disabled={loading || !formData.restaurant}
          className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
        >
          {loading ? "分析中..." : "開始分析"}
        </Button>
      </form>
    </div>
  )
}
