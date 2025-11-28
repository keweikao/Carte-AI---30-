"use client";

// import { useMemo } from "react";
// import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import type { RecommendationResponse } from "@/types";

interface MenuSummaryProps {
  categorySummary: RecommendationResponse['category_summary']; // Record<string, number>
  totalPrice: number;
  perPerson: number;
  decidedCount: number;
  totalCount: number;
  className?: string;
}

export function MenuSummary({
  categorySummary,
  totalPrice,
  perPerson,
  decidedCount,
  totalCount,
  className,
}: MenuSummaryProps) {
  // const categories = useMemo(() => {
  //   return Object.entries(categorySummary).map(([category, count]) => (
  //     <Badge key={category} variant="neutral" className="flex-shrink-0">
  //       {category} x {count}
  //     </Badge>
  //   ));
  // }, [categorySummary]);

  const progressValue = totalCount > 0 ? (decidedCount / totalCount) * 100 : 0;

  return (
    <div className={cn("bg-cream-100 p-4 rounded-xl shadow-card space-y-4", className)}>
      {/* Category Summary Grid Removed */}

      {/* Price Summary */}
      <div className="flex justify-between items-end">
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wider">總價</p>
          <h2 className="text-2xl font-bold font-mono text-foreground">NT$ {totalPrice.toLocaleString()}</h2>
        </div>
        <div className="text-right">
          <p className="text-xs text-muted-foreground">人均約</p>
          <p className="text-xl font-bold font-mono text-terracotta">NT$ {perPerson.toLocaleString()}</p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1">
        <p className="text-sm text-muted-foreground">
          已決定 {decidedCount} / {totalCount} 道菜
        </p>
        <Progress value={progressValue} className="w-full" complete={decidedCount === totalCount} />
      </div>
    </div>
  );
}
