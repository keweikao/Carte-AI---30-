"use client";

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
    Sparkles,
    Users,
    Clock,
    ChefHat,
    MessageSquare,
    ArrowRight,
    Check
} from "lucide-react";
import { CarteHeader, CarteFooter } from "@/components/carte";
import { cn } from "@/lib/utils";

export default function LandingPage() {
    const { status } = useSession();
    const router = useRouter();
    const [isScrolled, setIsScrolled] = useState(false);

    // Auto redirect if authenticated
    useEffect(() => {
        if (status === "authenticated") {
            // Check if onboarded
            const onboarded = localStorage.getItem("carte_onboarded");
            if (onboarded === "true") {
                router.push("/zh/input");
            } else {
                router.push("/zh/onboarding");
            }
        }
    }, [status, router]);

    // Scroll detection
    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50);
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    if (status === "loading") {
        return (
            <div className="flex min-h-screen items-center justify-center bg-cream">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-caramel" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-cream">
            {/* Header */}
            <CarteHeader />

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 md:pt-40 md:pb-32 overflow-hidden">
                {/* Background decoration */}
                <div className="absolute inset-0 bg-gradient-to-b from-cream via-cream-100 to-cream opacity-50" />

                <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                    <div className="max-w-4xl mx-auto text-center">
                        {/* Tagline */}
                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6 }}
                            className="text-caramel font-medium tracking-wider text-sm uppercase mb-6"
                        >
                            Your Personal Menu Curator
                        </motion.p>

                        {/* Headline */}
                        <motion.h1
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.1 }}
                            className="font-serif text-4xl md:text-5xl lg:text-6xl font-bold text-charcoal mb-6 leading-tight"
                        >
                            讓 AI 為你策劃
                            <br />
                            完美的用餐體驗
                        </motion.h1>

                        {/* Subheadline */}
                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="text-lg md:text-xl text-gray-600 mb-10 max-w-2xl mx-auto"
                        >
                            不再為點餐煩惱。告訴我們你的喜好與情境，Carte AI 將從菜單中為你精選最適合的菜色組合。
                        </motion.p>

                        {/* CTAs */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="flex flex-col sm:flex-row items-center justify-center gap-4"
                        >
                            <Link
                                href="/zh/input"
                                className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-medium text-white bg-gradient-to-r from-caramel to-terracotta rounded-full hover:opacity-90 hover:shadow-prominent transition-all"
                            >
                                開始探索菜單
                                <ArrowRight className="w-5 h-5" />
                            </Link>

                            <a
                                href="#how-it-works"
                                className="inline-flex items-center gap-2 text-charcoal hover:text-caramel transition-colors font-medium"
                            >
                                了解運作方式 →
                            </a>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-20 md:py-32 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    {/* Section Title */}
                    <div className="text-center mb-16">
                        <h2 className="font-serif text-3xl md:text-4xl font-bold text-charcoal mb-4">
                            為什麼選擇 Carte AI
                        </h2>
                    </div>

                    {/* Feature Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                        {[
                            {
                                icon: Sparkles,
                                title: "智慧推薦",
                                description: "AI 分析數千則評論與菜單資訊，找出最適合你的選擇"
                            },
                            {
                                icon: Users,
                                title: "情境感知",
                                description: "約會、商務、家庭聚餐？我們根據不同場合調整推薦策略"
                            },
                            {
                                icon: Clock,
                                title: "節省時間",
                                description: "30 秒完成輸入，獲得專業級的點餐建議"
                            }
                        ].map((feature, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.6, delay: index * 0.1 }}
                                className="bg-cream rounded-2xl p-8 hover:shadow-medium transition-shadow"
                            >
                                <div className="w-12 h-12 bg-caramel/10 rounded-full flex items-center justify-center mb-6">
                                    <feature.icon className="w-6 h-6 text-caramel" />
                                </div>
                                <h3 className="font-serif text-xl font-bold text-charcoal mb-3">
                                    {feature.title}
                                </h3>
                                <p className="text-gray-600">
                                    {feature.description}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section id="how-it-works" className="py-20 md:py-32 bg-cream">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    {/* Section Title */}
                    <div className="text-center mb-16">
                        <h2 className="font-serif text-3xl md:text-4xl font-bold text-charcoal mb-4">
                            簡單四步驟
                        </h2>
                    </div>

                    {/* Steps */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
                        {[
                            {
                                number: "01",
                                title: "選擇餐廳",
                                description: "搜尋或輸入你想去的餐廳名稱"
                            },
                            {
                                number: "02",
                                title: "設定情境",
                                description: "告訴我們用餐目的與人數"
                            },
                            {
                                number: "03",
                                title: "AI 分析",
                                description: "我們即時分析菜單與評論"
                            },
                            {
                                number: "04",
                                title: "獲得推薦",
                                description: "收到個人化的菜色組合建議"
                            }
                        ].map((step, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.6, delay: index * 0.1 }}
                                className="text-center"
                            >
                                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-caramel to-terracotta rounded-full text-white font-serif text-2xl font-bold mb-6">
                                    {step.number}
                                </div>
                                <h3 className="font-serif text-xl font-bold text-charcoal mb-3">
                                    {step.title}
                                </h3>
                                <p className="text-gray-600">
                                    {step.description}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Testimonials Section */}
            <section className="py-20 md:py-32 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    {/* Section Title */}
                    <div className="text-center mb-16">
                        <h2 className="font-serif text-3xl md:text-4xl font-bold text-charcoal mb-4">
                            用戶怎麼說
                        </h2>
                    </div>

                    {/* Testimonial Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                        {[
                            {
                                quote: "終於不用在餐廳門口研究菜單半小時了！",
                                author: "Amy L.",
                                context: "約會常客"
                            },
                            {
                                quote: "帶客戶吃飯時超有面子，每道菜都點到他們的心坎裡。",
                                author: "Kevin C.",
                                context: "業務經理"
                            },
                            {
                                quote: "家族聚餐眾口難調？Carte AI 幫我搞定一切。",
                                author: "Michelle W.",
                                context: "家庭主婦"
                            }
                        ].map((testimonial, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.6, delay: index * 0.1 }}
                                className="bg-cream rounded-2xl p-8"
                            >
                                <MessageSquare className="w-8 h-8 text-caramel mb-4" />
                                <p className="text-charcoal mb-6 italic">
                                    "{testimonial.quote}"
                                </p>
                                <div>
                                    <p className="font-semibold text-charcoal">
                                        {testimonial.author}
                                    </p>
                                    <p className="text-sm text-gray-500">
                                        {testimonial.context}
                                    </p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Final CTA Section */}
            <section className="py-20 md:py-32 bg-gradient-to-br from-caramel to-terracotta">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="max-w-3xl mx-auto"
                    >
                        <h2 className="font-serif text-3xl md:text-4xl font-bold text-white mb-6">
                            準備好探索你的下一餐了嗎？
                        </h2>
                        <Link
                            href="/zh/input"
                            className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-medium text-charcoal bg-white rounded-full hover:bg-cream transition-all shadow-floating"
                        >
                            <ChefHat className="w-5 h-5" />
                            免費開始使用
                        </Link>
                        <p className="mt-4 text-white/80 text-sm">
                            無需註冊，立即體驗
                        </p>
                    </motion.div>
                </div>
            </section>

            {/* Footer */}
            <CarteFooter />
        </div>
    );
}
