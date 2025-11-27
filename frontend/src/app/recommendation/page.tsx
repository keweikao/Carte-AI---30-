"use client";

import { useState, useEffect, Suspense, useRef } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Loader2, Check, Utensils, AlertCircle, ArrowLeft, CheckCircle2, RotateCw, AlertTriangle, Info } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";
import { getRecommendations, getAlternatives, UserInputV2 } from "@/lib/api";
import { DishCardSkeleton } from "@/components/dish-card-skeleton";
import type { MenuItem } from "@/types";
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog";

// V3 Type Definitions
interface DishSlot {
    category: string;
    display: MenuItem;
    alternatives: MenuItem[];
}

interface RecommendationData {
    recommendation_summary: string;
    items: DishSlot[];
    total_price: number;
    nutritional_balance_note: string | null;
    recommendation_id: string;
    restaurant_name: string;
    cuisine_type: string;
    category_summary: Record<string, number>;
}

// Define interfaces for component props for type safety
interface LoadingStateProps {
    reviewCount: number;
    restaurantName: string;
    analysisSteps: { text: string; icon: string; }[];
    analysisStep: number;
}

// Re-usable loading animation component
function LoadingState({ reviewCount, restaurantName, analysisSteps, analysisStep }: LoadingStateProps) {
    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 text-center space-y-8" role="status" aria-live="polite" aria-label="正在分析餐廳評論">
            <div className="relative w-32 h-32 flex items-center justify-center" aria-hidden="true">
                <motion.div
                    className="absolute inset-0 border-4 border-muted rounded-full"
                />
                <div
                    className="absolute inset-0 border-4 border-accent rounded-full border-t-transparent animate-spin"
                />
                <Utensils className="w-12 h-12 text-accent" />
            </div>
            <div className="space-y-2 max-w-sm mx-auto">
                <h2 className="text-2xl font-bold text-foreground">
                    正在爬梳 <motion.span
                        key={reviewCount}
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-accent"
                        aria-live="polite"
                    >
                        {reviewCount}
                    </motion.span> 則 Google 評論...
                </h2>
                <p className="text-muted-foreground text-sm">
                    AI 正在分析 <span className="font-semibold text-foreground">{restaurantName}</span> 的老饕推薦關鍵字
                </p>
            </div>
            <div className="w-full max-w-md bg-secondary/50 rounded-xl p-4 space-y-3" role="progressbar" aria-label="分析進度">
                {analysisSteps.map((step, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: analysisStep > index ? 1 : 0.3, x: analysisStep > index ? 0 : -10 }}
                        className="flex items-center gap-3"
                    >
                        <div className="w-6 h-6 flex items-center justify-center" aria-hidden="true">
                            {analysisStep > index && <Check className="w-5 h-5 text-success" />}
                            {analysisStep <= index && <Loader2 className="w-5 h-5 text-muted-foreground animate-spin" />}
                        </div>
                        <span className={`text-sm font-medium ${analysisStep > index ? "text-foreground" : "text-muted-foreground"}`}>
                            {step.text}
                        </span>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}

interface ErrorStateProps {
    error: string | null;
}

// Re-usable error component
function ErrorState({ error }: ErrorStateProps) {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center space-y-4 bg-background" role="alert" aria-live="assertive">
            <AlertCircle className="w-16 h-16 text-destructive" aria-hidden="true" />
            <h2 className="text-2xl font-bold text-foreground">出錯了！</h2>
            <p className="text-muted-foreground">{error}</p>
            <Link href="/input">
                <Button className="bg-primary text-primary-foreground hover:bg-primary/90" aria-label="返回輸入頁重新設定">返回重新設定</Button>
            </Link>
        </div>
    );
}

// Helper for generating analysis steps
const generateAnalysisSteps = (restaurantName: string) => {
    return [
        { text: `分析 ${restaurantName} 的菜單結構與評論`, icon: "spinner" },
        { text: "根據您的偏好篩選候選菜品", icon: "spinner" },
        { text: "設計菜色搭配以確保多樣性", icon: "spinner" },
        { text: "在預算內優化CP值最高的組合", icon: "spinner" }
    ];
};

// Skeleton state for when recommendations are being prepared
function RecommendationSkeleton() {
    return (
        <div className="relative min-h-screen bg-background pb-32 font-sans">
            <div className="absolute inset-0 w-full h-full overflow-y-auto">
                {/* Header */}
                <div className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur">
                    <div className="container flex h-14 items-center justify-between px-4">
                        <Button variant="ghost" disabled className="gap-2">
                            <ArrowLeft className="w-4 h-4" />返回設定
                        </Button>
                        <Button disabled className="gap-2 bg-primary hover:bg-primary/90">
                            <Check className="w-4 h-4" />產出點餐菜單
                        </Button>
                    </div>
                </div>

                {/* Sticky Price Summary - Skeleton */}
                <div className="bg-background/95 backdrop-blur-sm sticky top-14 z-10 px-6 py-4 shadow-sm border-b">
                    <div className="flex justify-between items-end mb-2">
                        <div>
                            <p className="text-xs text-muted-foreground mb-1 uppercase tracking-wider">菜單總價</p>
                            <div className="h-9 w-32 bg-cream-200 rounded animate-skeleton" />
                        </div>
                        <div className="text-right">
                            <p className="text-xs text-muted-foreground mb-1">人均約</p>
                            <div className="h-7 w-24 bg-cream-200 rounded animate-skeleton" />
                        </div>
                    </div>
                </div>

                {/* Skeleton Cards */}
                <div className="p-4 space-y-4">
                    {Array.from({ length: 5 }).map((_, index) => (
                        <DishCardSkeleton key={index} />
                    ))}
                </div>
            </div>
        </div>
    );
}

function RecommendationPageContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const { data: session } = useSession();

    // Core states
    const [initialLoading, setInitialLoading] = useState(true); // Only true for the very first load
    const [error, setError] = useState<string | null>(null);
    const [data, setData] = useState<RecommendationData | null>(null);

    // V3 states
    const [dishSlots, setDishSlots] = useState<DishSlot[]>([]);
    const [totalPrice, setTotalPrice] = useState<number>(0);
    const [slotStatus, setSlotStatus] = useState<Map<string, 'pending' | 'selected'>>(new Map());

    // Animation states
    const [analysisStep, setAnalysisStep] = useState(0);
    const [reviewCount, setReviewCount] = useState(0);
    const analysisSteps = generateAnalysisSteps(searchParams.get("restaurant") || "此餐廳");
    const [swappingSlots, setSwappingSlots] = useState<Set<number>>(new Set());

    // Dialog states for FE-039 and FE-040
    const [showEmptyPoolDialog, setShowEmptyPoolDialog] = useState(false);
    const [emptyPoolCategory, setEmptyPoolCategory] = useState<string>("");
    const [emptyPoolSlotIndex, setEmptyPoolSlotIndex] = useState<number>(-1);
    const [showBudgetWarning, setShowBudgetWarning] = useState(false);
    const [budgetExceedPercentage, setBudgetExceedPercentage] = useState<number>(0);

    // Track swapped dishes for "view previously swapped" feature
    const [swappedDishes, setSwappedDishes] = useState<Map<string, MenuItem[]>>(new Map());

    // Fetch V3 Data
    useEffect(() => {
        if (!session) return;

        const fetchData = async () => {
            let interval: NodeJS.Timeout | null = null;
            try {
                if (!data) { // Initial load
                    setInitialLoading(true);
                }
                setError(null);

                const targetReviews = Math.floor(Math.random() * 800) + 300;
                interval = setInterval(() => {
                    setAnalysisStep(prev => Math.min(prev + 1, analysisSteps.length));
                    setReviewCount(prev => Math.min(prev + Math.floor(Math.random() * 80) + 40, targetReviews));
                }, 800);
                // --- Build V2 Request from URL Search Params ---
                const restaurant_name = searchParams.get("restaurant") || "";
                const place_id = searchParams.get("place_id") || undefined;
                const party_size = parseInt(searchParams.get("people") || "2");

                const rawMode = searchParams.get("mode");
                const dining_style = (rawMode === "Shared" || rawMode === "sharing") ? "Shared" : "Individual";

                const dish_count_str = searchParams.get("dish_count");

                // Parse budget - now it's a number from the slider
                const budgetStr = searchParams.get("budget") || "";
                const budgetAmount = parseInt(budgetStr) || (dining_style === "Shared" ? 2000 : 500);

                const requestData: UserInputV2 = {
                    restaurant_name,
                    place_id,
                    party_size,
                    dining_style,
                    budget: {
                        type: dining_style === "Shared" ? "Total" : "Per_Person",
                        amount: budgetAmount,
                    },
                    dish_count_target: dish_count_str ? parseInt(dish_count_str) : null,
                    preferences: searchParams.get("dietary")?.split(",").filter(p => p) || [],
                };

                if (!requestData.restaurant_name) {
                    throw new Error("餐廳名稱為必填項。");
                }

                // @ts-expect-error - id_token exists on session but not in type definition
                const token = session?.id_token;
                const result: RecommendationData = await getRecommendations(requestData, token);

                // --- Set V3 State ---
                setData(result);
                setDishSlots(result.items);
                setTotalPrice(result.total_price);

                const initialStatus = new Map<string, 'pending' | 'selected'>();
                result.items.forEach(slot => initialStatus.set(slot.display.dish_name, 'pending'));
                setSlotStatus(initialStatus);

                setTimeout(() => {
                    if (interval) clearInterval(interval);
                    setInitialLoading(false);
                }, 3000);

            } catch (err) {
                const error = err as Error;
                console.error(error);
                if (interval) clearInterval(interval);
                setError(error.message || "無法取得推薦，請稍後再試");
                setInitialLoading(false); // Ensure loading state is reset even on error
            }
        };

        fetchData();
    }, [searchParams, session]); // eslint-disable-line react-hooks/exhaustive-deps

    const perPerson = Math.round(totalPrice / (parseInt(searchParams.get("people") || "2")));
    // Get budget type from URL params, fallback to "person" as default (matching input page default)
    const budgetType = searchParams.get("budget_type") || "person";

    // Determine the value to compare against the budget
    const comparisonPrice = budgetType === "person" ? perPerson : totalPrice;
    const budgetAmount = parseInt(searchParams.get("budget") || "0"); // Get raw budget amount

    // FE-040: Check budget and show warning if exceeded by 20%
    useEffect(() => {
        if (!data || comparisonPrice === 0 || budgetAmount === 0) return;

        if (comparisonPrice > budgetAmount) {
            const exceedPercentage = ((comparisonPrice - budgetAmount) / budgetAmount) * 100;
            if (exceedPercentage >= 20) {
                setBudgetExceedPercentage(Math.round(exceedPercentage));
                setShowBudgetWarning(true);
            }
        }
    }, [comparisonPrice, budgetAmount, data, searchParams]);

    // Trigger confetti when all dishes are confirmed
    const prevAllDecidedRef = useRef(false);

    useEffect(() => {
        const allDecided = Array.from(slotStatus.values()).every(status => status === 'selected');

        if (allDecided && !prevAllDecidedRef.current && dishSlots.length > 0) {
            // Dynamic import confetti only when needed
            import('canvas-confetti').then((confettiModule) => {
                const confetti = confettiModule.default;

                // Trigger confetti celebration
                const duration = 3000;
                const animationEnd = Date.now() + duration;
                const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

                function randomInRange(min: number, max: number) {
                    return Math.random() * (max - min) + min;
                }

                const interval: NodeJS.Timeout = setInterval(function () {
                    const timeLeft = animationEnd - Date.now();

                    if (timeLeft <= 0) {
                        return clearInterval(interval);
                    }

                    const particleCount = 50 * (timeLeft / duration);

                    confetti({
                        ...defaults,
                        particleCount,
                        origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
                        colors: ['#D4A574', '#C17767', '#8FA885'] // caramel, terracotta, sage
                    });
                    confetti({
                        ...defaults,
                        particleCount,
                        origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
                        colors: ['#D4A574', '#C17767', '#8FA885']
                    });
                }, 250);
            });
        }

        prevAllDecidedRef.current = allDecided;
    }, [slotStatus, dishSlots.length]);

    const handleSelect = (dishName: string, slotIndex: number) => {
        setSlotStatus(prev => {
            const newStatus = new Map(prev);
            const currentStatus = newStatus.get(dishName);

            if (currentStatus === 'selected') {
                // Unselect
                newStatus.set(dishName, 'pending');
            } else {
                // Select and scroll to next pending dish
                newStatus.set(dishName, 'selected');

                // Find next pending dish
                setTimeout(() => {
                    const nextPendingIndex = dishSlots.findIndex((slot, idx) =>
                        idx > slotIndex && newStatus.get(slot.display.dish_name) === 'pending'
                    );

                    if (nextPendingIndex !== -1) {
                        // Scroll to next pending dish
                        const element = document.querySelector(`[data-slot-index="${nextPendingIndex}"]`);
                        if (element) {
                            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        }
                    }
                }, 300);
            }

            return newStatus;
        });
    };

    const handleSwap = async (slotIndex: number) => {
        setSwappingSlots(prev => new Set(prev).add(slotIndex));

        const newSlots = [...dishSlots];
        const currentSlot = newSlots[slotIndex];
        const oldDish = currentSlot.display;

        let newDish: MenuItem | null = null;

        if (currentSlot.alternatives.length > 0) {
            newDish = currentSlot.alternatives.shift() as MenuItem;
        } else if (data) {
            try {
                // @ts-expect-error - id_token exists on session but not in type definition
                const token = session?.id_token;
                const seenDishes = [currentSlot.display, ...currentSlot.alternatives].map(d => d.dish_name);
                const moreAlternatives = await getAlternatives({
                    recommendation_id: data.recommendation_id,
                    category: currentSlot.category,
                    exclude: seenDishes
                }, token);

                if (moreAlternatives.length > 0) {
                    newDish = moreAlternatives.shift() as MenuItem;
                    currentSlot.alternatives.push(...moreAlternatives);
                } else {
                    // FE-039: No more alternatives available
                    setEmptyPoolCategory(currentSlot.category);
                    setEmptyPoolSlotIndex(slotIndex);
                    setShowEmptyPoolDialog(true);
                    setSwappingSlots(prev => {
                        const newSet = new Set(prev);
                        newSet.delete(slotIndex);
                        return newSet;
                    });
                    return;
                }
            } catch (e) {
                console.error("Failed to fetch more alternatives:", e);
                setSwappingSlots(prev => {
                    const newSet = new Set(prev);
                    newSet.delete(slotIndex);
                    return newSet;
                });
                return;
            }
        }

        if (newDish) {
            // Track swapped dish
            setSwappedDishes(prev => {
                const newMap = new Map(prev);
                const category = currentSlot.category;
                const existing = newMap.get(category) || [];
                newMap.set(category, [...existing, oldDish]);
                return newMap;
            });

            currentSlot.display = newDish;
            setDishSlots(newSlots); // Update the slots state
            setTotalPrice(prev => prev - oldDish.price + (newDish as MenuItem).price);

            setSlotStatus(prev => {
                const newMap = new Map(prev);
                newMap.delete(oldDish.dish_name);
                newMap.set((newDish as MenuItem).dish_name, 'pending');
                return newMap;
            });
        }

        setTimeout(() => setSwappingSlots(prev => {
            const newSet = new Set(prev);
            newSet.delete(slotIndex);
            return newSet;
        }), 500); // Animation duration
    };

    // FE-039: Handle keeping current dish when pool is empty
    const handleKeepCurrentDish = () => {
        setShowEmptyPoolDialog(false);
        // Automatically select the current dish
        if (emptyPoolSlotIndex >= 0) {
            const currentDish = dishSlots[emptyPoolSlotIndex].display;
            handleSelect(currentDish.dish_name, emptyPoolSlotIndex);
        }
    };

    // FE-039: Handle viewing previously swapped dishes
    const handleViewSwappedDishes = () => {
        setShowEmptyPoolDialog(false);
        if (emptyPoolSlotIndex >= 0) {
            const category = dishSlots[emptyPoolSlotIndex].category;
            const swapped = swappedDishes.get(category) || [];

            if (swapped.length > 0) {
                // Put swapped dishes back into alternatives
                const newSlots = [...dishSlots];
                newSlots[emptyPoolSlotIndex].alternatives.push(...swapped);
                setDishSlots(newSlots);

                // Clear swapped dishes for this category
                setSwappedDishes(prev => {
                    const newMap = new Map(prev);
                    newMap.delete(category);
                    return newMap;
                });

                // Trigger swap again
                handleSwap(emptyPoolSlotIndex);
            }
        }
    };

    // FE-040: Handle budget warning actions
    const handleContinueOverBudget = () => {
        setShowBudgetWarning(false);
    };

    const handleAdjustBudget = () => {
        setShowBudgetWarning(false);
        router.push(`/input?${searchParams.toString()}`);
    };

    const handleBackToSettings = () => {
        router.push(`/input?${searchParams.toString()}`);
    };

    if (initialLoading) return <LoadingState reviewCount={reviewCount} restaurantName={searchParams.get("restaurant") || ""} analysisSteps={analysisSteps} analysisStep={analysisStep} />;
    if (error) return <ErrorState error={error} />;
    if (!data) return null;

    const allDecided = Array.from(slotStatus.values()).every(status => status === 'selected');


    return (
        <div className="relative min-h-screen bg-background pb-32 font-sans">
            <div className="absolute inset-0 w-full h-full overflow-y-auto">
                <div className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur" role="banner">
                    <div className="container flex h-14 items-center justify-between px-2 sm:px-4 gap-2">
                        <Button variant="ghost" onClick={handleBackToSettings} className="gap-1 sm:gap-2 text-sm sm:text-base px-2 sm:px-4" aria-label="返回設定頁"><ArrowLeft className="w-4 h-4" aria-hidden="true" />返回修改偏好</Button>

                    </div>
                </div>

                <div className="bg-background/95 backdrop-blur-sm sticky top-14 z-10 px-4 sm:px-6 py-4 shadow-sm border-b" role="region" aria-label="價格摘要">
                    <div className="flex justify-between items-end mb-2">
                        <div>
                            <p className="text-xs text-muted-foreground mb-1 uppercase tracking-wider">菜單總價</p>
                            <h1 className="text-2xl sm:text-3xl font-bold text-foreground font-mono transition-colors duration-300" aria-live="polite">NT$ {totalPrice.toLocaleString()}</h1>
                        </div>
                        <div className="text-right">
                            <p className="text-xs text-muted-foreground mb-1">人均約</p>
                            <p className="text-lg sm:text-xl font-bold text-orange-600 font-mono" aria-live="polite">NT$ {perPerson.toLocaleString()}</p>
                        </div>
                    </div>
                </div>

                <div className="p-4 pb-32 space-y-4" role="list" aria-label="推薦菜品列表">
                    {dishSlots.map((slot, index) => {
                        const status = slotStatus.get(slot.display.dish_name) || 'pending';
                        const isSwapping = swappingSlots.has(index);

                        return (
                            <motion.div
                                key={slot.display.dish_name}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                data-slot-index={index}
                                role="listitem"
                            >
                                <Card
                                    className={`p-4 transition-all duration-300 rounded-xl bg-white shadow-sm ${status === 'selected' ? 'opacity-50' : ''}`}
                                    role="article"
                                    aria-label={`菜品推薦：${slot.display.dish_name}，價格 ${slot.display.price} 元`}
                                >
                                    <div className="flex gap-4">
                                        <div className="flex-1 min-w-0">
                                            <div className="flex justify-between items-start mb-2">
                                                <div className="flex items-center gap-2">
                                                    <h3 className="font-bold text-lg text-foreground leading-tight">{slot.display.dish_name}</h3>
                                                    {slot.display.quantity > 1 && (
                                                        <span className="bg-primary/10 text-primary text-xs font-bold px-2 py-0.5 rounded-full">
                                                            x{slot.display.quantity}
                                                        </span>
                                                    )}
                                                </div>
                                                <span className="text-lg font-mono font-semibold text-foreground" aria-label={`價格 ${slot.display.price} 元`}>NT$ {slot.display.price}</span>
                                            </div>
                                            <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">&ldquo;{slot.display.reason}&rdquo;</p>

                                            <div className="flex items-center gap-2 mt-4" role="group" aria-label="菜品操作">
                                                <Button
                                                    size="sm"
                                                    className={`flex-1 h-9 rounded-full ${status === 'selected' ? 'bg-green-600 hover:bg-green-700' : 'bg-primary hover:bg-primary/90'} text-primary-foreground`}
                                                    onClick={() => handleSelect(slot.display.dish_name, index)}
                                                    aria-label={status === 'selected' ? `取消選擇 ${slot.display.dish_name}` : `確認要點 ${slot.display.dish_name}`}
                                                    aria-pressed={status === 'selected'}
                                                >
                                                    <CheckCircle2 className="w-4 h-4 mr-1.5" aria-hidden="true" />
                                                    {status === 'selected' ? '已選擇' : '我要點'}
                                                </Button>
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    className="h-9 rounded-full px-4"
                                                    onClick={() => handleSwap(index)}
                                                    disabled={isSwapping}
                                                    aria-label={`換一道菜替代 ${slot.display.dish_name}`}
                                                    aria-busy={isSwapping}
                                                >
                                                    <RotateCw className={`w-4 h-4 mr-1.5 ${isSwapping ? 'animate-spin' : ''}`} aria-hidden="true" />
                                                    換一道
                                                </Button>
                                            </div>
                                        </div>
                                    </div>
                                </Card>
                            </motion.div>
                        );
                    })}
                </div>
            </div>

            {/* Fixed Bottom Bar for Generate Menu */}
            <div className="fixed bottom-0 left-0 right-0 p-4 bg-background/95 backdrop-blur border-t z-50">
                <div className="container max-w-4xl mx-auto">
                    <Button
                        onClick={() => {
                            if (allDecided) {
                                const finalMenu = {
                                    recommendation_id: data.recommendation_id,
                                    restaurant_name: data.restaurant_name,
                                    cuisine_type: data.cuisine_type,
                                    dishes: dishSlots.map(slot => slot.display),
                                    total_price: totalPrice,
                                    party_size: parseInt(searchParams.get("people") || "2")
                                };
                                localStorage.setItem('final_menu', JSON.stringify(finalMenu));
                                router.push('/menu');
                            }
                        }}
                        disabled={!allDecided}
                        className="w-full h-12 text-lg font-bold gap-2 bg-primary hover:bg-primary/90 shadow-lg shadow-primary/20"
                        aria-label={allDecided ? "產出最終點餐菜單" : "請先確認所有菜品"}
                        aria-disabled={!allDecided}
                    >
                        <Check className="w-5 h-5" aria-hidden="true" />
                        {allDecided ? "產出點餐菜單" : `還有 ${Array.from(slotStatus.values()).filter(s => s === 'pending').length} 道菜未確認`}
                    </Button>
                </div>
            </div>

            {/* FE-039: Empty Candidate Pool Dialog */}
            <AlertDialog open={showEmptyPoolDialog} onOpenChange={setShowEmptyPoolDialog}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <div className="flex items-center gap-2 mb-2">
                            <Info className="w-5 h-5 text-blue-600" />
                            <AlertDialogTitle className="text-foreground">該類別暫無更多推薦</AlertDialogTitle>
                        </div>
                        <AlertDialogDescription className="text-muted-foreground">
                            目前 <span className="font-semibold text-foreground">{emptyPoolCategory}</span> 類別已經沒有更多菜品可以推薦了。
                            {swappedDishes.get(emptyPoolCategory)?.length ? (
                                <span className="block mt-2">
                                    您之前換掉了 {swappedDishes.get(emptyPoolCategory)?.length} 道菜，可以查看並重新考慮。
                                </span>
                            ) : null}
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter className="flex-col sm:flex-row gap-2">
                        <AlertDialogCancel onClick={handleKeepCurrentDish} className="w-full sm:w-auto">
                            保留當前菜品
                        </AlertDialogCancel>
                        {swappedDishes.get(emptyPoolCategory)?.length ? (
                            <AlertDialogAction
                                onClick={handleViewSwappedDishes}
                                className="w-full sm:w-auto bg-primary hover:bg-primary/90"
                            >
                                查看之前換掉的菜品
                            </AlertDialogAction>
                        ) : (
                            <AlertDialogAction
                                onClick={handleKeepCurrentDish}
                                className="w-full sm:w-auto bg-primary hover:bg-primary/90"
                            >
                                確定
                            </AlertDialogAction>
                        )}
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>

            {/* FE-040: Over Budget Warning Dialog */}
            <AlertDialog open={showBudgetWarning} onOpenChange={setShowBudgetWarning}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <div className="flex items-center gap-2 mb-2">
                            <AlertTriangle className="w-5 h-5 text-orange-600" />
                            <AlertDialogTitle className="text-foreground">超出預算警告</AlertDialogTitle>
                        </div>
                        <AlertDialogDescription className="text-muted-foreground space-y-3">
                            <p>
                                {budgetType === "person" ? "目前人均價格" : "目前菜單總價"} <span className="font-bold text-orange-600">NT$ {comparisonPrice.toLocaleString()}</span> 已超出您的{budgetType === "person" ? "每人預算" : "總預算"} <span className="font-semibold text-foreground">NT$ {budgetAmount.toLocaleString()}</span>
                            </p>
                            <p className="text-sm">
                                超出預算約 <span className="font-bold text-orange-600">{budgetExceedPercentage}%</span>，建議您返回調整預算或重新選擇菜品。
                            </p>
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter className="flex-col sm:flex-row gap-2">
                        <AlertDialogCancel onClick={handleAdjustBudget} className="w-full sm:w-auto">
                            返回修改偏好
                        </AlertDialogCancel>
                        <AlertDialogAction
                            onClick={handleContinueOverBudget}
                            className="w-full sm:w-auto bg-orange-600 hover:bg-orange-700"
                        >
                            繼續（不調整預算）
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </div>
    );
}

export default function RecommendationPage() {
    return (
        <Suspense fallback={<RecommendationSkeleton />}>
            <RecommendationPageContent />
        </Suspense>
    );
}