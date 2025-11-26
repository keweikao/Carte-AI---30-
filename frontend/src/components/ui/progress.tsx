import * as React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ProgressProps {
    value: number; // 0 - 100
    complete?: boolean;
    className?: string;
}

export function Progress({ value, complete = false, className }: ProgressProps) {
    const clamped = Math.min(100, Math.max(0, value));

    return (
        <div
            data-slot="progress"
            className={cn(
                "h-2.5 w-full overflow-hidden rounded-full bg-cream-200",
                className
            )}
        >
            <motion.div
                className={cn(
                    "h-full rounded-full",
                    complete
                        ? "bg-sage"
                        : "bg-gradient-to-r from-accent-start to-accent-end"
                )}
                initial={{ width: 0 }}
                animate={{
                    width: `${clamped}%`,
                    scale: complete ? [1, 1.04, 1] : 1,
                }}
                transition={{
                    duration: complete ? 0.8 : 0.5,
                    ease: "easeInOut",
                    repeat: complete ? 2 : 0,
                }}
            />
        </div>
    );
}
