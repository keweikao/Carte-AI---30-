"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Loader2, Camera, MessageSquare, Search, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

{
    id: 'visual',
        label: 'Visual Agent 正在分析圖片菜單...',
            icon: Camera,
                duration: 3000,
    },
{
    id: 'review',
        label: 'Review Agent 正在分析 Google 評論...',
            icon: MessageSquare,
                duration: 2500,
    },
{
    id: 'search',
        label: 'Search Agent 正在搜尋食記推薦...',
            icon: Search,
                duration: 3500,
    },
{
    id: 'aggregation',
        label: 'Aggregation Agent 正在統整必吃菜單...',
            icon: Sparkles,
                duration: 2000,
    },
];

export function MultiAgentLoader() {
    const [currentStepIndex, setCurrentStepIndex] = useState(0);

    useEffect(() => {
        if (currentStepIndex >= steps.length - 1) return;

        const step = steps[currentStepIndex];
        const timer = setTimeout(() => {
            setCurrentStepIndex((prev) => prev + 1);
        }, step.duration);

        return () => clearTimeout(timer);
    }, [currentStepIndex]);

    return (
        <div className="w-full max-w-md mx-auto p-6 bg-card rounded-xl shadow-lg border border-border">
            <h3 className="text-lg font-semibold text-center mb-6 text-foreground">
                AI 美食特務出動中...
            </h3>
            <div className="space-y-6">
                {steps.map((step, index) => {
                    const isCompleted = index < currentStepIndex;
                    const isCurrent = index === currentStepIndex;
                    const isPending = index > currentStepIndex;

                    return (
                        <div key={step.id} className="flex items-center gap-4">
                            <div className="relative flex items-center justify-center w-8 h-8">
                                <AnimatePresence mode="wait">
                                    {isCompleted ? (
                                        <motion.div
                                            key="completed"
                                            initial={{ scale: 0, opacity: 0 }}
                                            animate={{ scale: 1, opacity: 1 }}
                                            exit={{ scale: 0, opacity: 0 }}
                                        >
                                            <CheckCircle2 className="w-6 h-6 text-green-500" />
                                        </motion.div>
                                    ) : isCurrent ? (
                                        <motion.div
                                            key="current"
                                            initial={{ scale: 0, opacity: 0 }}
                                            animate={{ scale: 1, opacity: 1 }}
                                            exit={{ scale: 0, opacity: 0 }}
                                        >
                                            <Loader2 className="w-6 h-6 text-primary animate-spin" />
                                        </motion.div>
                                    ) : (
                                        <motion.div
                                            key="pending"
                                            initial={{ scale: 0, opacity: 0 }}
                                            animate={{ scale: 1, opacity: 1 }}
                                            exit={{ scale: 0, opacity: 0 }}
                                        >
                                            <div className="w-3 h-3 rounded-full bg-muted" />
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>

                            <div className={cn(
                                "flex items-center gap-3 transition-colors duration-300",
                                isPending ? "text-muted-foreground opacity-50" : "text-foreground"
                            )}>
                                <step.icon className={cn(
                                    "w-5 h-5",
                                    isCurrent && "text-primary animate-pulse"
                                )} />
                                <span className={cn(
                                    "text-sm font-medium",
                                    isCurrent && "text-primary"
                                )}>
                                    {step.label}
                                </span>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
