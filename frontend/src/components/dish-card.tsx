"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CheckCircle2, RotateCw, Star } from "lucide-react";
import { motion } from "framer-motion";
import type { MenuItem, DishStatus } from "@/types";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge"; // Ensure Badge is imported

interface DishCardProps {
  item: MenuItem;
  status: DishStatus; // 'pending' or 'selected'
  onSelect: (dishName: string) => void;
  onSwap: () => void;
  isSwapping: boolean; // Indicates if the card is currently swapping
}

export function DishCard({ item, status, onSelect, onSwap, isSwapping }: DishCardProps) {
  const isSelected = status === 'selected';

  return (
    <motion.div
      key={item.dish_name} // Key by dish_name for animation
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card
        className={cn(
          "p-4 transition-all duration-300 rounded-xl bg-white shadow-sm",
          isSelected ? "opacity-50" : ""
        )}
      >
        <div className="flex gap-4 items-start">
          {/* Dish Image Placeholder */}
          <div className="flex-shrink-0 w-24 h-24 bg-cream-200 rounded-lg flex items-center justify-center text-charcoal/60 text-sm overflow-hidden">
            {/* You could add an actual image here, or an icon */}
            <span className="text-4xl">🍜</span>
          </div>

          {/* Right Content */}
          <div className="flex-1 min-w-0 flex flex-col justify-between">
            {/* Row 1: Title & Price */}
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-lg text-foreground leading-tight truncate pr-2">
                  {item.dish_name} {item.quantity > 1 && <span className="text-caramel">x{item.quantity}</span>}
                </h3>
                {item.price_estimated && (
                  <Badge variant="neutral" className="bg-caramel/10 text-caramel border-caramel/20">估價</Badge>
                )}
              </div>
              <div className="text-right">
                <span className="text-lg font-mono font-semibold text-foreground">NT$ {item.price * item.quantity}</span>
                {item.quantity > 1 && (
                  <div className="text-xs text-muted-foreground">{item.quantity} × NT$ {item.price}</div>
                )}
              </div>
            </div>

            {/* Row 2: Reason & Review Count */}
            <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed font-body">&quot;{item.reason}&quot;</p>
            <div className="flex items-center gap-2 mt-2 text-sm text-muted-foreground">
              {item.review_count && item.review_count > 0 && (
                <span className="flex items-center gap-1">
                  <Star className="w-3 h-3 fill-current text-caramel" /> {item.review_count} 則好評
                </span>
              )}
              {item.tag && (
                <Badge
                  variant="neutral"
                  className={cn(
                    "text-xs border-0",
                    item.tag === "必點" && "bg-red-100 text-red-700",
                    item.tag === "隱藏版" && "bg-purple-100 text-purple-700",
                    item.tag === "人氣" && "bg-orange-100 text-orange-700",
                    item.tag === "招牌" && "bg-blue-100 text-blue-700"
                  )}
                >
                  {item.tag}
                </Badge>
              )}
            </div>

            {/* Row 3: Actions */}
            <div className="flex items-center gap-2 mt-4">
              <Button
                variant="outline"
                size="sm"
                className="h-9 rounded-full px-4 border-charcoal/20 text-charcoal hover:bg-cream-200"
                onClick={onSwap}
                disabled={isSwapping}
              >
                <RotateCw className={cn("w-4 h-4 mr-1.5", isSwapping ? 'animate-spin' : '')} />
                換一道
              </Button>
              <Button
                size="sm"
                className={cn(
                  "flex-1 h-9 rounded-full",
                  isSelected ? "bg-sage hover:bg-sage-700" : "bg-primary hover:bg-primary/90"
                )}
                onClick={() => onSelect(item.dish_name)}
              >
                <CheckCircle2 className="w-4 h-4 mr-1.5" />
                {isSelected ? '已選擇' : '我要點'}
              </Button>
            </div>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
