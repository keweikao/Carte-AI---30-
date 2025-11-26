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
import { ArrowRight, Check, Utensils, Sparkles, Users, AlertCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { RestaurantSearch } from "@/components/restaurant-search";
import { TagInput } from "@/components/tag-input"; // New import

function InputPageContents() {
    // --- HOOKS ---
    const { data: session, status } = useSession();
    const router = useRouter();
    const searchParams = useSearchParams();
    const error = searchParams.get('error');

    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState<{
        restaurant_name: string;
        people: number;
        budget: string;
        dietary_restrictions: string;
        mode: "sharing" | "individual";
        dish_count: number | null;
    }>({
        restaurant_name: "",
        people: 2,
        budget: "",
        dietary_restrictions: "",
        mode: "sharing",
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
                ...(formData.dish_count && { dish_count: formData.dish_count.toString() })
            });
            router.push(`/recommendation?${params.toString()}`);
        }
    }, [step, formData, router]);

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

            setFormData({
                restaurant_name: restaurant || "",
                people: adjustedPeople,
                budget: budget || "",
                dietary_restrictions: dietary || "",
                mode: parsedMode,
                dish_count: dishCount ? parseInt(dishCount) : null
            });

            // 如果有餐廳名稱，直接進入第二步
            if (restaurant) {
                setStep(2);
            }
        }
    }, [searchParams]);

    // 當模式改變時調整人數
    // eslint-disable-next-line react-hooks/exhaustive-deps
    useEffect(() => {
        if (formData.mode === "individual" && formData.people !== 1) {
            setFormData(prev => ({ ...prev, people: 1 }));
        } else if (formData.mode === "sharing" && formData.people === 1) {
            setFormData(prev => ({ ...prev, people: 4 }));
        }
    }, [formData.mode, formData.people]);

    // --- CONDITIONAL RENDERING ---
    if (error) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center space-y-4 bg-background">
                <AlertCircle className="w-16 h-16 text-destructive" />
                <h2 className="text-2xl font-bold text-foreground">登入失敗</h2>
                <p className="text-muted-foreground">無法登入您的 Google 帳戶。請檢查您的網路連線或稍後再試。</p>
                <p className="text-sm text-destructive">錯誤訊息: {error}</p>
                <Button onClick={() => {
                    window.location.href = "/input";
                }}>重試</Button>
            </div>
        )
    }

    if (status === "loading") {
        return (
            <div className="flex min-h-screen items-center justify-center bg-background">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
            </div>
        );
    }

    if (!session) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-background">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
            </div>
        );
    }

    // --- FULL COMPONENT RENDER ---
    return (
        <div className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5 flex flex-col items-center justify-center p-4">
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
                        >
                            <div className="space-y-2 text-center">
                                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <Utensils className="text-primary w-6 h-6" />
                                </div>
                                <h2 className="text-2xl font-bold">不知道怎麼點？</h2>
                                <p className="text-muted-foreground">輸入餐廳名稱，AI 根據 Google Map 及實際評價幫你推薦菜色。</p>
                            </div>

                            <div className="space-y-4">
                                <RestaurantSearch 
                                    onSelect={({ name }) => {
                                        updateData("restaurant_name", name);
                                        // Automatically move to next step after selection for a smoother experience
                                        setTimeout(() => {
                                            if (name) {
                                                setStep(2);
                                            }
                                        }, 100);
                                    }} 
                                    defaultValue={formData.restaurant_name}
                                />
                                <Button
                                    className="w-full py-6 text-lg bg-primary hover:bg-primary/90"
                                    onClick={handleNext}
                                    disabled={!formData.restaurant_name}
                                >
                                    下一步 <ArrowRight className="ml-2 w-5 h-5" />
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
                        >
                            <div className="space-y-2 text-center">
                                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <Sparkles className="text-primary w-6 h-6" />
                                </div>
                                <h2 className="text-2xl font-bold">客製化你的餐點</h2>
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

                                {/* People Count */}
                                <div className="space-y-3">
                                    <Label className="text-base">幾位用餐？</Label>
                                    <div className="flex items-center justify-between bg-secondary/30 p-4 rounded-xl">
                                        <span className="text-sm text-muted-foreground">人數</span>
                                        <div className="flex items-center space-x-4">
                                            <Button
                                                variant="outline"
                                                size="icon"
                                                className="h-8 w-8 rounded-full"
                                                onClick={() => updateData("people", Math.max(1, formData.people - 1))}
                                            >
                                                -
                                            </Button>
                                            <span className="text-xl font-bold w-6 text-center">{formData.people}</span>
                                            <Button
                                                variant="outline"
                                                size="icon"
                                                className="h-8 w-8 rounded-full"
                                                onClick={() => updateData("people", formData.people + 1)}
                                            >
                                                +
                                            </Button>
                                        </div>
                                    </div>
                                </div>

                                {/* Budget */}
                                <div className="space-y-3">
                                    <div className="flex justify-between items-center">
                                        <Label htmlFor="budget" className="text-base">
                                            {budgetType === "person" ? "每人預算 (客單價)" : "總預算"}
                                        </Label>
                                        <div className="flex bg-secondary/50 rounded-lg p-1">
                                            <button
                                                className={`px-3 py-1 text-xs rounded-md transition-all ${budgetType === "person" ? "bg-white shadow-sm text-foreground font-medium" : "text-muted-foreground"}`}
                                                onClick={() => setBudgetType("person")}
                                            >
                                                每人(客單)
                                            </button>
                                            <button
                                                className={`px-3 py-1 text-xs rounded-md transition-all ${budgetType === "total" ? "bg-white shadow-sm text-foreground font-medium" : "text-muted-foreground"}`}
                                                onClick={() => setBudgetType("total")}
                                            >
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
                                        <div className="flex justify-between text-xs text-muted-foreground px-1">
                                            <span>NT$ 0</span>
                                            <div className="font-mono text-sm font-semibold text-primary rounded-full bg-primary/10 px-3 py-1">
                                                NT$ {Number(formData.budget).toLocaleString() || "0"}
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
                                    <Label className="text-base">飲食偏好</Label>
                                    <TagInput
                                        value={formData.dietary_restrictions.split(',').map(s => s.trim()).filter(Boolean)}
                                        onChange={(tags) => updateData("dietary_restrictions", tags.join(", "))}
                                        suggestions={[
                                            { id: "no_beef", label: "不吃牛", icon: "🥩" },
                                            { id: "no_pork", label: "不吃豬", icon: "🐷" },
                                            { id: "vegetarian", label: "素食", icon: "🥬" },
                                            { id: "seafood_allergy", label: "海鮮過敏", icon: "🦐" },
                                            { id: "spicy", label: "愛吃辣", icon: "🌶️" },
                                            { id: "no_spicy", label: "不吃辣", icon: "🚫" },
                                            { id: "alcohol", label: "想喝酒", icon: "🍺" },
                                            { id: "kid_friendly", label: "有小孩", icon: "👶" },
                                            { id: "elderly", label: "長輩友善", icon: "👴" },
                                        ]}
                                        placeholder="例如：不吃花生、奶蛋素..."
                                    />
                                    <Textarea
                                        placeholder="若你要用自然語言描述讓 AI 更了解你的需求也可以唷..."
                                        value={formData.dietary_restrictions}
                                        onChange={(e) => updateData("dietary_restrictions", e.target.value)}
                                        className="h-24 bg-secondary/30 border-transparent focus:border-primary resize-none"
                                    />
                                </div>

                                <Button
                                    className="w-full py-6 text-lg bg-primary hover:bg-primary/90 shadow-lg shadow-primary/20 rounded-xl"
                                    onClick={handleNext}
                                    disabled={!formData.budget}
                                >
                                    開始生成推薦 <Check className="ml-2 w-5 h-5" />
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