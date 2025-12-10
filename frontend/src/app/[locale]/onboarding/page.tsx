"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ChefHat, MessageSquare, Sparkles, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { useLocale } from "next-intl";

const onboardingSteps = [
    {
        icon: ChefHat,
        title: "歡迎來到 Carte AI",
        description: "我們是你的私人點餐顧問，透過 AI 技術為你找出菜單上的最佳選擇。"
    },
    {
        icon: MessageSquare,
        title: "告訴我們你的需求",
        description: "用餐人數、場合、口味偏好——越了解你，推薦越精準。"
    },
    {
        icon: Sparkles,
        title: "獲得個人化推薦",
        description: "AI 會即時分析菜單與評論，為你組合出完美的一餐。"
    }
];

export default function OnboardingPage() {
    const router = useRouter();
    const locale = useLocale();
    const localePrefix = locale || 'zh-TW';
    const [currentStep, setCurrentStep] = useState(0);
    const totalSteps = onboardingSteps.length;

    const handleNext = () => {
        if (currentStep < totalSteps - 1) {
            setCurrentStep(prev => prev + 1);
        } else {
            // Complete onboarding
            localStorage.setItem("carte_onboarded", "true");
            router.push(`/${localePrefix}/input`);
        }
    };

    const handleSkip = () => {
        localStorage.setItem("carte_onboarded", "true");
        router.push(`/${localePrefix}/input`);
    };

    const step = onboardingSteps[currentStep];
    const Icon = step.icon;

    return (
        <div className="min-h-screen bg-cream flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-md">
                {/* Progress Dots */}
                <div className="flex justify-center gap-2 mb-12">
                    {Array.from({ length: totalSteps }).map((_, index) => (
                        <div
                            key={index}
                            className={cn(
                                "h-2 rounded-full transition-all duration-300",
                                index === currentStep
                                    ? "w-8 bg-caramel"
                                    : index < currentStep
                                        ? "w-2 bg-caramel/50"
                                        : "w-2 bg-gray-200"
                            )}
                        />
                    ))}
                </div>

                {/* Step Content */}
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentStep}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.3 }}
                        className="text-center"
                    >
                        {/* Icon */}
                        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-caramel to-terracotta rounded-full mb-8">
                            <Icon className="w-10 h-10 text-white" />
                        </div>

                        {/* Title */}
                        <h1 className="font-serif text-3xl font-bold text-charcoal mb-4">
                            {step.title}
                        </h1>

                        {/* Description */}
                        <p className="text-lg text-gray-600 mb-12 max-w-sm mx-auto">
                            {step.description}
                        </p>
                    </motion.div>
                </AnimatePresence>

                {/* Navigation */}
                <div className="flex items-center justify-between">
                    {/* Skip Button */}
                    <button
                        onClick={handleSkip}
                        className="text-gray-500 hover:text-charcoal transition-colors font-medium"
                    >
                        跳過介紹
                    </button>

                    {/* Next/Start Button */}
                    <button
                        onClick={handleNext}
                        className="inline-flex items-center gap-2 px-8 py-3 text-base font-medium text-white bg-gradient-to-r from-caramel to-terracotta rounded-full hover:opacity-90 hover:shadow-medium transition-all"
                    >
                        {currentStep < totalSteps - 1 ? "下一步" : "開始使用"}
                        <ArrowRight className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}
