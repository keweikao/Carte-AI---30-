"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface PriceIndicatorProps {
  priceDiff: number; // The difference in price, e.g., +50, -20
  onComplete: () => void; // Callback when animation is complete
}

export function PriceIndicator({ priceDiff, onComplete }: PriceIndicatorProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (priceDiff !== 0) {
      setIsVisible(true);
      const timer = setTimeout(() => {
        setIsVisible(false);
        onComplete();
      }, 2000); // Auto-hide after 2 seconds
      return () => clearTimeout(timer);
    }
  }, [priceDiff, onComplete]);

  if (!isVisible) return null;

  const isPositive = priceDiff > 0;
  const displaySign = isPositive ? "+" : "";

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.8 }}
          transition={{
            type: "spring",
            stiffness: 260,
            damping: 20,
            duration: 0.3, // Opacity and y animation
            scale: { type: "spring", stiffness: 260, damping: 20, duration: 0.2 } // Scale animation
          }}
          className={cn(
            "fixed bottom-24 left-1/2 -translate-x-1/2 z-50",
            "bg-charcoal text-white px-4 py-2 rounded-full shadow-lg",
            "flex items-center gap-1 font-mono font-bold text-lg",
            isPositive ? "bg-sage" : "bg-terracotta" // Green for positive, red for negative
          )}
        >
          {displaySign}{priceDiff.toLocaleString()}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
