import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

interface DishCardSkeletonProps {
  className?: string;
}

/**
 * Skeleton loading state for DishCard component
 *
 * Matches the exact layout and dimensions of the actual DishCard:
 * - Image placeholder (96px x 96px)
 * - Title, price, and badge
 * - Description (2 lines)
 * - Review count
 * - Action buttons
 */
export function DishCardSkeleton({ className }: DishCardSkeletonProps) {
  return (
    <Card
      className={cn(
        "p-4 rounded-xl bg-white shadow-sm",
        className
      )}
    >
      <div className="flex gap-4 items-start">
        {/* Dish Image Placeholder - matches DishCard's 96px (w-24 h-24) */}
        <Skeleton className="flex-shrink-0 w-24 h-24 rounded-lg" />

        {/* Right Content */}
        <div className="flex-1 min-w-0 flex flex-col justify-between">
          {/* Row 1: Title & Price */}
          <div className="flex justify-between items-start mb-2 gap-2">
            <div className="flex items-center gap-2 flex-1">
              {/* Title - varies in width, typically 120-180px */}
              <Skeleton className="h-6 w-36" />
              {/* Badge placeholder */}
              <Skeleton className="h-5 w-12 rounded-full" />
            </div>
            {/* Price - consistent width ~80px */}
            <Skeleton className="h-6 w-20" />
          </div>

          {/* Row 2: Reason - 2 lines with line-clamp */}
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-4/5" />
          </div>

          {/* Row 3: Review Count */}
          <div className="flex items-center gap-2 mt-2">
            <Skeleton className="h-4 w-24" />
          </div>

          {/* Row 4: Action Buttons */}
          <div className="flex items-center gap-2 mt-4">
            <Skeleton className="flex-1 h-9 rounded-full" />
            <Skeleton className="h-9 w-24 rounded-full" />
          </div>
        </div>
      </div>
    </Card>
  );
}
