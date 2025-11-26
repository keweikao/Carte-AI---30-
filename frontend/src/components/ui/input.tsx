import * as React from "react"
import { motion } from "framer-motion"

import { cn } from "@/lib/utils"
import { DURATION, EASING, SPRING_CONFIGS, prefersReducedMotion } from "@/lib/animation-utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  const [isFocused, setIsFocused] = React.useState(false)
  const inputRef = React.useRef<HTMLInputElement>(null)
  const reducedMotion = prefersReducedMotion()

  const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
    setIsFocused(true)
    if (props.onFocus) {
      props.onFocus(e)
    }
  }

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    setIsFocused(false)
    if (props.onBlur) {
      props.onBlur(e)
    }
  }

  const motionProps = !reducedMotion
    ? {
        animate: {
          scale: isFocused ? 1.01 : 1,
          y: isFocused ? -1 : 0,
        },
        transition: {
          ...SPRING_CONFIGS.gentle,
          duration: DURATION.fast,
        },
      }
    : {};

  return (
    <div className="relative w-full">
      <motion.input
        ref={inputRef}
        type={type}
        data-slot="input"
        className={cn(
          "h-12 w-full min-w-0 rounded-md border border-[var(--color-border)] bg-surface px-4 text-base font-body text-charcoal shadow-xs transition-all outline-none",
          "placeholder:text-[rgba(45,45,45,0.4)] selection:bg-terracotta/20 selection:text-charcoal",
          "focus-visible:ring-4 focus-visible:ring-[var(--color-ring)] focus-visible:ring-offset-2 focus-visible:ring-offset-cream-100 focus-visible:border-0",
          "aria-invalid:border-error aria-invalid:ring-error/20 aria-invalid:ring-4",
          "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-60",
          className
        )}
        onFocus={handleFocus}
        onBlur={handleBlur}
        {...motionProps}
        {...props}
      />
      {!reducedMotion && (
        <motion.div
          className="absolute inset-0 rounded-md pointer-events-none"
          initial={false}
          animate={{
            opacity: isFocused ? 1 : 0,
            scale: isFocused ? 1 : 0.95,
          }}
          transition={{
            duration: DURATION.fast,
            ease: EASING.out,
          }}
          style={{
            background:
              "radial-gradient(circle at center, rgba(200, 90, 84, 0.05) 0%, transparent 70%)",
          }}
        />
      )}
    </div>
  )
}

export { Input }
