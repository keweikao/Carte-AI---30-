"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Utensils, Loader2, Check, BrainCircuit, Lightbulb, Circle, CheckCircle2 } from "lucide-react";

interface GamifiedLoadingStateProps {
    reviewCount: number;
    restaurantName: string;
    analysisSteps: { text: string; icon: string; }[];
    analysisStep: number;
}

const TRIVIA_QUESTIONS = [
    {
        question: "你知道為什麼壽司通常是兩個一組嗎？",
        answer: "因為早期的壽司很大，為了方便食用才切成兩半，後來就演變成兩個一組的習慣！"
    },
    {
        question: "世界上最貴的香料是什麼？",
        answer: "番紅花 (Saffron)，因為採收非常困難，需要大量的人力！"
    },
    {
        question: "凱薩沙拉 (Caesar Salad) 是以凱薩大帝命名的嗎？",
        answer: "不是！是以發明它的義大利主廚 Caesar Cardini 命名的。"
    },
    {
        question: "哪種水果的種子在外面？",
        answer: "草莓！它是唯一種子長在果肉外面的水果。"
    },
    {
        question: "蜂蜜會過期嗎？",
        answer: "純蜂蜜在密封良好的情況下，幾乎永遠不會變質！考古學家曾在埃及古墓發現還能吃的蜂蜜。"
    },
    {
        question: "法式薯條 (French Fries) 是法國人發明的嗎？",
        answer: "其實很有可能是比利時人發明的！"
    },
    {
        question: "辣椒為什麼會辣？",
        answer: "因為含有「辣椒素」，它會欺騙你的大腦，讓你覺得「熱」和「痛」，而不是味覺上的辣。"
    }
];

export function GamifiedLoadingState({ reviewCount, restaurantName, analysisSteps, analysisStep }: GamifiedLoadingStateProps) {
    const [currentTriviaIndex, setCurrentTriviaIndex] = useState(0);
    const [showAnswer, setShowAnswer] = useState(false);

    useEffect(() => {
        // Change trivia every 12 seconds (7s for reading question + 5s for answer)
        const interval = setInterval(() => {
            setShowAnswer(false);
            setTimeout(() => {
                setCurrentTriviaIndex((prev) => (prev + 1) % TRIVIA_QUESTIONS.length);
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
                <motion.div
                    className="absolute inset-0 border-4 border-muted rounded-full"
                />
                <motion.div
                    className="absolute inset-0 border-4 border-primary rounded-full border-t-transparent"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
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
