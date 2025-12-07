import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { motion, AnimatePresence } from "framer-motion"

import { cn } from "@/lib/utils"
import {
  DURATION,
  EASING,
  prefersReducedMotion
} from "@/lib/animation-utils"
import { hapticLight } from "@/lib/haptic-utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full font-body font-medium transition-all disabled:pointer-events-none disabled:opacity-60 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 [&_svg]:shrink-0 outline-none focus-visible:ring-4 focus-visible:ring-[var(--color-ring)] focus-visible:ring-offset-2 focus-visible:ring-offset-cream-100",
  {
    variants: {
      variant: {
        primary:
          "bg-gradient-to-r from-accent-start to-accent-end text-white shadow-card hover:brightness-105 hover:-translate-y-[1px] active:brightness-95 active:translate-y-[1px]",
        secondary:
          "bg-sage text-white shadow-card hover:brightness-105 hover:-translate-y-[1px] active:brightness-95 active:translate-y-[1px]",
        outline:
          "border border-terracotta text-terracotta bg-transparent hover:bg-terracotta/10 active:bg-terracotta/15",
        ghost:
          "text-charcoal hover:bg-cream-200 active:bg-cream-200",
        link: "text-terracotta underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-9 px-4 py-2",
        md: "h-11 px-5 py-2.5",
        lg: "h-12 px-6 py-3",
        icon: "size-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
)

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot : "button"
  const [ripples, setRipples] = React.useState<
    Array<{ x: number; y: number; id: number }>
  >([])
  const buttonRef = React.useRef<HTMLButtonElement>(null)
  const reducedMotion = prefersReducedMotion()

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (!reducedMotion && !asChild) {
      const button = buttonRef.current || e.currentTarget
      const rect = button.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top
      const id = Date.now()

      setRipples((prev) => [...prev, { x, y, id }])

      // Haptic feedback for mobile
      hapticLight()

      // Remove ripple after animation
      setTimeout(() => {
        setRipples((prev) => prev.filter((ripple) => ripple.id !== id))
      }, 600)
    }

    // Call original onClick handler
    if (props.onClick) {
      props.onClick(e)
    }
  }

  if (asChild) {
    return (
      <Comp
        data-slot="button"
        className={cn(buttonVariants({ variant, size, className }))}
        {...props}
        onClick={handleClick}
      >
        {props.children}
      </Comp>
    )
  }

  return (
    <motion.button
      ref={buttonRef}
      data-slot="button"
      className={cn(
        buttonVariants({ variant, size, className }),
        "relative overflow-hidden"
      )}
      onClick={handleClick}
      whileTap={
        !reducedMotion
          ? { scale: 0.97, transition: { duration: DURATION.instant } }
          : undefined
      }
      whileHover={
        !reducedMotion
          ? {
              scale: 1.02,
              transition: { duration: DURATION.fast, ease: EASING.out },
            }
          : undefined
      }
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      {...(props as any)}
    >
      {props.children}
      {!reducedMotion && (
        <AnimatePresence>
          {ripples.map((ripple) => (
            <motion.span
              key={ripple.id}
              className="absolute rounded-full bg-white/30 pointer-events-none"
              style={{
                left: ripple.x,
                top: ripple.y,
                width: 0,
                height: 0,
              }}
              initial={{ width: 0, height: 0, opacity: 1 }}
              animate={{
                width: 200,
                height: 200,
                opacity: 0,
                x: -100,
                y: -100,
              }}
              exit={{ opacity: 0 }}
              transition={{
                duration: DURATION.slow,
                ease: EASING.out,
              }}
            />
          ))}
        </AnimatePresence>
      )}
    </motion.button>
  )
}

export { Button, buttonVariants }
