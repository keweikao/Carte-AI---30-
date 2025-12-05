"use client"

import { useState } from "react"
import { Search, Users, Sparkles, ChefHat, ArrowRight, X } from "lucide-react"

interface OnboardingProps {
  onComplete: () => void
  onSkip: () => void
}

const steps = [
  {
    icon: Search,
    title: "搜尋餐廳",
    description: "輸入餐廳名稱，AI 會自動分析菜單與評論",
    color: "caramel",
  },
  {
    icon: Users,
    title: "設定偏好",
    description: "告訴我們人數、場合與飲食限制",
    color: "terracotta",
  },
  {
    icon: ChefHat,
    title: "獲得推薦",
    description: "AI 為您精選最適合的菜色組合",
    color: "charcoal",
  },
]

export function Onboarding({ onComplete, onSkip }: OnboardingProps) {
  const [currentStep, setCurrentStep] = useState(0)

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      onComplete()
    }
  }

  const step = steps[currentStep]
  const Icon = step.icon
  const isLast = currentStep === steps.length - 1

  const getColorClass = (type: "bg" | "text") => {
    const colors = {
      caramel: { bg: "bg-caramel", text: "text-caramel" },
      terracotta: { bg: "bg-terracotta", text: "text-terracotta" },
      charcoal: { bg: "bg-charcoal", text: "text-charcoal" },
    }
    return colors[step.color as keyof typeof colors][type]
  }

  return (
    <div className="fixed inset-0 z-50 bg-charcoal/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-[2rem] shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex justify-end p-4">
          <button
            onClick={onSkip}
            className="p-2 text-charcoal/40 hover:text-charcoal transition-colors"
            aria-label="關閉"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="px-8 pb-8">
          {/* Icon */}
          <div
            className={`
            w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-8
            ${getColorClass("bg")}
          `}
          >
            <Icon className="w-12 h-12 text-white" />
          </div>

          {/* Text */}
          <div className="text-center mb-8">
            <h2 className="font-serif text-2xl text-charcoal mb-3">{step.title}</h2>
            <p className="text-charcoal/60">{step.description}</p>
          </div>

          {/* Progress Dots */}
          <div className="flex items-center justify-center gap-2 mb-8">
            {steps.map((_, index) => (
              <div
                key={index}
                className={`
                  w-2 h-2 rounded-full transition-all
                  ${
                    index === currentStep
                      ? `${getColorClass("bg")} w-6`
                      : index < currentStep
                        ? "bg-charcoal/30"
                        : "bg-charcoal/10"
                  }
                `}
              />
            ))}
          </div>

          {/* Action */}
          <button
            onClick={handleNext}
            className={`
              w-full py-4 rounded-full font-semibold text-white transition-all
              flex items-center justify-center gap-2
              ${isLast ? "gradient-primary" : getColorClass("bg")}
              hover:scale-[1.02] hover:shadow-lg
            `}
          >
            {isLast ? (
              <>
                <Sparkles className="w-5 h-5" />
                開始使用
              </>
            ) : (
              <>
                下一步
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>

          {/* Skip */}
          {!isLast && (
            <button
              onClick={onSkip}
              className="w-full mt-3 py-3 text-sm text-charcoal/50 hover:text-charcoal transition-colors"
            >
              略過導覽
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
