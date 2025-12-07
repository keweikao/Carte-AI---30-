import { cn } from "@/lib/utils"

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Whether to animate the skeleton with a pulse effect
   * @default true
   */
  animate?: boolean;
}

/**
 * Base Skeleton component for loading states
 *
 * Features:
 * - Pulse animation using design system colors (cream, caramel)
 * - Respects prefers-reduced-motion for accessibility
 * - Fully customizable with className prop
 * - Follows OderWhat design system
 */
function Skeleton({
  className,
  animate = true,
  ...props
}: SkeletonProps) {
  return (
    <div
      className={cn(
        "bg-gradient-to-r from-cream-200 via-caramel-50 to-cream-200 bg-[length:200%_100%] rounded-lg",
        animate && "animate-skeleton",
        className
      )}
      aria-live="polite"
      aria-busy="true"
      {...props}
    />
  )
}

export { Skeleton }
