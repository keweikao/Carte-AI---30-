import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

interface MenuSummarySkeletonProps {
  className?: string;
}

/**
 * Skeleton loading state for MenuSummary component
 *
 * Matches the exact layout and dimensions of the actual MenuSummary:
 * - Category badges grid
 * - Price summary (total price and per person)
 * - Progress bar with text
 */
export function MenuSummarySkeleton({ className }: MenuSummarySkeletonProps) {
  return (
    <div className={cn("bg-cream-100 p-4 rounded-xl shadow-card space-y-4", className)}>
      {/* Category Summary Grid - 3-4 badge placeholders */}
      <div className="flex flex-wrap gap-2">
        <Skeleton className="h-6 w-20 rounded-full" />
        <Skeleton className="h-6 w-24 rounded-full" />
        <Skeleton className="h-6 w-16 rounded-full" />
        <Skeleton className="h-6 w-20 rounded-full" />
      </div>

      {/* Price Summary */}
      <div className="flex justify-between items-end">
        <div>
          <Skeleton className="h-3 w-12 mb-2" />
          <Skeleton className="h-8 w-32" />
        </div>
        <div className="text-right">
          <Skeleton className="h-3 w-16 mb-2" />
          <Skeleton className="h-6 w-24" />
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1">
        <Skeleton className="h-4 w-32" />
        <Skeleton className="h-2 w-full rounded-full" />
      </div>
    </div>
  );
}
