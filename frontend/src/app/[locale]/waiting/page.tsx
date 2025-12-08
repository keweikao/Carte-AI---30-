"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ChefHat, Sparkles, Search, FileText, Brain } from "lucide-react";
import { ProgressBar } from "@/components/carte";

// AI 處理階段
const processingStages = [
    {
        id: "search",
        icon: Search,
        title: "搜尋餐廳資料",
        description: "正在取得最新菜單與評論...",
        duration: 2000
    },
    {
        id: "analyze",
        icon: FileText,
        title: "分析菜單內容",
        description: "解析菜色、價格與特色...",
        duration: 3000
    },
    {
        id: "recommend",
        icon: Brain,
        title: "AI 智慧推薦",
        description: "根據你的偏好計算最佳組合...",
        duration: 2000
    },
    {
        id: "finalize",
        icon: Sparkles,
        title: "組合完美菜單",
        description: "最後調整，馬上完成！",
        duration: 1500
    }
];

export default function WaitingPage() {
    const router = useRouter();
    const searchParams = useSearchParams();

    const [currentStage, setCurrentStage] = useState(0);
    const [jobId, setJobId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    // 取得參數
    const restaurantName = searchParams.get("restaurant") || "";
    const placeId = searchParams.get("place_id");
    const people = parseInt(searchParams.get("people") || "2");
    const mode = searchParams.get("mode") || "sharing";
    const occasion = searchParams.get("occasion") || "friends";
    const dietary = searchParams.get("dietary") || "";

    // 開始推薦 API 請求
    const startRecommendation = useCallback(async () => {
        try {
            const response = await fetch("/api/v1/recommend/v2/async", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    restaurant_name: restaurantName,
                    place_id: placeId,
                    party_size: people,
                    dining_mode: mode,
                    occasion: occasion,
                    dietary_restrictions: dietary ? dietary.split(",") : []
                })
            });

            if (!response.ok) {
                throw new Error("Failed to start recommendation");
            }

            const data = await response.json();
            setJobId(data.job_id);
        } catch (err) {
            setError(err instanceof Error ? err.message : "發生錯誤");
        }
    }, [restaurantName, placeId, people, mode, occasion, dietary]);

    // 輪詢狀態
    const pollStatus = useCallback(async () => {
        if (!jobId) return;

        try {
            const response = await fetch(`/api/v1/recommend/v2/status/${jobId}`);
            const data = await response.json();

            // Update stage based on backend progress
            if (data.progress !== undefined) {
                // Map progress to stages: 0-25% -> stage 0, 25-50% -> stage 1, 50-75% -> stage 2, 75-100% -> stage 3
                const stageFromProgress = Math.min(
                    Math.floor((data.progress / 100) * processingStages.length),
                    processingStages.length - 1
                );
                setCurrentStage(stageFromProgress);
            }

            if (data.status === "completed") {
                // Set to final stage before redirecting
                setCurrentStage(processingStages.length - 1);
                // Small delay to show completion before redirect
                setTimeout(() => {
                    router.push(`/recommendation?job_id=${jobId}`);
                }, 500);
            } else if (data.status === "failed") {
                setError(data.error || "推薦生成失敗");
            }
        } catch (err) {
            console.error("Poll error:", err);
        }
    }, [jobId, router]);

    // 啟動推薦
    useEffect(() => {
        if (restaurantName) {
            startRecommendation();
        }
    }, [restaurantName, startRecommendation]);

    // 輪詢
    useEffect(() => {
        if (!jobId) return;

        const interval = setInterval(pollStatus, 1500);
        return () => clearInterval(interval);
    }, [jobId, pollStatus]);

    // Stage is now driven by backend progress via pollStatus
    // Removed fixed-time simulation

    const stage = processingStages[currentStage];
    const StageIcon = stage.icon;

    // 錯誤狀態
    if (error) {
        return (
            <div className="min-h-screen bg-cream flex items-center justify-center p-4">
                <div className="text-center max-w-md">
                    <div className="w-16 h-16 bg-terracotta/10 rounded-full flex items-center justify-center mx-auto mb-6">
                        <ChefHat className="w-8 h-8 text-terracotta" />
                    </div>
                    <h1 className="font-serif text-2xl font-bold text-charcoal mb-4">
                        發生錯誤
                    </h1>
                    <p className="text-gray-600 mb-8">{error}</p>
                    <button
                        onClick={() => router.back()}
                        className="px-8 py-3 bg-gradient-to-r from-caramel to-terracotta text-white rounded-full font-medium hover:opacity-90 transition-opacity"
                    >
                        返回重試
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-cream flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-md text-center">
                {/* Logo */}
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="mb-8"
                >
                    <div className="inline-flex items-center gap-2">
                        <span className="font-serif text-3xl font-bold text-charcoal">
                            Carte
                        </span>
                        <span className="text-lg font-medium text-caramel">AI</span>
                    </div>
                </motion.div>

                {/* 餐廳名稱 */}
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="text-gray-500 mb-8"
                >
                    正在為 <span className="font-medium text-charcoal">{restaurantName}</span> 準備推薦
                </motion.p>

                {/* 動畫圖示 */}
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentStage}
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.8, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="mb-8"
                    >
                        <div className="w-24 h-24 bg-gradient-to-br from-caramel to-terracotta rounded-full flex items-center justify-center mx-auto shadow-prominent">
                            <StageIcon className="w-12 h-12 text-white" />
                        </div>
                    </motion.div>
                </AnimatePresence>

                {/* 階段標題 */}
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentStage}
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        exit={{ y: -20, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="mb-8"
                    >
                        <h2 className="font-serif text-xl font-bold text-charcoal mb-2">
                            {stage.title}
                        </h2>
                        <p className="text-gray-500">
                            {stage.description}
                        </p>
                    </motion.div>
                </AnimatePresence>

                {/* 進度條 */}
                <div className="mb-8">
                    <ProgressBar
                        currentStep={currentStage + 1}
                        totalSteps={processingStages.length}
                        type="continuous"
                    />
                </div>

                {/* 階段指示器 */}
                <div className="flex justify-center gap-2">
                    {processingStages.map((s, index) => (
                        <div
                            key={s.id}
                            className={`w-2 h-2 rounded-full transition-all duration-300 ${index <= currentStage ? "bg-caramel" : "bg-gray-200"
                                }`}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}
