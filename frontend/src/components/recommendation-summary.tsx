"use client";

import { Card } from "@/components/ui/card";
import { useTranslations } from "next-intl";

interface RecommendationSummaryProps {
  totalDishes: number;
  categorySummary: Record<string, number>;
}

export function RecommendationSummary({
  totalDishes,
  categorySummary,
}: RecommendationSummaryProps) {
  const t = useTranslations('RecommendationPage');

  // 生成摘要文字：「冷菜 1 道 · 熱菜 2 道 · 主食 1 道」
  const summaryText = Object.entries(categorySummary)
    .map(([category, count]) => `${category} ${count} ${t('dishes')}`)
    .join(" · ");

  return (
    <Card className="mb-6 p-4 bg-cream-100 border-caramel/20">
      <div className="text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <span className="text-2xl" aria-hidden="true">✨</span>
          <h2 className="text-lg font-semibold text-foreground">
            {t('recommending_dishes', { count: totalDishes })}
          </h2>
        </div>
        <p className="text-sm text-muted-foreground">{summaryText}</p>
      </div>
    </Card>
  );
}
