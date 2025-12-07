"use client";

import { motion, AnimatePresence } from "framer-motion";
import { DishCard } from "@/components/dish-card";
import type { MenuItem, DishStatus } from "@/types"; // Import types

interface SwapAnimationProps {
  item: MenuItem | null; // The item to display in the card, can be null during animation
  status: DishStatus; // Status of the item
  onSelect: (dishName: string) => void;
  onSwap: () => void;
  isSwapping: boolean; // Indicates if the card is currently swapping
}

export function SwapAnimation({ item, status, onSelect, onSwap, isSwapping }: SwapAnimationProps) {
  if (!item) return null; // Don't render if item is null

  return (
    <AnimatePresence mode="wait" initial={false}> {/* Use mode="wait" to ensure previous animation finishes */}
      <motion.div
        key={item.dish_name} // Use dish_name as key to trigger exit/enter animations
        initial={{ opacity: 0, x: 200, rotateY: 90 }}
        animate={{ opacity: 1, x: 0, rotateY: 0 }}
        exit={{ opacity: 0, x: -200, rotateY: -90 }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
        className="relative w-full"
      >
        <DishCard 
            item={item} 
            status={status} 
            onSelect={onSelect} 
            onSwap={onSwap} 
            isSwapping={isSwapping} 
        />
      </motion.div>
    </AnimatePresence>
  );
}
