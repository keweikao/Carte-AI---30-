"use client";

import { useState, useEffect, Suspense, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import { AlertDialog, AlertDialogContent, AlertDialogDescription, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { ArrowRight, Check, Utensils, Sparkles, Users, AlertCircle, ArrowLeft, User, Briefcase, Heart, Dumbbell, Home, Zap, Compass } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import { RestaurantSearch } from "@/components/restaurant-search";
import { PricingModal } from "@/components/pricing-modal";
import { TagInput } from "@/components/tag-input"; // New import

function InputPageContents() {
    // --- HOOKS ---
    const { data: session, status } = useSession();
    const router = useRouter();
    const searchParams = useSearchParams();
    const error = searchParams.get('error');

    const [step, setStep] = useState(1);
    const [showPricingModal, setShowPricingModal] = useState(false); // New state
    const [formData, setFormData] = useState<{
        restaurant_name: string;
        place_id?: string;
        people: number;
        budget: string;
        dietary_restrictions: string;
        mode: "sharing" | "individual";
        occasion: "business" | "date" | "family" | "friends" | "fitness";
        dish_count: number | null;
    }>({
        restaurant_name: "",
        place_id: undefined,
        people: 2,
        budget: "200",
        dietary_restrictions: "",
        mode: "sharing",
        occasion: "friends",
        dish_count: null
    });
    const [budgetType, setBudgetType] = useState<"person" | "total">("person");
    const [dishCountWarning, setDishCountWarning] = useState<string | null>(null);

    // --- FUNCTIONS ---
    const updateData = useCallback((key: string, value: string | number | null) => {
        setFormData(prev => ({ ...prev, [key]: value }));
    }, []);

    const validateDishCount = (count: number | null, people: number): { valid: boolean; message?: string } => {
        if (!count) return { valid: true };

        const minDishes = Math.max(1, Math.floor(people * 0.8));
        const maxDishes = people * 3;

        if (count < minDishes) {
            return {
                valid: false,
                message: `建議至少點 ${minDishes} 道菜，才能滿足 ${people} 人份量`
            };
        }

        if (count > maxDishes) {
            return {
                valid: false,
                message: `${count} 道菜對 ${people} 人來說可能太多了，建議不超過 ${maxDishes} 道`
            };
        }

        return { valid: true };
    };

    const handleNext = useCallback(() => {
        if (step === 1 && formData.restaurant_name) {
            setStep(2);
        } else if (step === 2) {
            // 驗證菜品數量
            if (formData.dish_count) {
                const validation = validateDishCount(formData.dish_count, formData.people);
                if (!validation.valid && validation.message) {
                    setDishCountWarning(validation.message);
                    return;
                }
            }

            const params = new URLSearchParams({
                restaurant: formData.restaurant_name,
                people: formData.people.toString(),
                budget: formData.budget,
                dietary: formData.dietary_restrictions,
                mode: formData.mode,
                occasion: formData.occasion, // Add occasion here
                budget_type: budgetType,
                ...(formData.dish_count && { dish_count: formData.dish_count.toString() }),
                ...(formData.place_id && { place_id: formData.place_id })
            });
            router.push(`/recommendation?${params.toString()}`);
        }
    }, [step, formData, router, budgetType]);

    // --- EFFECTS ---
    useEffect(() => {
        if (status === "unauthenticated" && !error) {
            router.push("/");
        }
    }, [status, error, router]);

    // 從 URL 參數預填表單
    useEffect(() => {
        const restaurant = searchParams.get("restaurant");
        const people = searchParams.get("people");
        const budget = searchParams.get("budget");
        const dietary = searchParams.get("dietary");
        const mode = searchParams.get("mode");
        const dishCount = searchParams.get("dish_count");

        if (restaurant || people || budget) {
            const parsedPeople = people ? parseInt(people) : 2;
            // 將 URL 參數的 mode 轉換為內部使用的類型
            const urlMode = mode as "solo" | "sharing" | "individual" | null;
            const parsedMode: "sharing" | "individual" =
                (urlMode === "solo" || urlMode === "individual") ? "individual" : "sharing";

            // 根據模式調整人數
            const adjustedPeople = parsedMode === "individual" ? 1 :
                (parsedMode === "sharing" && parsedPeople === 1) ? 4 : parsedPeople;

            // 如果有餐廳名稱，直接進入第二步
            if (restaurant) {
                setTimeout(() => setStep(2), 0);
            }

            // Update form data (wrapped in setTimeout to avoid synchronous state update warning)
            setTimeout(() => {
                setFormData({
                    restaurant_name: restaurant || "",
                    people: adjustedPeople,
                    budget: budget || "",
                    dietary_restrictions: dietary || "",
                    mode: parsedMode,
                    occasion: "friends", // Default to friends if not specified
                    dish_count: dishCount ? parseInt(dishCount) : null
                });
            }, 0);
        }
    }, [searchParams]);

    // 當模式改變時調整人數
    useEffect(() => {
        setTimeout(() => {
            if (formData.mode === "individual" && formData.people !== 1) {
                setFormData(prev => ({ ...prev, people: 1 }));
            } else if (formData.mode === "sharing" && formData.people === 1) {
                setFormData(prev => ({ ...prev, people: 4 }));
            }
        }, 0);
    }, [formData.mode, formData.people]);

    // --- CONDITIONAL RENDERING ---
    if (error) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center space-y-4 bg-background" role="alert" aria-live="assertive">
                <AlertCircle className="w-16 h-16 text-destructive" aria-hidden="true" />
                <h2 className="text-2xl font-bold text-foreground">登入失敗</h2>
                <p className="text-muted-foreground">無法登入您的 Google 帳戶。請檢查您的網路連線或稍後再試。</p>
                <p className="text-sm text-destructive" role="status">錯誤訊息: {error}</p>
                <Button onClick={() => {
                    window.location.href = "/input";
                }} aria-label="重新嘗試登入">重試</Button>
            </div>
        )
    }

    if (status === "loading") {
        return (
            <div className="flex min-h-screen items-center justify-center bg-background">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary" role="status" aria-label="載入中">
                    <span className="sr-only">載入中...</span>
                </div>
            </div>
        );
    }

    if (!session) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-background">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary" role="status" aria-label="載入中">
                    <span className="sr-only">載入中...</span>
                </div>
            </div>
        );
    }

    // --- FULL COMPONENT RENDER ---
    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 sm:p-6 font-sans relative overflow-hidden">
            <PricingModal
                isOpen={showPricingModal}
                onClose={() => setShowPricingModal(false)}
                currentCredits={0}
            />

            {/* Temporary Demo Button */}
            <div className="absolute top-4 right-4 z-50">
                <Button variant="outline" size="sm" onClick={() => setShowPricingModal(true)}>
                    💎 升級方案
                </Button>
            </div>

            {/* Background Decoration */}
            <div className="w-full max-w-md">
                <AnimatePresence mode="wait">
                    {/* Step 1: Restaurant Name */}
                    {step === 1 && (
                        <motion.div
                            key="step1"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-8"
                            role="region"
                            aria-label="步驟一：選擇餐廳"
                        >
                            <div className="space-y-2 text-center">

                                <h2 className="text-2xl font-bold">不知道怎麼點？</h2>
                                <p className="text-muted-foreground">輸入餐廳名稱，AI 根據 Google Map 及實際評價幫你推薦菜色。</p>
                            </div>

                            <div className="space-y-4">
                                <div role="group" aria-labelledby="restaurant-input-label">
                                    <label id="restaurant-input-label" className="sr-only">餐廳名稱</label>
                                    <RestaurantSearch
                                        onSelect={({ name, place_id }) => {
                                            updateData("restaurant_name", name);
                                            if (place_id) {
                                                setFormData(prev => ({ ...prev, place_id }));
                                            }
                                            if (name) {
                                                setStep(2);
                                            }
                                        }}
                                        onChange={(value) => {
                                            updateData("restaurant_name", value);
                                        }}
                                        defaultValue={formData.restaurant_name}
                                    />
                                </div>
                                <Button
                                    className="w-full py-6 text-lg bg-primary hover:bg-primary/90"
                                    onClick={handleNext}
                                    disabled={!formData.restaurant_name}
                                    aria-label="繼續到下一步，設定用餐偏好"
                                >
                                    下一步 <ArrowRight className="ml-2 w-5 h-5" aria-hidden="true" />
                                </Button>
                            </div>
                        </motion.div>
                    )}

                    {/* Step 2: Preferences (Combined) */}
                    {step === 2 && (
                        <motion.div
                            key="step2"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="w-full space-y-8 pb-8"
                            role="region"
                            aria-label="步驟二：設定用餐偏好"
                        >
                            {/* 返回按鈕 */}
                            <Button
                                variant="ghost"
                                onClick={() => setStep(1)}
                                className="gap-2 mb-4"
                                aria-label="返回上一步"
                            >
                                <ArrowLeft className="w-4 h-4" />
                                返回
                            </Button>

                            <div className="space-y-2 text-center">
                                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4" aria-hidden="true">
                                    <Sparkles className="text-primary w-6 h-6" />
                                </div>
                                <h2 className="text-2xl font-bold">開啟你的美食探索之旅</h2>
                                <p className="text-muted-foreground">告訴我們你的喜好。</p>
                            </div>

                            <div className="space-y-8">
                                {/* Dining Style (Moved to Top) */}
                                <div className="space-y-3">
                                    <Label className="text-base">用餐方式</Label>
                                    <RadioGroup
                                        defaultValue={formData.mode}
                                        onValueChange={(val) => updateData("mode", val)}
                                        className="grid grid-cols-2 gap-4"
                                    >
                                        <div>
                                            <RadioGroupItem value="sharing" id="sharing" className="peer sr-only" />
                                            <Label
                                                htmlFor="sharing"
                                                className="flex flex-col items-center justify-center gap-2 rounded-xl border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary peer-data-[state=checked]:bg-primary/5 cursor-pointer transition-all"
                                            >
                                                <Users className="h-5 w-5" />
                                                <span className="font-medium">大家一起分食</span>
                                            </Label>
                                        </div>
                                        <div>
                                            <RadioGroupItem value="individual" id="individual" className="peer sr-only" />
                                            <Label
                                                htmlFor="individual"
                                                className="flex flex-col items-center justify-center gap-2 rounded-xl border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary peer-data-[state=checked]:bg-primary/5 cursor-pointer transition-all"
                                            >
                                                <Utensils className="h-5 w-5" />
                                                <span className="font-medium">個人套餐</span>
                                            </Label>
                                        </div>
                                    </RadioGroup>
                                </div>

                                {/* Occasion (Contextual) */}
                                <div className="space-y-3">
                                    <Label className="text-base">用餐情境</Label>
                                    <RadioGroup
                                        defaultValue={formData.occasion}
                                        onValueChange={(val) => updateData("occasion", val)}
                                        className="grid grid-cols-2 sm:grid-cols-4 gap-2"
                                    >
                                        {(formData.mode === "individual" ? [
                                            { id: "quick", label: "快速解決", icon: Zap },
                                            { id: "treat", label: "犒賞自己", icon: Sparkles },
                                            { id: "fitness", label: "健身減脂", icon: Dumbbell },
                                            { id: "adventure", label: "全新探險", icon: Compass },
                                        ] : [
                                            { id: "friends", label: "朋友聚會", icon: Users },
                                            { id: "family", label: "家庭聚餐", icon: Home },
                                            { id: "date", label: "約會慶祝", icon: Heart },
                                            { id: "business", label: "商務聚餐", icon: Briefcase },
                                        ]).map((item) => (
                                            <div key={item.id}>
                                                <RadioGroupItem value={item.id} id={`occasion-${item.id}`} className="peer sr-only" />
                                                <Label
                                                    htmlFor={`occasion-${item.id}`}
                                                    className="flex flex-col items-center justify-center gap-2 rounded-xl border-2 border-muted bg-popover p-3 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary peer-data-[state=checked]:bg-primary/5 cursor-pointer transition-all h-full"
                                                >
                                                    <item.icon className="h-5 w-5" />
                                                    <span className="text-sm font-medium text-center">{item.label}</span>
                                                </Label>
                                            </div>
                                        ))}
                                    </RadioGroup>
                                </div>

                                {/* People Count */}
                                <div className="space-y-3">
                                    <Label htmlFor="people-count" className="text-base">幾位用餐？</Label>
                                    <div className="flex items-center justify-between bg-secondary/30 p-4 rounded-xl" role="group" aria-labelledby="people-count">
                                        <span className="text-sm text-muted-foreground">人數</span>
                                        <div className="flex items-center space-x-4">
                                            <Button
                                                variant="outline"
                                                size="icon"
                                                className="h-8 w-8 rounded-full"
                                                onClick={() => updateData("people", Math.max(1, formData.people - 1))}
                                                aria-label="減少用餐人數"
                                                disabled={formData.people <= 1}
                                            >
                                                -
                                            </Button>
                                            <span className="text-xl font-bold w-6 text-center" id="people-count" aria-live="polite">{formData.people}</span>
                                            <Button
                                                variant="outline"
                                                size="icon"
                                                className="h-8 w-8 rounded-full"
                                                onClick={() => updateData("people", formData.people + 1)}
                                                aria-label="增加用餐人數"
                                            >
                                                +
                                            </Button>
                                        </div>
                                    </div>
                                </div>

                                {/* Budget */}
                                <div className="space-y-3">
                                    <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
                                        <Label htmlFor="budget" className="text-base">
                                            {budgetType === "person" ? "每人預算 (客單價)" : "總預算"}
                                        </Label>
                                        <div className="flex bg-secondary/50 rounded-lg p-1" role="group" aria-label="預算計算方式">
                                            <button
                                                type="button"
                                                className={`flex items-center gap-1.5 px-3 py-2 text-sm rounded-md transition-all cursor-pointer ${budgetType === "person" ? "bg-white shadow-md text-foreground font-semibold border-2 border-primary" : "text-muted-foreground hover:bg-white/50 hover:text-foreground border-2 border-transparent"}`}
                                                onClick={() => setBudgetType("person")}
                                                aria-label="選擇每人預算模式"
                                                aria-pressed={budgetType === "person"}
                                            >
                                                <User className="w-4 h-4" />
                                                每人(客單)
                                            </button>
                                            <button
                                                type="button"
                                                className={`flex items-center gap-1.5 px-3 py-2 text-sm rounded-md transition-all cursor-pointer ${budgetType === "total" ? "bg-white shadow-md text-foreground font-semibold border-2 border-primary" : "text-muted-foreground hover:bg-white/50 hover:text-foreground border-2 border-transparent"}`}
                                                onClick={() => setBudgetType("total")}
                                                aria-label="選擇總預算模式"
                                                aria-pressed={budgetType === "total"}
                                            >
                                                <Users className="w-4 h-4" />
                                                總預算
                                            </button>
                                        </div>
                                    </div>
                                    <div className="space-y-3 pt-2">
                                        <div className="px-1">
                                            <Slider
                                                id="budget"
                                                value={[Number(formData.budget) || (budgetType === 'person' ? 500 : 2000)]}
                                                onValueChange={(value) => updateData("budget", String(value[0]))}
                                                max={budgetType === 'person' ? 3000 : 10000}
                                                step={budgetType === 'person' ? 50 : 250}
                                            />
                                        </div>
                                        <div className="flex justify-between text-xs text-muted-foreground px-1 items-center">
                                            <span>NT$ 0</span>
                                            <div className="flex items-center gap-1">
                                                <span className="font-mono text-sm font-semibold text-primary">NT$</span>
                                                <Input
                                                    type="number"
                                                    value={formData.budget}
                                                    onChange={(e) => {
                                                        const val = e.target.value;
                                                        // Allow empty string for typing, otherwise parse
                                                        updateData("budget", val);
                                                    }}
                                                    className="h-8 w-24 text-center font-mono font-semibold text-primary bg-primary/10 border-none focus:ring-1 focus:ring-primary"
                                                    placeholder="例如：500"
                                                />
                                            </div>
                                            <span>NT$ {budgetType === 'person' ? "3,000+" : "10,000+"}</span>
                                        </div>
                                    </div>
                                </div>

                                {/* Dish Count (Optional) */}
                                <div className="space-y-3">
                                    <Label className="text-base">想要幾道菜？（選填）</Label>
                                    <div className="flex items-center gap-2">
                                        <Input
                                            type="number"
                                            min="1"
                                            placeholder="留空則由 AI 決定"
                                            value={formData.dish_count || ""}
                                            onChange={(e) => updateData("dish_count", e.target.value ? parseInt(e.target.value) : null)}
                                            className="bg-secondary/30 border-transparent focus:border-primary"
                                        />
                                        <span className="text-muted-foreground">道</span>
                                    </div>
                                    <p className="text-xs text-muted-foreground flex items-center gap-1">
                                        💡 不填的話，AI 會根據人數和預算自動決定
                                    </p>
                                </div>

                                {/* Dietary */}
                                <div className="space-y-3">
                                    <Label className="text-base">飲食禁忌與偏好</Label>
                                    <TagInput
                                        value={formData.dietary_restrictions.split(',').map(s => s.trim()).filter(Boolean)}
                                        onChange={(tags) => updateData("dietary_restrictions", tags.join(", "))}
                                        suggestions={[
                                            { id: "no_beef", label: "不吃牛", icon: "🥩" },
                                            { id: "no_pork", label: "不吃豬", icon: "🐷" },
                                            { id: "no_seafood", label: "不吃海鮮", icon: "🦐" },
                                            { id: "vegetarian", label: "素食", icon: "🥬" },
                                            { id: "no_spicy", label: "不吃辣", icon: "🚫" },
                                            { id: "no_cilantro", label: "不吃香菜", icon: "🌿" },
                                        ]}
                                        placeholder="例如：不吃花生、奶蛋素..."
                                    />
                                    <Textarea
                                        placeholder="還有什麼特別需求都可以告訴我，例如：不吃牛、怕過敏、偏好當季食材..."
                                        value={formData.dietary_restrictions}
                                        onChange={(e) => updateData("dietary_restrictions", e.target.value)}
                                        className="h-24 bg-secondary/30 border-transparent focus:border-primary resize-none"
                                    />
                                </div>

                                <Button
                                    className="w-full py-6 text-lg bg-primary hover:bg-primary/90 shadow-lg shadow-primary/20 rounded-xl"
                                    onClick={handleNext}
                                    disabled={!formData.budget}
                                    aria-label="完成設定並開始生成推薦菜單"
                                >
                                    開始生成推薦 <Check className="ml-2 w-5 h-5" aria-hidden="true" />
                                </Button>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* 警告對話框 */}
            <AlertDialog open={!!dishCountWarning} onOpenChange={() => setDishCountWarning(null)}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>菜品數量建議</AlertDialogTitle>
                        <AlertDialogDescription>{dishCountWarning}</AlertDialogDescription>
                    </AlertDialogHeader>
                    <div className="flex gap-3 mt-4">
                        <Button
                            variant="outline"
                            className="flex-1"
                            onClick={() => {
                                setDishCountWarning(null);
                                // 不做任何事，留在當前頁面讓用戶修改
                            }}
                        >
                            那我改一下
                        </Button>
                        <Button
                            className="flex-1 bg-primary"
                            onClick={() => {
                                setDishCountWarning(null);
                                // 繼續提交，執行原本的導航邏輯
                                const params = new URLSearchParams({
                                    restaurant: formData.restaurant_name,
                                    people: formData.people.toString(),
                                    budget: formData.budget,
                                    dietary: formData.dietary_restrictions,
                                    mode: formData.mode,
                                    budget_type: budgetType, // Add budget_type here

                                    ...(formData.dish_count && { dish_count: formData.dish_count.toString() })
                                });
                                router.push(`/recommendation?${params.toString()}`);
                            }}
                        >
                            就是要點
                        </Button>
                    </div>
                </AlertDialogContent>
            </AlertDialog>
        </div>
    );
}

export default function InputPage() {
    return (
        <Suspense fallback={
            <div className="flex min-h-screen items-center justify-center bg-background">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
            </div>
        }>
            <InputPageContents />
        </Suspense>
    );
}