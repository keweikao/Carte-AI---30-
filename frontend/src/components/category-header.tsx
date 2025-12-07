"use client";

import { getCategoryIcon } from "@/constants/categories";

interface CategoryHeaderProps {
  category: string;
  count: number;
  cuisineType: string;
}

export function CategoryHeader({ category, count, cuisineType }: CategoryHeaderProps) {
  const icon = getCategoryIcon(category, cuisineType);

  return (
    <div className="flex items-center justify-center my-8" role="heading" aria-level={2}>
      <div className="flex items-center gap-2 px-4 py-2 bg-sage/10 rounded-full shadow-sm">
        <span className="text-xl" aria-hidden="true">{icon}</span>
        <h3 className="text-md font-semibold text-sage-800">
          {category} ({count})
        </h3>
      </div>
    </div>
  );
}
