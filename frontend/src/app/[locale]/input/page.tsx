"use client";
import { useTranslations } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect, Suspense, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { MultiAgentLoader } from "@/components/multi-agent-loader";
import { useSession } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Textarea } from "@/components/ui/textarea";
import { ArrowRight, Check, Utensils, Sparkles, Users, AlertCircle, ArrowLeft, Briefcase, Heart, Dumbbell, Home, Zap, Compass, Crown } from "lucide-react";
// import Image from "next/image";
import { RestaurantSearch } from "@/components/restaurant-search";
import { TagInput } from "@/components/tag-input"; // New import

function InputPageContents() {
    const t = useTranslations('InputPage');
    // --- HOOKS ---
    const { data: session, status } = useSession();
    const router = useRouter();
    const searchParams = useSearchParams();
    const error = searchParams.get('error');

    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState<{
        restaurant_name: string;
        place_id?: string;
        people: number;
        dietary_restrictions: string;
        mode: "sharing" | "individual";
        occasion: "business" | "date" | "family" | "friends" | "fitness" | "all_signatures";
    }>({
        restaurant_name: "",
        place_id: undefined,
        people: 2,
        dietary_restrictions: "",
        mode: "sharing",
        occasion: "friends"
    });

    // --- FUNCTIONS ---
    const updateData = useCallback((key: string, value: string | number | null) => {
        setFormData(prev => ({ ...prev, [key]: value }));
    }, []);

    const handleNext = useCallback(() => {
        if (step === 1 && formData.restaurant_name) {
            setStep(2);
        } else if (step === 2) {
            const params = new URLSearchParams({
                restaurant: formData.restaurant_name,
                people: formData.people.toString(),
                dietary: formData.dietary_restrictions,
                mode: formData.mode,
                occasion: formData.occasion,
                ...(formData.place_id && { place_id: formData.place_id })
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
        const dietary = searchParams.get("dietary");
        const mode = searchParams.get("mode");

        if (restaurant || people) {
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
                    dietary_restrictions: dietary || "",
                    mode: parsedMode,
                    occasion: "friends"
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
    if (error && error !== 'mock_bypass') {
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
            <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-background">
                <MultiAgentLoader />
            </div>
        );
    }

    if (!session && error !== 'mock_bypass') {
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
                            aria-label={t('title')}
                        >
                            <div className="space-y-2 text-center">

                                <h2 className="text-2xl font-bold">{t('title')}</h2>
                                <p className="text-muted-foreground">{t('subtitle')}</p>
                            </div>

                            <div className="space-y-4">
                                <div role="group" aria-labelledby="restaurant-input-label">
                                    <label id="restaurant-input-label" className="sr-only">{t('restaurant_placeholder')}</label>
                                    <RestaurantSearch
                                        name="restaurant_name"
                                        onSelect={({ name, place_id }) => {
                                            // ... (keep existing logic)
                                            updateData("restaurant_name", name);
                                            if (place_id) {
                                                setFormData(prev => ({ ...prev, place_id }));
                                            }
                                            if (name) {
                                                // Trigger prefetch immediately
                                                // @ts-expect-error - session type definition might be incomplete
                                                const token = session?.id_token;
                                                if (token) {
                                                    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/v2/prefetch_restaurant`, {
                                                        method: 'POST',
                                                        headers: {
                                                            'Content-Type': 'application/json',
                                                            'Authorization': `Bearer ${token}`
                                                        },
                                                        body: JSON.stringify({
                                                            restaurant_name: name,
                                                            place_id: place_id
                                                        })
                                                    }).catch(err => console.error("Prefetch failed:", err));
                                                }

                                                setStep(2);
                                            }
                                        }}
                                        onChange={(value) => {
                                            updateData("restaurant_name", value);
                                        }}
                                        defaultValue={formData.restaurant_name}
                                        placeholder={t('restaurant_placeholder')}
                                    />
                                    <div className="flex justify-between items-start mt-2">
                                        <p className="text-xs text-muted-foreground" id="restaurant-search-hint">
                                            💡 請等待 Google Maps 自動帶出餐廳建議後點選，以獲得最精準的菜單資訊
                                        </p>
                                    </div>
                                </div>
                                <Button
                                    className="w-full py-6 text-lg bg-primary hover:bg-primary/90"
                                    onClick={handleNext}
                                    disabled={!formData.restaurant_name}
                                    aria-label={t('next_button')}
                                >
                                    {t('next_button')} <ArrowRight className="ml-2 w-5 h-5" aria-hidden="true" />
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
                            aria-label={t('step2_title')}
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
                                <h2 className="text-2xl font-bold">{t('step2_title')}</h2>
                                <p className="text-muted-foreground">{t('step2_subtitle')}</p>
                            </div>

                            <div className="space-y-8">
                                {/* Dining Style (Moved to Top) */}
                                <div className="space-y-3">
                                    <Label className="text-base">{t('mode_label')}</Label>
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
                                                <span className="font-medium">{t('mode_sharing')}</span>
                                            </Label>
                                        </div>
                                        <div>
                                            <RadioGroupItem value="individual" id="individual" className="peer sr-only" />
                                            <Label
                                                htmlFor="individual"
                                                className="flex flex-col items-center justify-center gap-2 rounded-xl border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary peer-data-[state=checked]:bg-primary/5 cursor-pointer transition-all"
                                            >
                                                <Utensils className="h-5 w-5" />
                                                <span className="font-medium">{t('mode_individual')}</span>
                                            </Label>
                                        </div>
                                    </RadioGroup>
                                </div>

                                {/* Occasion (Contextual) */}
                                <div className="space-y-3">
                                    <Label className="text-base">{t('occasion_label')}</Label>
                                    <RadioGroup
                                        defaultValue={formData.occasion}
                                        onValueChange={(val) => updateData("occasion", val)}
                                        className="grid grid-cols-2 sm:grid-cols-4 gap-2"
                                    >
                                        {(formData.mode === "individual" ? [
                                            { id: "quick", label: t('occasion_quick'), icon: Zap },
                                            { id: "treat", label: t('occasion_treat'), icon: Sparkles },
                                            { id: "fitness", label: t('occasion_fitness'), icon: Dumbbell },
                                            { id: "adventure", label: t('occasion_adventure'), icon: Compass },
                                        ] : [
                                            { id: "friends", label: t('occasion_friends'), icon: Users },
                                            { id: "family", label: t('occasion_family'), icon: Home },
                                            { id: "date", label: t('occasion_date'), icon: Heart },
                                            { id: "business", label: t('occasion_business'), icon: Briefcase },
                                            { id: "all_signatures", label: t('occasion_all_signatures'), icon: Crown },
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
                                    <Label htmlFor="people-count" className="text-base">{t('people_label')}</Label>
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

                                {/* Dietary */}
                                <div className="space-y-3">
                                    <Label className="text-base">{t('dietary_label')}</Label>
                                    <TagInput
                                        value={formData.dietary_restrictions.split(',').map(s => s.trim()).filter(Boolean)}
                                        onChange={(tags) => updateData("dietary_restrictions", tags.join(", "))}
                                        suggestions={[
                                            { id: "some_no_beef", label: "有人不吃牛", icon: "🥩" },
                                            { id: "some_no_pork", label: "有人不吃豬", icon: "🐷" },
                                            { id: "some_no_seafood", label: "有人不吃海鮮", icon: "🦐" },
                                            { id: "some_vegetarian", label: "有素食需求", icon: "🥬" },
                                            { id: "some_no_spicy", label: "不太能吃辣", icon: "🌶️" },
                                            { id: "some_no_cilantro", label: "不要香菜", icon: "🌿" },
                                        ]}
                                        placeholder={t('dietary_placeholder')}
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
                                    aria-label={t('generate_button')}
                                >
                                    {t('generate_button')} <Check className="ml-2 w-5 h-5" aria-hidden="true" />
                                </Button>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
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