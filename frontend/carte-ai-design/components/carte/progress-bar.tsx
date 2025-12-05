"use client"

interface ProgressBarProps {
  currentStep: number
  totalSteps: number
  onStepClick?: (step: number) => void
}

export function ProgressBar({ currentStep, totalSteps, onStepClick }: ProgressBarProps) {
  const steps = [
    { number: 1, label: "餐廳" },
    { number: 2, label: "模式" },
    { number: 3, label: "人數" },
    { number: 4, label: "偏好" },
  ]

  return (
    <div className="w-full max-w-md mx-auto">
      {/* Progress Line */}
      <div className="relative flex items-center justify-between">
        {/* Background Line */}
        <div className="absolute left-0 right-0 h-0.5 bg-charcoal/10" />

        {/* Active Line */}
        <div
          className="absolute left-0 h-0.5 bg-charcoal transition-all duration-500 ease-out"
          style={{ width: `${((currentStep - 1) / (totalSteps - 1)) * 100}%` }}
        />

        {/* Step Indicators */}
        {steps.map((step) => {
          const isCompleted = step.number < currentStep
          const isActive = step.number === currentStep
          const isClickable = step.number < currentStep && onStepClick

          return (
            <button
              key={step.number}
              onClick={() => isClickable && onStepClick(step.number)}
              disabled={!isClickable}
              className={`
                relative z-10 flex flex-col items-center gap-2
                ${isClickable ? "cursor-pointer" : "cursor-default"}
              `}
            >
              <div
                className={`
                  w-10 h-10 rounded-full flex items-center justify-center
                  text-sm font-medium transition-all duration-300
                  ${
                    isCompleted
                      ? "bg-charcoal text-white"
                      : isActive
                        ? "bg-caramel text-white scale-110 shadow-lg"
                        : "bg-white text-charcoal/40 border-2 border-charcoal/10"
                  }
                `}
              >
                {isCompleted ? (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  step.number
                )}
              </div>
              <span
                className={`
                  text-xs font-medium transition-colors
                  ${isActive ? "text-charcoal" : "text-charcoal/40"}
                `}
              >
                {step.label}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
