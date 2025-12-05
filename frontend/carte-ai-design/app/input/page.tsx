"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react"
import { ProgressBar } from "@/components/carte/progress-bar"
import { StepRestaurant } from "@/components/carte/step-restaurant"
import { StepDiningMode } from "@/components/carte/step-dining-mode"
import { StepPartySize } from "@/components/carte/step-party-size"
import { StepPreferences } from "@/components/carte/step-preferences"

interface Restaurant {
  id: string
  name: string
  type: string
  rating: number
  priceLevel: string
  distance: string
  address: string
}

type DiningMode = "sharing" | "individual"
type Occasion = "friends" | "family" | "date" | "business"

interface FormData {
  restaurant: Restaurant | null
  diningMode: DiningMode | null
  partySize: number
  preferences: {
    occasion: Occasion | null
    dietary: string[]
  }
}

export default function InputPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState<FormData>({
    restaurant: null,
    diningMode: null,
    partySize: 2,
    preferences: {
      occasion: null,
      dietary: [],
    },
  })

  const totalSteps = 4

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return formData.restaurant !== null
      case 2:
        return formData.diningMode !== null
      case 3:
        return formData.partySize >= 1
      case 4:
        return formData.preferences.occasion !== null
      default:
        return false
    }
  }

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1)
    } else {
      // Submit and navigate to waiting screen
      router.push("/waiting")
    }
  }

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleStepClick = (step: number) => {
    if (step < currentStep) {
      setCurrentStep(step)
    }
  }

  return (
    <div className="min-h-screen bg-cream">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-cream/80 backdrop-blur-md border-b border-charcoal/5">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-charcoal/60 hover:text-charcoal transition-colors">
            <ArrowLeft className="w-5 h-5" />
            <span className="text-sm">返回首頁</span>
          </Link>
          <Link href="/" className="font-serif text-xl text-charcoal">
            Carte <span className="text-caramel text-xs">AI</span>
          </Link>
          <div className="w-20" /> {/* Spacer for centering */}
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-32 px-4">
        <div className="max-w-xl mx-auto">
          {/* Progress Bar */}
          <div className="mb-12">
            <ProgressBar currentStep={currentStep} totalSteps={totalSteps} onStepClick={handleStepClick} />
          </div>

          {/* Main Card */}
          <div className="bg-white rounded-[2rem] shadow-floating border border-white/50 p-6 sm:p-8 min-h-[420px]">
            {/* Step Content */}
            {currentStep === 1 && (
              <StepRestaurant
                value={formData.restaurant}
                onChange={(restaurant) => setFormData({ ...formData, restaurant })}
              />
            )}
            {currentStep === 2 && (
              <StepDiningMode
                value={formData.diningMode}
                onChange={(diningMode) => setFormData({ ...formData, diningMode })}
              />
            )}
            {currentStep === 3 && (
              <StepPartySize
                value={formData.partySize}
                onChange={(partySize) => setFormData({ ...formData, partySize })}
              />
            )}
            {currentStep === 4 && (
              <StepPreferences
                value={formData.preferences}
                onChange={(preferences) => setFormData({ ...formData, preferences })}
              />
            )}
          </div>
        </div>
      </main>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-cream/80 backdrop-blur-md border-t border-charcoal/5 p-4">
        <div className="max-w-xl mx-auto flex items-center justify-between gap-4">
          {/* Back Button */}
          {currentStep > 1 ? (
            <button
              onClick={handleBack}
              className="flex items-center gap-2 px-6 py-3 text-charcoal/70 hover:text-charcoal transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>上一步</span>
            </button>
          ) : (
            <div /> // Spacer
          )}

          {/* Next / Submit Button */}
          <button
            onClick={handleNext}
            disabled={!canProceed()}
            className={`
              flex items-center gap-2 px-8 py-3 rounded-full font-semibold transition-all
              ${
                canProceed()
                  ? currentStep === totalSteps
                    ? "gradient-primary text-white shadow-lg hover:shadow-xl hover:scale-105"
                    : "bg-charcoal text-white hover:bg-charcoal/90"
                  : "bg-charcoal/20 text-charcoal/40 cursor-not-allowed"
              }
            `}
          >
            {currentStep === totalSteps ? (
              <>
                <span>告訴我該點什麼</span>
                <Sparkles className="w-4 h-4" />
              </>
            ) : (
              <>
                <span>下一步</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
