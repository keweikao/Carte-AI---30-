"use client";

import React, { useState, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { motion, AnimatePresence } from 'framer-motion';
import { RestaurantSearch } from '@/components/restaurant-search';
import { MapPin, Users, Utensils, ChefHat, ChevronLeft, Check } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function InputPageV3() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const { data: session, status } = useSession();
    const error = searchParams.get('error');

    // Current step (1-4)
    const [currentStep, setCurrentStep] = useState(1);

    // Form data
    const [formData, setFormData] = useState({
        restaurant_name: "",
        place_id: undefined as string | undefined,
        mode: "sharing" as "sharing" | "individual",
        people: 2,
        occasion: "friends" as "friends" | "family" | "date" | "business",
        dietary_restrictions: "",
    });

    const updateData = useCallback((key: string, value: string | number | null) => {
        setFormData(prev => ({ ...prev, [key]: value }));
    }, []);

    // Mode options
    const modeOptions = [
        { value: "sharing", label: "分食", icon: Users, description: "一起享用多道菜" },
        { value: "individual", label: "個人", icon: Utensils, description: "各自點餐" }
    ];

    // Occasion options  
    const occasionOptions = [
        { value: "friends", label: "聚餐", icon: "🍻", description: "朋友聚會" },
        { value: "family", label: "家庭", icon: "👨‍👩‍👧‍👦", description: "家人用餐" },
        { value: "date", label: "約會", icon: "💑", description: "浪漫時光" },
        { value: "business", label: "商務", icon: "💼", description: "工作應酬" }
    ];

    // Dietary suggestions
    const dietarySuggestions = [
        "不吃牛", "不吃豬", "不吃辣", "素食", "鍋邊素",
        "清淡口味", "老人友善", "兒童友善", "海鮮過敏"
    ];

    // Navigation
    const canGoNext = () => {
        switch (currentStep) {
            case 1: return formData.restaurant_name !== "";
            case 2: return true; // Mode has default
            case 3: return formData.people > 0;
            case 4: return true; // Occasion/dietary optional
            default: return false;
        }
    };

    const nextStep = () => {
        if (canGoNext() && currentStep < 4) {
            setCurrentStep(prev => prev + 1);
        }
    };

    const prevStep = () => {
        if (currentStep > 1) {
            setCurrentStep(prev => prev - 1);
        }
    };

    const handleSubmit = () => {
        if (!canGoNext()) return;

        const params = new URLSearchParams({
            restaurant: formData.restaurant_name,
            people: formData.people.toString(),
            dietary: formData.dietary_restrictions,
            mode: formData.mode,
            occasion: formData.occasion,
        });

        if (formData.place_id) {
            params.set('place_id', formData.place_id);
        }

        router.push(`/recommendation?${params.toString()}`);
    };

    // Step indicator
    const stepLabels = ["餐廳", "模式", "人數", "偏好"];

    // Redirect if not authenticated
    if (status === 'unauthenticated' && !error) {
        router.push('/');
        return null;
    }

    if (error && error !== 'mock_bypass') {
        return (
            <div className="min-h-screen flex items-center justify-center p-6 bg-cream-50">
                <div className="text-center space-y-4 max-w-md">
                    <p className="text-lg text-charcoal-700">發生錯誤：{error}</p>
                    <button onClick={() => router.push('/')} className="text-caramel hover:underline">
                        返回首頁
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-cream-50 via-white to-cream-100 p-6">
            <div className="max-w-2xl mx-auto pt-8 pb-16">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-3xl sm:text-4xl font-bold text-charcoal mb-3">
                        Dining Concierge
                    </h1>
                    <p className="text-charcoal-600">AI 為您規劃完美的用餐體驗</p>
                </div>

                {/* Step Indicator */}
                <div className="flex items-center justify-center gap-2 mb-12">
                    {stepLabels.map((label, index) => {
                        const stepNum = index + 1;
                        const isActive = stepNum === currentStep;
                        const isCompleted = stepNum < currentStep;

                        return (
                            <React.Fragment key={stepNum}>
                                <button
                                    onClick={() => stepNum < currentStep && setCurrentStep(stepNum)}
                                    disabled={stepNum > currentStep}
                                    className={cn(
                                        "flex items-center gap-2 px-4 py-2 rounded-full transition-all",
                                        isActive && "bg-caramel text-white shadow-lg scale-110",
                                        isCompleted && "bg-caramel/20 text-caramel cursor-pointer hover:bg-caramel/30",
                                        !isActive && !isCompleted && "bg-gray-100 text-gray-400 cursor-not-allowed"
                                    )}
                                >
                                    <span className="text-sm font-semibold">{stepNum}</span>
                                    {isCompleted && <Check className="w-4 h-4" />}
                                    <span className="hidden sm:inline text-sm">{label}</span>
                                </button>
                                {index < stepLabels.length - 1 && (
                                    <div className={cn(
                                        "h-0.5 w-8 transition-colors",
                                        stepNum < currentStep ? "bg-caramel" : "bg-gray-200"
                                    )} />
                                )}
                            </React.Fragment>
                        );
                    })}
                </div>

                {/* Step Content */}
                <div className="bg-white rounded-3xl shadow-xl p-8 sm:p-10 min-h-[400px]">
                    <AnimatePresence mode="wait">
                        {/* Step 1: Restaurant Search */}
                        {currentStep === 1 && (
                            <motion.div
                                key="step1"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="space-y-6"
                            >
                                <div className="text-center mb-8">
                                    <MapPin className="w-12 h-12 text-caramel mx-auto mb-4" />
                                    <h2 className="text-2xl font-bold text-charcoal mb-2">
                                        您想去哪家餐廳？
                                    </h2>
                                    <p className="text-charcoal-600">搜尋並選擇餐廳</p>
                                </div>

                                <RestaurantSearch
                                    name="restaurant_name"
                                    value={formData.restaurant_name}
                                    onSelect={({ name, place_id }) => {
                                        updateData("restaurant_name", name);
                                        if (place_id) {
                                            setFormData(prev => ({ ...prev, place_id }));
                                            // Prefetch
                                            // @ts-expect-error - id_token exists on session
                                            const token = session?.id_token;
                                            if (token && name) {
                                                fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/recommend/v2/prefetch?restaurant_name=${encodeURIComponent(name)}&place_id=${place_id}`, {
                                                    method: 'POST',
                                                    headers: { 'Authorization': `Bearer ${token}` }
                                                }).catch(err => console.error("Prefetch failed:", err));
                                            }
                                        }
                                    }}
                                    onChange={(value) => updateData("restaurant_name", value)}
                                    placeholder="例如：鼎泰豐、海底撈..."
                                    className="text-xl font-semibold border-2 border-gray-200 focus:border-caramel rounded-xl px-6 py-4"
                                />
                            </motion.div>
                        )}

                        {/* Step 2: Mode Selection */}
                        {currentStep === 2 && (
                            <motion.div
                                key="step2"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="space-y-6"
                            >
                                <div className="text-center mb-8">
                                    <Utensils className="w-12 h-12 text-caramel mx-auto mb-4" />
                                    <h2 className="text-2xl font-bold text-charcoal mb-2">
                                        用餐方式
                                    </h2>
                                    <p className="text-charcoal-600">選擇您的用餐模式</p>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    {modeOptions.map((option) => {
                                        const Icon = option.icon;
                                        const isSelected = formData.mode === option.value;

                                        return (
                                            <button
                                                key={option.value}
                                                onClick={() => updateData("mode", option.value)}
                                                className={cn(
                                                    "p-6 rounded-2xl border-2 transition-all text-center space-y-3",
                                                    "hover:scale-105 hover:shadow-lg",
                                                    isSelected
                                                        ? "border-caramel bg-caramel/5 shadow-lg"
                                                        : "border-gray-200 hover:border-caramel/50"
                                                )}
                                            >
                                                <Icon className={cn(
                                                    "w-10 h-10 mx-auto",
                                                    isSelected ? "text-caramel" : "text-gray-400"
                                                )} />
                                                <div>
                                                    <p className={cn(
                                                        "font-bold text-lg mb-1",
                                                        isSelected ? "text-caramel" : "text-charcoal"
                                                    )}>
                                                        {option.label}
                                                    </p>
                                                    <p className="text-sm text-gray-600">{option.description}</p>
                                                </div>
                                            </button>
                                        );
                                    })}
                                </div>
                            </motion.div>
                        )}

                        {/* Step 3: People Count */}
                        {currentStep === 3 && (
                            <motion.div
                                key="step3"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="space-y-6"
                            >
                                <div className="text-center mb-8">
                                    <Users className="w-12 h-12 text-caramel mx-auto mb-4" />
                                    <h2 className="text-2xl font-bold text-charcoal mb-2">
                                        幾位用餐？
                                    </h2>
                                    <p className="text-charcoal-600">讓我們知道人數</p>
                                </div>

                                <div className="flex items-center justify-center gap-6">
                                    <button
                                        onClick={() => formData.people > 1 && updateData("people", formData.people - 1)}
                                        disabled={formData.people <= 1}
                                        className="w-14 h-14 rounded-full bg-gray-100 hover:bg-gray-200 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center text-2xl font-bold text-charcoal transition-all hover:scale-110"
                                    >
                                        −
                                    </button>

                                    <div className="text-center min-w-[120px]">
                                        <div className="text-6xl font-bold text-caramel mb-2">
                                            {formData.people}
                                        </div>
                                        <div className="text-sm text-gray-600">
                                            {formData.people === 1 ? "位" : "位"}
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => updateData("people", formData.people + 1)}
                                        disabled={formData.people >= 20}
                                        className="w-14 h-14 rounded-full bg-caramel hover:bg-caramel-600 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center text-2xl font-bold text-white transition-all hover:scale-110 shadow-lg"
                                    >
                                        +
                                    </button>
                                </div>

                                {/* Quick select */}
                                <div className="flex justify-center gap-3 flex-wrap">
                                    {[2, 4, 6, 8].map(num => (
                                        <button
                                            key={num}
                                            onClick={() => updateData("people", num)}
                                            className={cn(
                                                "px-4 py-2 rounded-full text-sm font-semibold transition-all",
                                                formData.people === num
                                                    ? "bg-caramel text-white shadow-md"
                                                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                                            )}
                                        >
                                            {num} 位
                                        </button>
                                    ))}
                                </div>
                            </motion.div>
                        )}

                        {/* Step 4: Occasion + Dietary */}
                        {currentStep === 4 && (
                            <motion.div
                                key="step4"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="space-y-8"
                            >
                                <div className="text-center mb-6">
                                    <ChefHat className="w-12 h-12 text-caramel mx-auto mb-4" />
                                    <h2 className="text-2xl font-bold text-charcoal mb-2">
                                        告訴我們更多
                                    </h2>
                                    <p className="text-charcoal-600">讓推薦更符合您的需求</p>
                                </div>

                                {/* Occasion */}
                                <div className="space-y-4">
                                    <label className="block text-sm font-semibold text-charcoal-700">
                                        用餐目的
                                    </label>
                                    <div className="grid grid-cols-2 gap-3">
                                        {occasionOptions.map((option) => {
                                            const isSelected = formData.occasion === option.value;

                                            return (
                                                <button
                                                    key={option.value}
                                                    onClick={() => updateData("occasion", option.value)}
                                                    className={cn(
                                                        "p-4 rounded-xl border-2 transition-all text-left",
                                                        "hover:scale-105 hover:shadow-md",
                                                        isSelected
                                                            ? "border-caramel bg-caramel/5"
                                                            : "border-gray-200 hover:border-caramel/50"
                                                    )}
                                                >
                                                    <div className="flex items-center gap-3">
                                                        <span className="text-3xl">{option.icon}</span>
                                                        <div>
                                                            <p className={cn(
                                                                "font-semibold",
                                                                isSelected ? "text-caramel" : "text-charcoal"
                                                            )}>
                                                                {option.label}
                                                            </p>
                                                            <p className="text-xs text-gray-600">{option.description}</p>
                                                        </div>
                                                    </div>
                                                </button>
                                            );
                                        })}
                                    </div>
                                </div>

                                {/* Dietary */}
                                <div className="space-y-4">
                                    <label className="block text-sm font-semibold text-charcoal-700">
                                        飲食偏好 <span className="text-gray-500 font-normal">（選填）</span>
                                    </label>
                                    <input
                                        type="text"
                                        value={formData.dietary_restrictions}
                                        onChange={(e) => updateData("dietary_restrictions", e.target.value)}
                                        placeholder="例如：不吃牛、素食、海鮮過敏..."
                                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-caramel focus:outline-none transition-colors"
                                    />
                                    <div className="flex flex-wrap gap-2">
                                        {dietarySuggestions.map((tag) => (
                                            <button
                                                key={tag}
                                                onClick={() => {
                                                    const current = formData.dietary_restrictions;
                                                    const tags = current ? current.split('、').filter(Boolean) : [];
                                                    if (tags.includes(tag)) {
                                                        updateData("dietary_restrictions", tags.filter(t => t !== tag).join('、'));
                                                    } else {
                                                        updateData("dietary_restrictions", [...tags, tag].join('、'));
                                                    }
                                                }}
                                                className={cn(
                                                    "px-3 py-1.5 rounded-full text-sm font-medium transition-all",
                                                    formData.dietary_restrictions.includes(tag)
                                                        ? "bg-caramel text-white shadow-sm"
                                                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                                                )}
                                            >
                                                {tag}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                {/* Navigation Buttons */}
                <div className="flex items-center justify-between mt-8">
                    <button
                        onClick={prevStep}
                        disabled={currentStep === 1}
                        className={cn(
                            "flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all",
                            currentStep === 1
                                ? "opacity-0 cursor-not-allowed"
                                : "bg-gray-100 hover:bg-gray-200 text-charcoal"
                        )}
                    >
                        <ChevronLeft className="w-5 h-5" />
                        上一步
                    </button>

                    {currentStep < 4 ? (
                        <button
                            onClick={nextStep}
                            disabled={!canGoNext()}
                            className={cn(
                                "px-8 py-3 rounded-xl font-semibold transition-all shadow-lg",
                                canGoNext()
                                    ? "bg-gradient-to-r from-caramel to-terracotta text-white hover:shadow-xl hover:scale-105"
                                    : "bg-gray-200 text-gray-400 cursor-not-allowed"
                            )}
                        >
                            下一步
                        </button>
                    ) : (
                        <button
                            onClick={handleSubmit}
                            className="px-8 py-3 rounded-xl font-semibold bg-gradient-to-r from-caramel to-terracotta text-white shadow-lg hover:shadow-xl hover:scale-105 transition-all"
                        >
                            告訴我該點什麼 ✨
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
