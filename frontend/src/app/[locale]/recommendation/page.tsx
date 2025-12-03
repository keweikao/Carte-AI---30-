"use client";

import { useState, useEffect, Suspense, useRef, useMemo } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { useTranslations, useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Check, AlertCircle, ArrowLeft, CheckCircle2, RotateCw, Info, Crown } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";
import { getAlternatives, finalizeOrder, requestAddOn, UserInputV2, getRecommendationsAsync } from "@/lib/api";
import { DishCardSkeleton } from "@/components/dish-card-skeleton";
// import { CategoryHeader } from "@/components/category-header";
import { RecommendationSummary } from "@/components/recommendation-summary";
import { AddOnSection } from "@/components/add-on-section";
import { getSortedCategories } from "@/constants/categories";
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
    currency?: string;
}

// Define interfaces for component props for type safety
import { AgentFocusLoader } from "@/components/agent-focus-loader";

interface ErrorStateProps {
    error: string | null;
}

// Re-usable error component
function ErrorState({ error }: ErrorStateProps) {
    const t = useTranslations('RecommendationPage');
    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center space-y-4 bg-background" role="alert" aria-live="assertive">
            <AlertCircle className="w-16 h-16 text-destructive" aria-hidden="true" />
            <h2 className="text-2xl font-bold text-foreground">{t('error_title')}</h2>
            <p className="text-muted-foreground">{error}</p>
            <Link href="/input">
                <Button className="bg-primary text-primary-foreground hover:bg-primary/90" aria-label={t('back_button')}>{t('back_button')}</Button>
            </Link>
        </div>
    );
}

// Skeleton state for when recommendations are being prepared
function RecommendationSkeleton() {
    const t = useTranslations('RecommendationPage');
    return (
        <div className="relative min-h-screen bg-background pb-32 font-sans">
            <div className="absolute inset-0 w-full h-full overflow-y-auto">
                {/* Header */}
                <div className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur">
                    <div className="container flex h-14 items-center justify-between px-4">
                        <Button variant="ghost" disabled className="gap-2">
                            <ArrowLeft className="w-4 h-4" />{t('back_button')}
                        </Button>
                        <Button disabled className="gap-2 bg-primary hover:bg-primary/90">
                            <Check className="w-4 h-4" />{t('generate_menu_button')}
                        </Button>
                    </div>
                </div>

                {/* Sticky Price Summary - Skeleton */}
                <div className="bg-background/95 backdrop-blur-sm sticky top-14 z-10 px-6 py-4 shadow-sm border-b">
                    <div className="flex justify-between items-end mb-2">
                        <div>
                            <p className="text-xs text-muted-foreground mb-1 uppercase tracking-wider">{t('total_price')}</p>
                            <div className="h-9 w-32 bg-cream-200 rounded animate-skeleton" />
                        </div>
                        <div className="text-right">
                            <p className="text-xs text-muted-foreground mb-1">{t('per_person')}</p>
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
    const t = useTranslations('RecommendationPage');
    const locale = useLocale();
    const searchParams = useSearchParams();
    const router = useRouter();
    const { data: session } = useSession();
    const startTimeRef = useRef(Date.now());

    // Core states
    const [initialLoading, setInitialLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [data, setData] = useState<RecommendationData | null>(null);
    const [jobId, setJobId] = useState<string | null>(null);

    // V3 states
    const [dishSlots, setDishSlots] = useState<DishSlot[]>([]);
    const [slotStatus, setSlotStatus] = useState<Map<string, 'pending' | 'selected'>>(new Map());
    const [swappingSlots, setSwappingSlots] = useState<Set<number>>(new Set());

    // Dialog states for FE-039 and FE-040
    const [showEmptyPoolDialog, setShowEmptyPoolDialog] = useState(false);
    const [emptyPoolCategory, setEmptyPoolCategory] = useState<string>("");
    const [emptyPoolSlotIndex, setEmptyPoolSlotIndex] = useState<number>(-1);


    // Track swapped dishes for "view previously swapped" feature
    const [swappedDishes, setSwappedDishes] = useState<Map<string, MenuItem[]>>(new Map());

    // Track add-on operation
    const [isAddingDish, setIsAddingDish] = useState(false);

    // Start async job
    useEffect(() => {
        if (!session || jobId) return; // Only start once

        const startJob = async () => {
            try {
                setError(null);
                setInitialLoading(true);

                // Build request from URL params
                const restaurant_name = searchParams.get("restaurant") || "";
                const place_id = searchParams.get("place_id") || undefined;
                const party_size = parseInt(searchParams.get("people") || "2");
                const rawMode = searchParams.get("mode");
                const dining_style = (rawMode === "Shared" || rawMode === "sharing") ? "Shared" : "Individual";
                const dish_count_str = searchParams.get("dish_count");
                const budgetStr = searchParams.get("budget") || "";
                const occasion = searchParams.get("occasion") || undefined;

                const requestData: UserInputV2 = {
                    restaurant_name,
                    place_id,
                    party_size,
                    dining_style,
                    budget: undefined,
                    dish_count_target: dish_count_str ? parseInt(dish_count_str) : null,
                    preferences: searchParams.get("dietary")?.split(",").filter(p => p) || [],
                    occasion,
                    language: locale, // Dynamic language
                };

                if (!requestData.restaurant_name) {
                    throw new Error(t('error_restaurant_required'));
                }

                // @ts-expect-error - id_token exists on session but not in type definition
                const token = session?.id_token;

                // Start async job
                const jobResponse = await getRecommendationsAsync(requestData, token);
                setJobId(jobResponse.job_id);

            } catch (err) {
                const error = err as Error;
                console.error("Job start error:", error);
                let message = error.message || t('error_job_start');
                if (message.includes("504")) message = t('error_timeout');
                if (message.includes("500")) message = t('error_server');
                setError(message);
                setInitialLoading(false);
            }
        };

        startJob();
    }, [searchParams, session, jobId, locale, t]);

    // Calculate dynamic totals based on SELECTED items
    const selectedTotalPrice = useMemo(() => {
        return dishSlots.reduce((total, slot) => {
            const status = slotStatus.get(slot.display.dish_name);
            if (status === 'selected') {
                return total + (slot.display.price * slot.display.quantity);
            }
            return total;
        }, 0);
    }, [dishSlots, slotStatus]);

    const perPerson = Math.round(selectedTotalPrice / (parseInt(searchParams.get("people") || "2")));

    // Check if "All Signatures" mode
    const isAllSignaturesMode = searchParams.get("occasion") === "all_signatures";

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

    const handleSelect = (dishName: string, _: number) => {
        setSlotStatus(prev => {
            const newStatus = new Map(prev);
            const currentStatus = newStatus.get(dishName);

            if (currentStatus === 'selected') {
                // Toggle to unselected (pending)
                newStatus.set(dishName, 'pending');
            } else {
                // Toggle to selected
                newStatus.set(dishName, 'selected');
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

    // Handle add-on request
    const handleAddOn = async (category: string) => {
        if (!data) return;

        setIsAddingDish(true);
        try {
            // @ts-expect-error - id_token exists on session but not in type definition
            const token = session?.id_token;

            const response = await requestAddOn(data.recommendation_id, category, 1, token);

            if (response.new_dishes && response.new_dishes.length > 0) {
                const newDish = response.new_dishes[0];

                // Create a new dish slot for the added dish
                const newSlot: DishSlot = {
                    category: category,
                    display: newDish,
                    alternatives: []
                };

                // const newSlotIndex = dishSlots.length;

                // Add to dish slots
                setDishSlots(prev => [...prev, newSlot]);

                // Add to slot status
                setSlotStatus(prev => {
                    const newMap = new Map(prev);
                    newMap.set(newDish.dish_name, 'pending');
                    return newMap;
                });

                // Update total price
                // setTotalPrice(prev => prev + (newDish.price * newDish.quantity));

                // Show success message (you can add a toast here)
                console.log(`${t('add_success')}${newDish.dish_name}`);
            }
        } catch (error) {
            console.error('Failed to add on:', error);
            alert(`${t('add_failed')}${error instanceof Error ? error.message : '未知錯誤'}`);
        } finally {
            setIsAddingDish(false);
        }
    };



    const handleBackToSettings = () => {
        router.push(`/input?${searchParams.toString()}`);
    };

    // Group dishes by category
    const groupedByCategory = useMemo(() => {
        if (!dishSlots || dishSlots.length === 0) return new Map();

        const grouped = new Map<string, DishSlot[]>();
        dishSlots.forEach((slot) => {
            const category = slot.category;
            if (!grouped.has(category)) {
                grouped.set(category, []);
            }
            grouped.get(category)!.push(slot);
        });

        return grouped;
    }, [dishSlots]);

    // Get sorted categories
    const orderedCategories = useMemo(() => {
        if (!data) return [];

        const categories = Array.from(groupedByCategory.keys());
        return getSortedCategories(categories, data.cuisine_type);
    }, [groupedByCategory, data]);

    if (initialLoading && jobId) {
        return (
            <AgentFocusLoader
                jobId={jobId}
                onComplete={(result: RecommendationData) => {
                    setData(result);
                    setDishSlots(result.items);
                    const initialStatus = new Map<string, 'pending' | 'selected'>();
                    // Default to pending (let user select)
                    result.items.forEach((slot: DishSlot) => initialStatus.set(slot.display.dish_name, 'pending'));
                    setSlotStatus(initialStatus);
                    setInitialLoading(false);
                }}
                onError={(errorMsg: string) => {
                    setError(errorMsg);
                    setInitialLoading(false);
                }}
            />
        );
    }
    if (initialLoading) return <RecommendationSkeleton />;
    if (error) return <ErrorState error={error} />;
    if (!data) return null;




    return (
        <div className="relative min-h-screen bg-background pb-32 font-sans">
            <div className="absolute inset-0 w-full h-full overflow-y-auto">
                <div className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur" role="banner">
                    <div className="container flex h-14 items-center justify-between px-2 sm:px-4 gap-2">
                        <Button variant="ghost" onClick={handleBackToSettings} className="gap-1 sm:gap-2 text-sm sm:text-base px-2 sm:px-4" aria-label={t('back_button')}><ArrowLeft className="w-4 h-4" aria-hidden="true" />{t('back_button')}</Button>

                    </div>
                </div>

                <div className="bg-background/95 backdrop-blur-sm sticky top-14 z-10 px-4 sm:px-6 py-4 shadow-sm border-b" role="region" aria-label="價格摘要">
                    <div className="flex justify-between items-end mb-2">
                        <div>
                            <p className="text-xs text-muted-foreground mb-1 uppercase tracking-wider">{t('total_price')}</p>
                            <h1 className="text-2xl sm:text-3xl font-bold text-foreground font-mono transition-colors duration-300" aria-live="polite">{data.currency || 'NT$'} {selectedTotalPrice.toLocaleString()}</h1>
                        </div>
                        <div className="text-right">
                            <p className="text-xs text-muted-foreground mb-1">{t('per_person')}</p>
                            <p className="text-lg sm:text-xl font-bold text-orange-600 font-mono" aria-live="polite">{data.currency || 'NT$'} {perPerson.toLocaleString()}</p>
                        </div>
                    </div>
                </div>

                <div className="p-4 pb-32" role="list" aria-label="推薦菜品列表">
                    {/* Recommendation Summary */}
                    <RecommendationSummary
                        totalDishes={dishSlots.length}
                        categorySummary={data.category_summary}
                    />

                    {/* Mode Badge */}
                    {isAllSignaturesMode && (
                        <div className="flex items-center justify-center gap-2 mb-6 bg-yellow-100 border border-yellow-300 text-yellow-800 px-4 py-2 rounded-full shadow-sm">
                            <Crown className="w-5 h-5 fill-yellow-500 text-yellow-600" />
                            <span className="font-bold">{t('mode_all_signatures')}</span>
                        </div>
                    )}

                    {/* Category Sections */}
                    {orderedCategories.map((category) => {
                        const slotsInCategory = groupedByCategory.get(category)!;

                        return (
                            <div key={category} className="mb-8">
                                {/* CategoryHeader Removed */}

                                <div className="space-y-4">
                                    {slotsInCategory.map((slot: DishSlot) => {
                                        // Find original index for swap/select handlers
                                        const index = dishSlots.findIndex(
                                            (s) => s.display.dish_name === slot.display.dish_name
                                        );
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
                                                                <span className="text-lg font-mono font-semibold text-foreground" aria-label={`價格 ${slot.display.price} 元`}>
                                                                    {slot.display.price > 0 ? `${data.currency || 'NT$'} ${slot.display.price}` : t('price_on_site')}
                                                                </span>
                                                            </div>
                                                            <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">&ldquo;{slot.display.reason}&rdquo;</p>

                                                            <div className="flex items-center gap-2 mt-4" role="group" aria-label="菜品操作">
                                                                <Button
                                                                    size="sm"
                                                                    className={`flex-1 h-9 rounded-full ${status === 'selected' ? 'bg-green-600 hover:bg-green-700' : 'bg-secondary hover:bg-secondary/80 text-secondary-foreground'} transition-colors`}
                                                                    onClick={() => handleSelect(slot.display.dish_name, index)}
                                                                    aria-label={status === 'selected' ? `移除 ${slot.display.dish_name}` : `加入 ${slot.display.dish_name}`}
                                                                    aria-pressed={status === 'selected'}
                                                                >
                                                                    {status === 'selected' ? (
                                                                        <>
                                                                            <CheckCircle2 className="w-4 h-4 mr-1.5" aria-hidden="true" />
                                                                            {t('selected')}
                                                                        </>
                                                                    ) : (
                                                                        <>
                                                                            <span className="mr-1.5 text-lg leading-none">+</span>
                                                                            {t('add_dish')}
                                                                        </>
                                                                    )}
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
                                                                    {t('swap_dish')}
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
                        );
                    })}

                    {/* Add-On Section - Moved inside scrollable container */}
                    <div className="mt-8">
                        <AddOnSection onAddOn={handleAddOn} isLoading={isAddingDish} />
                    </div>
                </div>
            </div>

            {/* Fixed Bottom Bar for Generate Menu */}
            <div className="fixed bottom-0 left-0 right-0 p-4 bg-background/95 backdrop-blur border-t z-50">
                <div className="container max-w-4xl mx-auto">
                    <Button
                        onClick={async () => {
                            if (selectedTotalPrice > 0) {
                                try {
                                    // Calculate session duration
                                    const duration = Math.floor((Date.now() - startTimeRef.current) / 1000);

                                    // Filter only SELECTED dishes
                                    const selectedSlots = dishSlots.filter(slot => slotStatus.get(slot.display.dish_name) === 'selected');

                                    // Track finalization
                                    // Track finalization
                                    await finalizeOrder(data.recommendation_id, {
                                        final_selections: selectedSlots.map(slot => ({
                                            dish_name: slot.display.dish_name,
                                            category: slot.category,
                                            price: slot.display.price,
                                        })),
                                        total_price: selectedTotalPrice,
                                        session_duration_seconds: duration,
                                        recommended_count: dishSlots.length,
                                        selected_count: selectedSlots.length
                                    });
                                } catch (e) {
                                    console.error("Failed to track order finalization:", e);
                                    // Proceed anyway
                                }

                                const selectedSlots = dishSlots.filter(slot => slotStatus.get(slot.display.dish_name) === 'selected');
                                const finalMenu = {
                                    recommendation_id: data.recommendation_id,
                                    restaurant_name: data.restaurant_name,
                                    cuisine_type: data.cuisine_type,
                                    dishes: selectedSlots.map(slot => slot.display),
                                    total_price: selectedTotalPrice,
                                    party_size: parseInt(searchParams.get("people") || "2"),
                                    original_params: {
                                        restaurant: searchParams.get("restaurant"),
                                        people: searchParams.get("people"),
                                        dietary: searchParams.get("dietary"),
                                        mode: searchParams.get("mode"),
                                        occasion: searchParams.get("occasion"),
                                        place_id: searchParams.get("place_id")
                                    }
                                };
                                localStorage.setItem('final_menu', JSON.stringify(finalMenu));
                                router.push('/menu');
                            } else {
                                alert(t('error_no_selection'));
                            }
                        }}
                        // disabled={selectedTotalPrice === 0} // Removed as per user request
                        className="w-full h-12 text-lg font-bold gap-2 bg-primary hover:bg-primary/90 shadow-lg shadow-primary/20"
                        aria-label={t('generate_menu_button')}
                    >
                        <Check className="w-5 h-5" aria-hidden="true" />
                        {t('generate_menu_button')} ({dishSlots.filter(slot => slotStatus.get(slot.display.dish_name) === 'selected').length} 道)
                    </Button>
                </div>
            </div>

            {/* FE-039: Empty Candidate Pool Dialog */}
            <AlertDialog open={showEmptyPoolDialog} onOpenChange={setShowEmptyPoolDialog}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <div className="flex items-center gap-2 mb-2">
                            <Info className="w-5 h-5 text-blue-600" />
                            <AlertDialogTitle className="text-foreground">{t('empty_pool_title')}</AlertDialogTitle>
                        </div>
                        <AlertDialogDescription className="text-muted-foreground">
                            {t('empty_pool_desc', { category: emptyPoolCategory })}
                            {swappedDishes.get(emptyPoolCategory)?.length ? (
                                <span className="block mt-2">
                                    {t('empty_pool_swapped_desc', { count: swappedDishes.get(emptyPoolCategory)?.length || 0 })}
                                </span>
                            ) : null}
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter className="flex-col sm:flex-row gap-2">
                        <AlertDialogCancel onClick={handleKeepCurrentDish} className="w-full sm:w-auto">
                            {t('keep_current')}
                        </AlertDialogCancel>
                        {swappedDishes.get(emptyPoolCategory)?.length ? (
                            <AlertDialogAction
                                onClick={handleViewSwappedDishes}
                                className="w-full sm:w-auto bg-primary hover:bg-primary/90"
                            >
                                {t('view_swapped')}
                            </AlertDialogAction>
                        ) : (
                            <AlertDialogAction
                                onClick={handleKeepCurrentDish}
                                className="w-full sm:w-auto bg-primary hover:bg-primary/90"
                            >
                                {t('confirm')}
                            </AlertDialogAction>
                        )}
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