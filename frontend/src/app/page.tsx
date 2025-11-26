"use client";

import { useSession, signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { BrandHeader } from "@/components/brand-header";
import { FeatureShowcaseDynamic } from "@/lib/dynamic-imports";
import { motion } from "framer-motion";

export default function LandingPage() {
    const { status } = useSession();
    const router = useRouter();

    useEffect(() => {
        if (status === "authenticated") {
            router.push("/input");
        }
    }, [status, router]);

    if (status === "loading") {
        return (
            <div className="flex min-h-screen items-center justify-center bg-background">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
            </div>
        );
    }

    if (status === "authenticated") {
        return null; // Will redirect
    }

    return (
        <main className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5">
            {/* Hero Section with Two-Column Layout */}
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="grid gap-12 py-16 lg:grid-cols-2 lg:gap-16 lg:py-24">
                    {/* Left Column - Brand & Features */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.6 }}
                        className="flex flex-col justify-center space-y-8"
                    >
                        <BrandHeader />
                        <FeatureShowcaseDynamic />
                    </motion.div>

                    {/* Right Column - Login Card */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="flex items-center justify-center"
                    >
                        <Card className="w-full max-w-md border-border bg-card/80 backdrop-blur-sm shadow-xl">
                            <div className="p-8">
                                {/* Card Header */}
                                <div className="mb-8 space-y-2 text-center">
                                    <h2 className="text-2xl font-bold text-foreground">開始使用 Carte</h2>
                                    <p className="text-sm text-muted-foreground">
                                        30 秒快速決定吃什麼
                                    </p>
                                </div>

                                {/* Social Login */}
                                <div className="space-y-4">
                                    <Button
                                        className="w-full h-12 bg-primary text-primary-foreground hover:bg-primary/90"
                                        onClick={() => signIn("google", { callbackUrl: "/input" })}
                                    >
                                        <svg
                                            className="mr-2 h-5 w-5"
                                            viewBox="0 0 488 512"
                                            fill="currentColor"
                                        >
                                            <path d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z" />
                                        </svg>
                                        使用 Google 登入
                                    </Button>

                                    <Button
                                        variant="outline"
                                        className="w-full h-12 border-border hover:bg-secondary bg-transparent"
                                        disabled
                                    >
                                        Facebook (即將推出)
                                    </Button>
                                </div>

                                {/* Features List */}
                                <div className="mt-8 space-y-2">
                                    {[
                                        "✓ 分析 Google 評論尋找人氣菜色",
                                        "✓ 符合你的預算和飲食偏好",
                                        "✓ 30 秒快速決定吃什麼"
                                    ].map((feature, i) => (
                                        <div key={i} className="flex items-center gap-2 text-sm text-muted-foreground">
                                            <span className="text-primary font-bold">{feature.split(" ")[0]}</span>
                                            <span>{feature.substring(2)}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </Card>
                    </motion.div>
                </div>
            </div>

            {/* Trust Section - Bottom */}
            <div className="border-t border-border bg-card/30 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
                    <p className="text-sm text-muted-foreground">
                        被全台灣的美食愛好者信任 • 智慧推薦 • 個人化體驗
                    </p>
                </div>
            </div>
        </main>
    );
}
