"use client";
import { useTranslations } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect, Suspense, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { ArrowRight, Users, Utensils, Heart, Briefcase, Home, MapPin, AlertCircle } from "lucide-react";
import { RestaurantSearch } from "@/components/restaurant-search";
import { TagInput } from "@/components/tag-input";
import { InstallButton } from "@/components/install-button";
import { MultiAgentLoader } from "@/components/multi-agent-loader";
import { cn } from "@/lib/utils";

function InputPageContents() {
    const t = useTranslations('InputPage');
    const { data: session, status } = useSession();
    const router = useRouter();
    const searchParams = useSearchParams();
    const error = searchParams.get('error');

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

    const isRestaurantSelected = !!formData.restaurant_name;

    const updateData = useCallback((key: string, value: string | number | null) => {
        setFormData(prev => ({ ...prev, [key]: value }));
    }, []);

    const handleGo = useCallback(() => {
        const params = new URLSearchParams({
            restaurant: formData.restaurant_name,
            people: formData.people.toString(),
            dietary: formData.dietary_restrictions,
            mode: formData.mode,
            occasion: formData.occasion,
            ...(formData.place_id && { place_id: formData.place_id })
        });
        router.push(`/recommendation?${params.toString()}`);
    }, [formData, router]);

    // Auth Check
    useEffect(() => {
        if (status === "unauthenticated" && !error) {
            router.push("/");
        }
    }, [status, error, router]);

    // URL Prefill Logic
    useEffect(() => {
        const restaurant = searchParams.get("restaurant");
        const people = searchParams.get("people");

        if (restaurant) {
            updateData("restaurant_name", restaurant);
        }
        if (people) {
            updateData("people", parseInt(people));
        }
    }, [searchParams, updateData]);

    if (error && error !== 'mock_bypass') {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center space-y-4 bg-background">
                <AlertCircle className="w-16 h-16 text-destructive" />
                <h2 className="text-2xl font-bold">登入失敗</h2>
                <Button onClick={() => window.location.href = "/input"}>重試</Button>
            </div>
        );
    }

    if (status === "loading") {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-cream-50">
                <MultiAgentLoader />
            </div>
        );
    }

    if (!session && error !== 'mock_bypass') return null;

    return (
        <div className="min-h-screen bg-cream-50 flex flex-col items-center p-4 sm:p-6 font-sans relative overflow-y-auto">

            <div className="w-full max-w-lg space-y-8 relative z-10 py-10">
                <div className="flex justify-end mb-4 absolute top-0 right-0">
                    <InstallButton />
                </div>

                {/* Header: Concierge Metaphor */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-2"
                >
                    <p className="text-caramel-700 font-medium tracking-widest uppercase text-xs sm:text-sm">
                        {t('concierge_subtitle')}
                    </p>
                    <h1 className="text-4xl sm:text-5xl font-display font-bold text-charcoal leading-tight">
                        {t('concierge_title')}
                    </h1>
                </motion.div>

                {/* Hero Input: Restaurant Search */}
                <motion.div
                    className="transition-all duration-500 ease-out"
                    animate={{ scale: isRestaurantSelected ? 1 : 1.02 }}
                >
                    <div className="relative group">
                        <div className={cn(
                            "absolute -inset-1 bg-gradient-to-r from-caramel to-terracotta rounded-2xl blur opacity-20 transition duration-1000",
                            !isRestaurantSelected && "opacity-40 group-hover:opacity-60 group-hover:duration-200"
                        )}></div>
                        <div className="relative bg-white rounded-xl shadow-card p-1">
                            <RestaurantSearch
                                name="restaurant_name"
                                onSelect={({ name, place_id }) => {
                                    updateData("restaurant_name", name);
                                    if (place_id) {
                                        updateData("place_id", place_id);
                                        // Prefetch logic
                                        // @ts-expect-error - session token type
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
                                defaultValue={formData.restaurant_name}
                                placeholder={t('restaurant_placeholder')}
                                className="text-xl sm:text-2xl font-bold border-none shadow-none focus-visible:ring-0 px-4 h-16 sm:h-20 bg-transparent placeholder:text-muted-foreground/50"
                            />
                        </div>
                    </div>
                    {/* Reselect Button */}
                    {isRestaurantSelected && (
                        <motion.button
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            onClick={() => {
                                updateData("restaurant_name", "");
                                updateData("place_id", undefined);
                            }}
                            className="text-xs text-muted-foreground mt-3 hover:text-primary flex items-center gap-1 ml-1"
                        >
                            <MapPin className="w-3 h-3" /> {t('reselect_restaurant')}
                        </motion.button>
                    )}
                </motion.div>

                {/* The Unfolding Form (Mad Libs) */}
                <AnimatePresence>
                    {isRestaurantSelected && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            exit={{ opacity: 0, height: 0 }}
                            transition={{ type: "spring", stiffness: 300, damping: 30 }}
                            className="overflow-hidden"
                        >
                            <div className="pt-8 space-y-10 pb-20">

                                {/* 1. People & Mode */}
                                <div className="space-y-4">
                                    <h2 className="text-2xl font-display font-semibold text-charcoal flex items-center gap-2">
                                        {t('section_we_have')}
                                    </h2>
                                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-charcoal/5 space-y-6">
                                        {/* People Counter */}
                                        <div className="flex items-center justify-between">
                                            <span className="text-lg font-medium text-charcoal-700">{t('people_label')}</span>
                                            <div className="flex items-center gap-4 bg-cream-100 rounded-full p-1.5">
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-10 w-10 rounded-full hover:bg-white hover:shadow-sm text-lg"
                                                    onClick={() => updateData("people", Math.max(1, formData.people - 1))}
                                                    disabled={formData.people <= 1}
                                                    aria-label="減少人數"
                                                > - </Button>
                                                <span className="w-8 text-center font-bold text-xl tabular-nums">{formData.people}</span>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-10 w-10 rounded-full hover:bg-white hover:shadow-sm text-lg"
                                                    onClick={() => updateData("people", formData.people + 1)}
                                                    aria-label="增加人數"
                                                > + </Button>
                                            </div>
                                        </div>

                                        <div className="h-px bg-border/50" />

                                        {/* Sharing Mode */}
                                        <div className="space-y-3">
                                            <Label className="text-base text-charcoal-700">{t('mode_label')}</Label>
                                            <div className="grid grid-cols-2 gap-3">
                                                <button
                                                    onClick={() => updateData("mode", "sharing")}
                                                    className={cn(
                                                        "p-4 rounded-xl border-2 text-center transition-all flex flex-col items-center gap-2",
                                                        formData.mode === "sharing"
                                                            ? "border-caramel bg-caramel/5 text-caramel-900 shadow-sm"
                                                            : "border-transparent bg-secondary/10 hover:bg-secondary/20 text-muted-foreground"
                                                    )}
                                                    aria-label="大家一起分食"
                                                >
                                                    <Users className="w-6 h-6" />
                                                    <span className="font-bold text-sm">{t('mode_sharing')}</span>
                                                </button>
                                                <button
                                                    onClick={() => updateData("mode", "individual")}
                                                    className={cn(
                                                        "p-4 rounded-xl border-2 text-center transition-all flex flex-col items-center gap-2",
                                                        formData.mode === "individual"
                                                            ? "border-caramel bg-caramel/5 text-caramel-900 shadow-sm"
                                                            : "border-transparent bg-secondary/10 hover:bg-secondary/20 text-muted-foreground"
                                                    )}
                                                    aria-label="個人套餐"
                                                >
                                                    <Utensils className="w-6 h-6" />
                                                    <span className="font-bold text-sm">{t('mode_individual')}</span>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* 2. Occasion */}
                                <div className="space-y-4">
                                    <h2 className="text-2xl font-display font-semibold text-charcoal">
                                        {t('section_occasion')}
                                    </h2>
                                    <div className="grid grid-cols-4 gap-3 sm:gap-4">
                                        {[
                                            { id: "friends", label: t('occasion_friends'), icon: Users },
                                            { id: "family", label: t('occasion_family'), icon: Home },
                                            { id: "date", label: t('occasion_date'), icon: Heart },
                                            { id: "business", label: t('occasion_business'), icon: Briefcase },
                                        ].map((item) => (
                                            <button
                                                key={item.id}
                                                onClick={() => updateData("occasion", item.id)}
                                                className={cn(
                                                    "flex flex-col items-center justify-center p-3 sm:p-4 rounded-2xl border transition-all gap-2 aspect-square",
                                                    formData.occasion === item.id
                                                        ? "bg-caramel text-white border-caramel shadow-md transform scale-105"
                                                        : "bg-white border-transparent shadow-sm hover:border-caramel/30 text-muted-foreground"
                                                )}
                                                aria-label={item.label}
                                            >
                                                <item.icon className="w-6 h-6" />
                                                <span className="text-xs sm:text-sm font-bold">{item.label}</span>
                                            </button>
                                        ))}
                                    </div>
                                </div>

                                {/* 3. Dietary */}
                                <div className="space-y-4">
                                    <h2 className="text-2xl font-display font-semibold text-charcoal">
                                        {t('section_dietary')}
                                    </h2>
                                    <div className="bg-white p-4 rounded-xl shadow-sm border border-charcoal/5">
                                        <TagInput
                                            value={formData.dietary_restrictions.split(',').map(s => s.trim()).filter(Boolean)}
                                            onChange={(tags) => updateData("dietary_restrictions", tags.join(", "))}
                                            suggestions={[
                                                { id: "no_beef", label: "不吃牛", icon: "🥩" },
                                                { id: "no_pork", label: "不吃豬", icon: "🐷" },
                                                { id: "no_seafood", label: "海鮮過敏", icon: "🦐" },
                                                { id: "no_spicy", label: "不吃辣", icon: "🌶️" },
                                                { id: "kid_friendly", label: "有小孩", icon: "👶" },
                                            ]}
                                            placeholder={t('dietary_placeholder')}
                                            className="bg-transparent"
                                        />
                                    </div>
                                </div>

                                {/* 4. CTA Button */}
                                <div className="pt-4">
                                    <Button
                                        className="w-full py-8 text-xl font-bold bg-gradient-to-r from-caramel to-terracotta hover:from-caramel-700 hover:to-terracotta-700 text-white shadow-lg shadow-caramel/30 rounded-2xl transform transition-all hover:scale-[1.02] active:scale-[0.98]"
                                        onClick={handleGo}
                                    >
                                        <span className="flex items-center gap-3">
                                            {t('generate_button')}
                                            <ArrowRight className="w-6 h-6" />
                                        </span>
                                    </Button>
                                    <p className="text-center text-xs text-muted-foreground mt-4 opacity-70">
                                        {t('ai_disclaimer')}
                                    </p>
                                </div>
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
            <div className="flex min-h-screen items-center justify-center bg-cream-50">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-caramel"></div>
            </div>
        }>
            <InputPageContents />
        </Suspense>
    );
}
