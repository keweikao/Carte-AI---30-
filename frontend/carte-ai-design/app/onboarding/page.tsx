"use client"

import { useRouter } from "next/navigation"
import { Onboarding } from "@/components/carte/onboarding"

export default function OnboardingPage() {
  const router = useRouter()

  const handleComplete = () => {
    // Save onboarding completion to localStorage
    localStorage.setItem("carte-onboarding-completed", "true")
    router.push("/input")
  }

  const handleSkip = () => {
    localStorage.setItem("carte-onboarding-completed", "true")
    router.push("/input")
  }

  return (
    <div className="min-h-screen bg-cream">
      <Onboarding onComplete={handleComplete} onSkip={handleSkip} />
    </div>
  )
}
