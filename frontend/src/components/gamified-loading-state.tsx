"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Utensils, Loader2, Check, BrainCircuit, Lightbulb, Circle, CheckCircle2 } from "lucide-react";

import { TRIVIA_QUESTIONS } from "../data/trivia";

interface GamifiedLoadingStateProps {
    reviewCount: number;
    restaurantName: string;
    analysisSteps: { text: string; icon: string; }[];
    analysisStep: number;
}

export function GamifiedLoadingState({ reviewCount, restaurantName, analysisSteps, analysisStep }: GamifiedLoadingStateProps) {
    // Start with a random question
    const [currentTriviaIndex, setCurrentTriviaIndex] = useState(() => Math.floor(Math.random() * TRIVIA_QUESTIONS.length));
    const [showAnswer, setShowAnswer] = useState(false);

    useEffect(() => {
        // Change trivia every 12 seconds (7s for reading question + 5s for answer)
        const interval = setInterval(() => {
            setShowAnswer(false);
            setTimeout(() => {
                setCurrentTriviaIndex((prev) => {
                    // Ensure we don't repeat the same question immediately
                    let nextIndex = Math.floor(Math.random() * TRIVIA_QUESTIONS.length);
                    while (nextIndex === prev && TRIVIA_QUESTIONS.length > 1) {
                        nextIndex = Math.floor(Math.random() * TRIVIA_QUESTIONS.length);
                    }
                    return nextIndex;
                });
            }, 500); // Wait for exit animation
        }, 12000);

        return () => clearInterval(interval);
    }, []);

    // Show answer after 7 seconds
    useEffect(() => {
        const timer = setTimeout(() => {
            setShowAnswer(true);
        }, 7000);
        return () => clearTimeout(timer);
    }, [currentTriviaIndex]);

    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 text-center space-y-8 relative overflow-hidden" role="status" aria-live="polite">
            {/* Background Decoration Removed to fix visual glitch */}

            {/* Main Loading Animation */}
            <div className="relative w-32 h-32 flex items-center justify-center z-10">
                {/* Background circle */}
                <motion.div
                    className="absolute inset-0 border-[6px] border-muted/30 rounded-full"
                />
                {/* Rotating progress arc */}
                <motion.div
                    className="absolute inset-0 border-[6px] rounded-full"
                    style={{
                        borderColor: 'transparent',
                        borderTopColor: 'hsl(var(--primary))',
                        borderRightColor: 'hsl(var(--primary))',
                    }}
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                />
                <Utensils className="w-12 h-12 text-primary" />
            </div>

            <div className="space-y-2 max-w-sm mx-auto z-10">
                <h2 className="text-2xl font-bold text-foreground">
                    AI 正在為您精選美食...
                </h2>
                <p className="text-muted-foreground text-sm">
                    已分析 <motion.span
                        key={reviewCount}
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="font-mono font-bold text-primary"
                    >
                        {reviewCount}
                    </motion.span> 則評論，正在閱讀 {restaurantName} 的菜單照片
                </p>
            </div>

            {/* Progress Steps */}
            <div className="w-full max-w-md bg-secondary/30 backdrop-blur-sm rounded-xl p-4 space-y-3 z-10 border border-border/50">
                {analysisSteps.map((step, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: analysisStep > index ? 1 : 0.4, x: analysisStep > index ? 0 : -10 }}
                        className="flex items-center gap-3"
                    >
                        <div className="w-6 h-6 flex items-center justify-center">
                            {analysisStep > index ? (
                                <CheckCircle2 className="w-5 h-5 text-green-500" />
                            ) : analysisStep === index ? (
                                <Loader2 className="w-5 h-5 text-primary animate-spin" />
                            ) : (
                                <Circle className="w-4 h-4 text-muted-foreground" />
                            )}
                        </div>
                        <span className={`text-sm font-medium ${analysisStep >= index ? "text-foreground" : "text-muted-foreground"}`}>
                            {step.text}
                        </span>
                    </motion.div>
                ))}
            </div>

            {/* Gamified Trivia Section */}
            <motion.div
                className="w-full max-w-md mt-8 p-6 bg-card rounded-xl shadow-lg border border-primary/20 relative overflow-hidden z-10"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
            >
                <div className="absolute top-0 left-0 w-full h-1 bg-secondary">
                    <motion.div
                        className="h-full bg-primary"
                        initial={{ width: "0%" }}
                        animate={{ width: "100%" }}
                        transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                    />
                </div>

                <div className="flex items-center gap-2 mb-3 text-primary">
                    <Lightbulb className="w-5 h-5" />
                    <span className="text-sm font-bold uppercase tracking-wider">等待時的小知識</span>
                </div>

                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentTriviaIndex}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className="min-h-[100px] flex flex-col justify-center"
                    >
                        <h3 className="text-lg font-bold text-foreground mb-2">
                            {TRIVIA_QUESTIONS[currentTriviaIndex].question}
                        </h3>
                        {showAnswer && (
                            <motion.p
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: "auto" }}
                                className="text-muted-foreground text-sm"
                            >
                                {TRIVIA_QUESTIONS[currentTriviaIndex].answer}
                            </motion.p>
                        )}
                    </motion.div>
                </AnimatePresence>
            </motion.div>
        </div>
    );
}
