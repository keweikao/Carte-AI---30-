"use client";

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Utensils, Search, BookOpen, ChefHat, MessageSquare } from 'lucide-react';

interface WaitingScreenProps {
    jobId: string;
    onComplete: (result: unknown) => void;
    onError: (error: string) => void;
}

const TRIVIA_FACTS = [
    "你知道嗎？拉麵最早是從中國傳入日本的，當時被稱為「南京蕎麥麵」。",
    "義大利麵的種類超過 600 種，每種形狀都有其特定的醬汁搭配。",
    "世界上最貴的披薩售價高達 12,000 美元，製作時間需 72 小時。",
    "壽司最初是一種保存魚肉的方法，而不是現在的生魚片料理。",
    "米其林指南最初是為了鼓勵人們多開車旅遊（從而多換輪胎）而發行的。",
    "在法國，麵包是免費供應的，吃完可以無限續加。",
    "韓國人平均每年吃掉的泡菜量超過 20 公斤。",
    "世界上第一家餐廳於 1765 年在巴黎開業，主要販售湯品。",
    "台灣的珍珠奶茶發明於 1980 年代，現在已風靡全球。",
    "在日本吃麵發出聲音被視為對廚師的讚賞，表示麵很好吃。",
];

export default function WaitingScreen({ jobId, onComplete, onError }: WaitingScreenProps) {
    const [progress, setProgress] = useState(0);
    const [statusMessage, setStatusMessage] = useState("準備中...");
    const [triviaIndex, setTriviaIndex] = useState(0);

    // Polling logic
    useEffect(() => {
        const pollInterval = setInterval(async () => {
            try {
                const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://dining-backend-1045148759148.asia-east1.run.app';
                const response = await fetch(`${apiUrl}/v2/recommendations/status/${jobId}`);

                if (!response.ok) {
                    // Handle 404 or other errors gracefully
                    if (response.status === 404) {
                        console.warn("Job not found yet, retrying...");
                        return;
                    }
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();

                if (data.status === 'completed') {
                    clearInterval(pollInterval);
                    setProgress(100);
                    setStatusMessage("分析完成！");
                    setTimeout(() => onComplete(data.result), 500); // Small delay for UX
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval);
                    onError(data.error || 'Unknown error occurred');
                } else {
                    // Update progress based on backend or simulate progress
                    const backendProgress = data.progress || 0;
                    // Smooth progress update (don't jump backwards)
                    setProgress(prev => Math.max(prev, backendProgress));

                    // Update message based on progress
                    if (backendProgress < 10) setStatusMessage("準備中...");
                    else if (backendProgress < 30) setStatusMessage("正在搜尋餐廳資料...");
                    else if (backendProgress < 60) setStatusMessage("正在分析菜單...");
                    else if (backendProgress < 90) setStatusMessage("正在閱讀顧客評論...");
                    else setStatusMessage("正在為您量身打造推薦...");
                }
            } catch (error) {
                console.error("Polling error:", error);
                // Don't stop polling on transient network errors
            }
        }, 3000);

        return () => clearInterval(pollInterval);
    }, [jobId, onComplete, onError]);

    // Trivia rotation (Random)
    useEffect(() => {
        // Initial random fact
        setTriviaIndex(Math.floor(Math.random() * TRIVIA_FACTS.length));

        const triviaInterval = setInterval(() => {
            setTriviaIndex((prev: number) => {
                let nextIndex;
                do {
                    nextIndex = Math.floor(Math.random() * TRIVIA_FACTS.length);
                } while (nextIndex === prev && TRIVIA_FACTS.length > 1); // Avoid same fact twice in a row
                return nextIndex;
            });
        }, 8000);
        return () => clearInterval(triviaInterval);
    }, []);

    // Icon based on progress
    const getIcon = () => {
        if (progress < 10) return <Utensils className="w-12 h-12 text-caramel" />;
        if (progress < 30) return <Search className="w-12 h-12 text-caramel" />;
        if (progress < 60) return <BookOpen className="w-12 h-12 text-caramel" />;
        if (progress < 90) return <MessageSquare className="w-12 h-12 text-caramel" />;
        return <ChefHat className="w-12 h-12 text-caramel" />;
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] p-6 bg-cream-50 rounded-card shadow-card max-w-md mx-auto border border-cream-200">
            {/* Icon Animation */}
            <motion.div
                key={statusMessage} // Triggers animation on change
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                transition={{ type: "spring", stiffness: 260, damping: 20 }}
                className="mb-8 p-6 bg-white rounded-full shadow-floating border border-caramel-50"
            >
                {getIcon()}
            </motion.div>

            {/* Status Message */}
            <h2 className="text-xl font-display font-bold text-charcoal mb-2 text-center">
                {statusMessage}
            </h2>

            <p className="text-charcoal-700 text-sm mb-6 text-center opacity-80">
                AI 正在努力工作中，請稍候...
            </p>

            {/* Progress Bar */}
            <div className="w-full h-2 bg-caramel-100 rounded-full mb-8 overflow-hidden">
                <motion.div
                    className="h-full bg-caramel"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.5, ease: "easeInOut" }}
                />
            </div>

            {/* Trivia Card */}
            <AnimatePresence mode="wait">
                <motion.div
                    key={triviaIndex}
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    exit={{ y: -20, opacity: 0 }}
                    transition={{ duration: 0.5 }}
                    className="bg-white p-6 rounded-lg shadow-sm border border-caramel-100 w-full relative overflow-hidden"
                >
                    <div className="absolute top-0 left-0 w-1 h-full bg-terracotta" />
                    <div className="flex items-center mb-2">
                        <span className="text-xs font-bold text-terracotta uppercase tracking-wider flex items-center gap-1">
                            <span className="text-lg">💡</span> 冷知識時間
                        </span>
                    </div>
                    <p className="text-charcoal-700 text-sm leading-relaxed font-body">
                        {TRIVIA_FACTS[triviaIndex]}
                    </p>
                </motion.div>
            </AnimatePresence>
        </div>
    );
}
