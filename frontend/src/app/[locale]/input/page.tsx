"use client";

import React, { useState, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { motion, AnimatePresence } from 'framer-motion';
import { RestaurantSearch } from '@/components/restaurant-search';
import { MapPin, Users, Utensils, ChefHat, ChevronLeft, Check, ArrowRight } from 'lucide-react';
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
        { value: "sharing", label: "大家分食", icon: Users, description: "適合合菜、熱炒，氣氛熱鬧" },
        { value: "individual", label: "個人套餐", icon: Utensils, description: "拉麵、定食，各自享用" }
    ];

    // Occasion options  
    const occasionOptions = [
        { value: "friends", label: "朋友聚餐", icon: "🍻" },
        { value: "family", label: "家庭聚會", icon: "👨‍👩‍👧‍👦" },
        { value: "date", label: "浪漫約會", icon: "💑" },
        { value: "business", label: "商務應酬", icon: "💼" }
    ];

    // Dietary suggestions
    const dietarySuggestions = [
        "不吃牛", "不吃豬", "不吃辣", "全素", "鍋邊素",
        "少油少鹽", "老人友善", "兒童友善", "海鮮過敏"
    ];

    // Navigation Logic
    const canGoNext = () => {
        switch (currentStep) {
            case 1: return formData.restaurant_name !== "" && formData.place_id !== undefined;
            case 2: return true;
            case 3: return formData.people > 0;
            case 4: return true;
            default: return false;
        }
    };

    const nextStep = () => {
        if (canGoNext() && currentStep < 4) setCurrentStep(prev => prev + 1);
    };

    const prevStep = () => {
        if (currentStep > 1) setCurrentStep(prev => prev - 1);
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
        if (formData.place_id) params.set('place_id', formData.place_id);
        router.push(`/recommendation?${params.toString()}`);
    };



    if (error && error !== 'mock_bypass') {
        return (
            <div className="min-h-screen flex items-center justify-center p-6 bg-[#F9F6F0]">
                <div className="text-center space-y-4 max-w-md">
                    <p className="text-lg text-charcoal-700">發生錯誤：{error}</p>
                    <button onClick={() => router.push('/')} className="text-caramel hover:underline font-bold">
                        返回首頁
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-cream-50 p-4 sm:p-6 flex flex-col justify-center">
            <div className="max-w-xl mx-auto w-full pt-4 pb-12">

                {/* Header - Editorial Style */}
                <div className="text-center mb-8 sm:mb-10">
                    <p className="text-caramel-700 font-bold tracking-[0.2em] text-xs uppercase mb-2">
                        Dining Concierge
                    </p>
                    <h1 className="text-3xl sm:text-4xl font-serif font-bold text-charcoal leading-tight">
                        為您規劃<br />完美的用餐體驗
                    </h1>
                </div>

                {/* Progress Bar */}
                <div className="mb-8 px-2">
                    <div className="flex justify-between mb-2">
                        {["餐廳", "模式", "人數", "偏好"].map((label, idx) => (
                            <span key={idx} className={cn(
                                "text-xs font-bold transition-colors duration-300",
                                currentStep > idx ? "text-caramel-700" :
                                    currentStep === idx + 1 ? "text-charcoal" : "text-gray-300"
                            )}>
                                {label}
                            </span>
                        ))}
                    </div>
                    <div className="h-1.5 w-full bg-gray-200 rounded-full overflow-hidden">
                        <motion.div
                            className="h-full bg-gradient-to-r from-caramel to-terracotta"
                            initial={{ width: "0%" }}
                            animate={{ width: `${(currentStep / 4) * 100}%` }}
                            transition={{ ease: "easeInOut", duration: 0.4 }}
                        />
                    </div>
                </div>

                {/* Main Card */}
                <div className="bg-white rounded-[2rem] shadow-floating border border-white/50 p-6 sm:p-8 min-h-[420px] relative overflow-hidden flex flex-col">
                    <AnimatePresence mode="wait">

                        {/* Step 1: Restaurant Search */}
                        {currentStep === 1 && (
                            <motion.div
                                key="step1"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="flex-1 flex flex-col"
                            >
                                <div className="mb-6">
                                    <h2 className="text-2xl font-serif font-bold text-charcoal mb-2">
                                        您準備在哪間餐廳用餐？
                                    </h2>
                                    <p className="text-gray-500 text-sm">輸入餐廳名稱，AI 將為您解讀菜單</p>
                                </div>

                                <div className="relative z-20">
                                    <RestaurantSearch
                                        name="restaurant_name"
                                        value={formData.restaurant_name}
                                        onSelect={({ name, place_id }) => {
                                            updateData("restaurant_name", name);
                                            if (place_id) {
                                                setFormData(prev => ({ ...prev, place_id }));
                                                // @ts-expect-error - id_token exists on session
                                                const token = session?.id_token;
                                                if (token && name) {
                                                    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/recommend/v2/prefetch?restaurant_name=${encodeURIComponent(name)}&place_id=${place_id}`, {
                                                        method: 'POST',
                                                        headers: { 'Authorization': `Bearer ${token}` }
                                                    }).catch(console.error);
                                                }
                                            }
                                        }}
                                        onChange={(value) => updateData("restaurant_name", value)}
                                        placeholder="例如：鼎泰豐..."
                                        className="text-xl font-bold bg-cream border-2 border-charcoal/10 focus:border-caramel rounded-xl px-5 py-6 shadow-inner placeholder:font-normal"
                                    />
                                </div>
                            </motion.div>
                        )}

                        {/* Step 2: Mode Selection */}
                        {currentStep === 2 && (
                            <motion.div
                                key="step2"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="flex-1"
                            >
                                <div className="mb-6">
                                    <h2 className="text-2xl font-serif font-bold text-charcoal mb-2">
                                        怎麼吃？
                                    </h2>
                                    <p className="text-gray-500 text-sm">選擇您的用餐形式</p>
                                </div>

                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    {modeOptions.map((option) => {
                                        const Icon = option.icon;
                                        const isSelected = formData.mode === option.value;

                                        return (
                                            <button
                                                key={option.value}
                                                onClick={() => updateData("mode", option.value)}
                                                className={cn(
                                                    "p-5 rounded-2xl border-2 transition-all duration-300 text-left relative overflow-hidden group",
                                                    isSelected
                                                        ? "bg-charcoal border-charcoal text-white shadow-lg scale-[1.02]"
                                                        : "bg-white border-gray-200 text-charcoal hover:border-caramel hover:bg-cream-50"
                                                )}
                                            >
                                                <div className="flex items-start justify-between mb-3">
                                                    <Icon className={cn(
                                                        "w-8 h-8",
                                                        isSelected ? "text-caramel" : "text-gray-400 group-hover:text-caramel"
                                                    )} />
                                                    {isSelected && <div className="bg-caramel rounded-full p-1"><Check className="w-3 h-3 text-white" /></div>}
                                                </div>
                                                <div>
                                                    <p className="font-bold text-lg mb-1">{option.label}</p>
                                                    <p className={cn(
                                                        "text-xs",
                                                        isSelected ? "text-gray-300" : "text-gray-500"
                                                    )}>{option.description}</p>
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
                                className="flex-1 flex flex-col justify-center"
                            >
                                <div className="text-center mb-8">
                                    <h2 className="text-2xl font-serif font-bold text-charcoal mb-2">
                                        幾位用餐？
                                    </h2>
                                    <p className="text-gray-500 text-sm">我們會依人數調整份量建議</p>
                                </div>

                                <div className="bg-cream-50 rounded-full p-2 flex items-center justify-between max-w-xs mx-auto w-full border border-gray-200 shadow-inner">
                                    <button
                                        onClick={() => formData.people > 1 && updateData("people", formData.people - 1)}
                                        disabled={formData.people <= 1}
                                        className="w-12 h-12 rounded-full bg-white border border-gray-200 flex items-center justify-center text-xl font-bold text-charcoal shadow-sm hover:scale-105 active:scale-95 disabled:opacity-50 disabled:scale-100 transition-all"
                                    >
                                        −
                                    </button>

                                    <div className="text-center">
                                        <span className="text-4xl font-serif font-bold text-charcoal tabular-nums">
                                            {formData.people}
                                        </span>
                                        <span className="text-gray-500 ml-2 font-medium">位</span>
                                    </div>

                                    <button
                                        onClick={() => updateData("people", formData.people + 1)}
                                        disabled={formData.people >= 20}
                                        className="w-12 h-12 rounded-full bg-charcoal text-white flex items-center justify-center text-xl font-bold shadow-md hover:scale-105 active:scale-95 disabled:opacity-50 disabled:scale-100 transition-all"
                                    >
                                        +
                                    </button>
                                </div>

                                <div className="flex justify-center gap-2 mt-8 flex-wrap">
                                    {[2, 4, 6].map(num => (
                                        <button
                                            key={num}
                                            onClick={() => updateData("people", num)}
                                            className={cn(
                                                "px-4 py-2 rounded-lg text-sm font-bold transition-colors border",
                                                formData.people === num
                                                    ? "bg-caramel text-white border-caramel"
                                                    : "bg-white text-gray-500 border-gray-200 hover:border-caramel/50"
                                            )}
                                        >
                                            {num} 人
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
                                className="flex-1 space-y-8 overflow-y-auto max-h-[50vh] pr-1"
                            >
                                <div className="mb-2">
                                    <h2 className="text-2xl font-serif font-bold text-charcoal mb-2">
                                        最後確認
                                    </h2>
                                    <p className="text-gray-500 text-sm">讓推薦更精準</p>
                                </div>

                                {/* Occasion Grid */}
                                <div className="space-y-3">
                                    <label className="text-sm font-bold text-charcoal uppercase tracking-wider">用餐目的</label>
                                    <div className="grid grid-cols-2 gap-3">
                                        {occasionOptions.map((option) => {
                                            const isSelected = formData.occasion === option.value;
                                            return (
                                                <button
                                                    key={option.value}
                                                    onClick={() => updateData("occasion", option.value)}
                                                    className={cn(
                                                        "p-4 rounded-xl border-2 transition-all flex items-center gap-3",
                                                        isSelected
                                                            ? "bg-charcoal border-charcoal text-white shadow-md"
                                                            : "bg-white border-gray-200 text-charcoal hover:border-caramel"
                                                    )}
                                                >
                                                    <span className="text-2xl">{option.icon}</span>
                                                    <span className="font-bold text-sm">{option.label}</span>
                                                </button>
                                            );
                                        })}
                                    </div>
                                </div>

                                {/* Dietary Pills */}
                                <div className="space-y-3">
                                    <label className="text-sm font-bold text-charcoal uppercase tracking-wider">飲食偏好 (多選)</label>
                                    <div className="flex flex-wrap gap-2">
                                        {dietarySuggestions.map((tag) => {
                                            const current = formData.dietary_restrictions;
                                            const isSelected = current.includes(tag);

                                            return (
                                                <button
                                                    key={tag}
                                                    onClick={() => {
                                                        const tags = current ? current.split('、').filter(Boolean) : [];
                                                        if (isSelected) {
                                                            updateData("dietary_restrictions", tags.filter(t => t !== tag).join('、'));
                                                        } else {
                                                            updateData("dietary_restrictions", [...tags, tag].join('、'));
                                                        }
                                                    }}
                                                    className={cn(
                                                        "px-4 py-2 rounded-full text-sm font-bold border-2 transition-all",
                                                        isSelected
                                                            ? "bg-terracotta border-terracotta text-white shadow-sm"
                                                            : "bg-white border-gray-200 text-charcoal hover:border-terracotta/50"
                                                    )}
                                                >
                                                    {tag}
                                                </button>
                                            )
                                        })}
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Bottom Navigation */}
                    <div className="mt-8 pt-6 border-t border-gray-100 flex items-center justify-between">
                        <button
                            onClick={prevStep}
                            disabled={currentStep === 1}
                            className={cn(
                                "flex items-center gap-2 px-4 py-2 rounded-lg font-bold transition-all text-sm",
                                currentStep === 1
                                    ? "opacity-0 cursor-not-allowed"
                                    : "text-gray-500 hover:text-charcoal hover:bg-gray-100"
                            )}
                        >
                            <ChevronLeft className="w-4 h-4" />
                            上一步
                        </button>

                        {currentStep < 4 ? (
                            <button
                                onClick={nextStep}
                                disabled={!canGoNext()}
                                className={cn(
                                    "flex items-center gap-2 px-8 py-3 rounded-full font-bold transition-all shadow-md",
                                    canGoNext()
                                        ? "bg-charcoal text-white hover:bg-black hover:scale-105"
                                        : "bg-gray-200 text-gray-400 cursor-not-allowed"
                                )}
                            >
                                下一步
                                <ArrowRight className="w-4 h-4" />
                            </button>
                        ) : (
                            <button
                                onClick={handleSubmit}
                                className="flex items-center gap-2 px-8 py-3 rounded-full font-bold bg-gradient-to-r from-caramel to-terracotta text-white shadow-lg hover:shadow-xl hover:scale-105 transition-all"
                            >
                                <ChefHat className="w-5 h-5" />
                                告訴我該點什麼 ✨
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
