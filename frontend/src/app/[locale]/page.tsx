"use client";

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { useLocale, useTranslations } from "next-intl";
import {
    Sparkles,
    Users,
    Clock,
    ChefHat,
    MessageSquare,
    ArrowRight
} from "lucide-react";
import { CarteHeader, CarteFooter } from "@/components/carte";

export default function LandingPage() {
    const { status } = useSession();
    const router = useRouter();
    const locale = useLocale();
    const t = useTranslations('HomePage');
    const localePrefix = locale || 'zh-TW';

    // Auto redirect if authenticated
    useEffect(() => {
        if (status === "authenticated") {
            // Check if onboarded
            const onboarded = localStorage.getItem("carte_onboarded");
            if (onboarded === "true") {
                router.push(`/${localePrefix}/input`);
            } else {
                router.push(`/${localePrefix}/onboarding`);
            }
        }
    }, [status, router, localePrefix]);

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
                            {t('tagline')}
                        </motion.p>

                        {/* Headline */}
                        <motion.h1
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.1 }}
                            className="font-serif text-4xl md:text-5xl lg:text-6xl font-bold text-charcoal mb-6 leading-tight"
                        >
                            {t('title')}
                            <br />
                            {t('title_line2')}
                        </motion.h1>

                        {/* Subheadline */}
                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="text-lg md:text-xl text-gray-600 mb-10 max-w-2xl mx-auto"
                        >
                            {t('subtitle')}
                        </motion.p>

                        {/* CTAs */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="flex flex-col sm:flex-row items-center justify-center gap-4"
                        >
                            <Link
                                href={`/${localePrefix}/input`}
                                className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-medium text-white bg-gradient-to-r from-caramel to-terracotta rounded-full hover:opacity-90 hover:shadow-prominent transition-all"
                            >
                                {t('start_button')}
                                <ArrowRight className="w-5 h-5" />
                            </Link>

                            <a
                                href="#how-it-works"
                                className="inline-flex items-center gap-2 text-charcoal hover:text-caramel transition-colors font-medium"
                            >
                                {t('learn_more')} →
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
                            {t('features_title')}
                        </h2>
                    </div>

                    {/* Feature Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                        {[
                            {
                                icon: Sparkles,
                                title: t('feature1_title'),
                                description: t('feature1_desc')
                            },
                            {
                                icon: Users,
                                title: t('feature2_title'),
                                description: t('feature2_desc')
                            },
                            {
                                icon: Clock,
                                title: t('feature3_title'),
                                description: t('feature3_desc')
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
                            {t('how_it_works_title')}
                        </h2>
                    </div>

                    {/* Steps */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
                        {[
                            {
                                number: "01",
                                title: t('step1_title'),
                                description: t('step1_desc')
                            },
                            {
                                number: "02",
                                title: t('step2_title'),
                                description: t('step2_desc')
                            },
                            {
                                number: "03",
                                title: t('step3_title'),
                                description: t('step3_desc')
                            },
                            {
                                number: "04",
                                title: t('step4_title'),
                                description: t('step4_desc')
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
                            {t('testimonials_title')}
                        </h2>
                    </div>

                    {/* Testimonial Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                        {[
                            {
                                quote: t('testimonial1_quote'),
                                author: t('testimonial1_author'),
                                context: t('testimonial1_context')
                            },
                            {
                                quote: t('testimonial2_quote'),
                                author: t('testimonial2_author'),
                                context: t('testimonial2_context')
                            },
                            {
                                quote: t('testimonial3_quote'),
                                author: t('testimonial3_author'),
                                context: t('testimonial3_context')
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
                                    &ldquo;{testimonial.quote}&rdquo;
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
                            {t('cta_title')}
                        </h2>
                        <Link
                            href={`/${localePrefix}/input`}
                            className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-medium text-charcoal bg-white rounded-full hover:bg-cream transition-all shadow-floating"
                        >
                            <ChefHat className="w-5 h-5" />
                            {t('cta_button')}
                        </Link>
                        <p className="mt-4 text-white/80 text-sm">
                            {t('cta_note')}
                        </p>
                    </motion.div>
                </div>
            </section>

            {/* Footer */}
            <CarteFooter />
        </div>
    );
}
