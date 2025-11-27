"use client";

import { Card } from "@/components/ui/card";

interface RecommendationSummaryProps {
  totalDishes: number;
  categorySummary: Record<string, number>;
}

export function RecommendationSummary({
  totalDishes,
  categorySummary,
}: RecommendationSummaryProps) {
  // 生成摘要文字：「冷菜 1 道 · 熱菜 2 道 · 主食 1 道」
  const summaryText = Object.entries(categorySummary)
    .map(([category, count]) => `${category} ${count} 道`)
    .join(" · ");

  return (
    <Card className="mb-6 p-4 bg-cream-100 border-caramel/20">
      <div className="text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <span className="text-2xl" aria-hidden="true">📊</span>
          <h2 className="text-lg font-semibold text-foreground">
            為您推薦 {totalDishes} 道菜
          </h2>
        </div>
        <p className="text-sm text-muted-foreground">{summaryText}</p>
      </div>
    </Card>
  );
}
