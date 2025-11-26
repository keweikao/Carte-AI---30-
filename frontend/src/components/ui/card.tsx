import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { motion } from "framer-motion"

import { cn } from "@/lib/utils"
import {
  DURATION,
  prefersReducedMotion
} from "@/lib/animation-utils"

const cardVariants = cva(
  "bg-card text-card-foreground flex flex-col gap-6 rounded-xl border py-6 px-0 transition-colors",
  {
    variants: {
      variant: {
        default: "border-[var(--color-border)]",
        selected: "border-terracotta bg-terracotta/6",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

function Card({
  className,
  variant,
  ...props
}: React.ComponentProps<"div"> & VariantProps<typeof cardVariants>) {
  const [isHovered, setIsHovered] = React.useState(false)
  const reducedMotion = prefersReducedMotion()

  const motionProps = !reducedMotion
    ? {
        animate: {
          y: isHovered ? -4 : 0,
          scale: isHovered ? 1.01 : 1,
        },
        transition: {
          ...SPRING_CONFIGS.gentle,
          duration: DURATION.fast,
        },
        onHoverStart: () => setIsHovered(true),
        onHoverEnd: () => setIsHovered(false),
      }
    : {};

  return (
    <motion.div
      data-slot="card"
      className={cn(cardVariants({ variant, className }))}
      style={{
        boxShadow: isHovered && !reducedMotion
          ? "0 12px 40px rgba(45, 45, 45, 0.25)"
          : "0 4px 20px rgba(212, 165, 116, 0.15)",
        transition: "box-shadow 0.2s ease-out",
      }}
      {...motionProps}
      {...props}
    >
      {props.children}
    </motion.div>
  )
}

function CardHeader({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-header"
      className={cn(
        "@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-2 px-6 has-data-[slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6",
        className
      )}
      {...props}
    />
  )
}

function CardTitle({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-title"
      className={cn("leading-none font-semibold", className)}
      {...props}
    />
  )
}

function CardDescription({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-description"
      className={cn("text-muted-foreground text-sm", className)}
      {...props}
    />
  )
}

function CardAction({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-action"
      className={cn(
        "col-start-2 row-span-2 row-start-1 self-start justify-self-end",
        className
      )}
      {...props}
    />
  )
}

function CardContent({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-content"
      className={cn("px-6", className)}
      {...props}
    />
  )
}

function CardFooter({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-footer"
      className={cn("flex items-center px-6 [.border-t]:pt-6", className)}
      {...props}
    />
  )
}

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardAction,
  CardDescription,
  CardContent,
}
