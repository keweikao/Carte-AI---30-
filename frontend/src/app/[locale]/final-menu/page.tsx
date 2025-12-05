"use client";

import { useState, useMemo } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import {
    Share2,
    ChefHat,
    Check,
    Copy,
    MessageCircle
} from "lucide-react";
import { CarteHeader, CarteFooter } from "@/components/carte";

interface MenuItem {
    name: string;
    price: number;
    quantity: number;
    category: string;
}

interface FinalMenuData {
    restaurant_name: string;
    items: MenuItem[];
    total_price: number;
    party_size: number;
    created_at: string;
}

export default function FinalMenuPage() {
    const router = useRouter();
    const searchParams = useSearchParams();

    const [copied, setCopied] = useState(false);
    const [shared, setShared] = useState(false);

    // 從 URL 載入資料 (使用 useMemo 避免 setState in effect)
    const menuData = useMemo<FinalMenuData | null>(() => {
        if (typeof window === "undefined") return null;

        const dataParam = searchParams.get("data");

        if (dataParam) {
            try {
                return JSON.parse(atob(dataParam));
            } catch {
                // 嘗試從 localStorage
                const stored = localStorage.getItem("carte_final_menu");
                if (stored) {
                    return JSON.parse(stored);
                }
            }
        } else {
            // 從 localStorage 載入
            const stored = localStorage.getItem("carte_final_menu");
            if (stored) {
                return JSON.parse(stored);
            }
        }
        return null;
    }, [searchParams]);

    // 複製菜單
    const handleCopy = async () => {
        if (!menuData) return;

        const text = formatMenuText(menuData);
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    // 分享菜單
    const handleShare = async () => {
        if (!menuData) return;

        const shareData = btoa(JSON.stringify(menuData));
        const shareUrl = `${window.location.origin}/final-menu?data=${shareData}`;

        if (navigator.share) {
            try {
                await navigator.share({
                    title: `${menuData.restaurant_name} - Carte AI 推薦菜單`,
                    text: formatMenuText(menuData),
                    url: shareUrl
                });
                setShared(true);
            } catch {
                // 用戶取消分享
            }
        } else {
            // Fallback: 複製連結
            await navigator.clipboard.writeText(shareUrl);
            setShared(true);
            setTimeout(() => setShared(false), 2000);
        }
    };

    // 格式化菜單文字
    const formatMenuText = (data: FinalMenuData): string => {
        let text = `📋 ${data.restaurant_name}\n`;
        text += `👥 ${data.party_size} 人用餐\n\n`;
        text += `━━━━━━━━━━━━━━\n`;

        data.items.forEach(item => {
            text += `${item.name} x${item.quantity} - $${item.price * item.quantity}\n`;
        });

        text += `━━━━━━━━━━━━━━\n`;
        text += `💰 總計: $${data.total_price}\n\n`;
        text += `由 Carte AI 推薦 ✨`;

        return text;
    };

    // 分類菜色
    const groupByCategory = (items: MenuItem[]) => {
        return items.reduce((acc, item) => {
            if (!acc[item.category]) {
                acc[item.category] = [];
            }
            acc[item.category].push(item);
            return acc;
        }, {} as Record<string, MenuItem[]>);
    };

    if (!menuData) {
        return (
            <div className="min-h-screen bg-cream flex items-center justify-center">
                <div className="text-center">
                    <ChefHat className="w-12 h-12 text-caramel mx-auto mb-4" />
                    <p className="text-gray-500">載入中...</p>
                </div>
            </div>
        );
    }

    const groupedItems = groupByCategory(menuData.items);

    return (
        <div className="min-h-screen bg-cream">
            <CarteHeader />

            <main className="pt-24 pb-32">
                <div className="container mx-auto px-4 max-w-2xl">
                    {/* 成功標題 */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center mb-8"
                    >
                        <div className="w-16 h-16 bg-gradient-to-br from-caramel to-terracotta rounded-full flex items-center justify-center mx-auto mb-6 shadow-prominent">
                            <Check className="w-8 h-8 text-white" />
                        </div>
                        <h1 className="font-serif text-3xl font-bold text-charcoal mb-2">
                            菜單已確認！
                        </h1>
                        <p className="text-gray-500">
                            {menuData.party_size} 人份的完美組合
                        </p>
                    </motion.div>

                    {/* 餐廳卡片 */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="bg-white rounded-2xl shadow-medium p-6 mb-6"
                    >
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-12 h-12 bg-caramel/10 rounded-full flex items-center justify-center">
                                <ChefHat className="w-6 h-6 text-caramel" />
                            </div>
                            <div>
                                <h2 className="font-serif text-xl font-bold text-charcoal">
                                    {menuData.restaurant_name}
                                </h2>
                                <p className="text-sm text-gray-500">
                                    {new Date(menuData.created_at).toLocaleDateString("zh-TW")}
                                </p>
                            </div>
                        </div>

                        {/* 菜色列表 */}
                        <div className="space-y-6">
                            {Object.entries(groupedItems).map(([category, items]) => (
                                <div key={category}>
                                    <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-3">
                                        {category}
                                    </h3>
                                    <div className="space-y-3">
                                        {items.map((item, index) => (
                                            <div
                                                key={index}
                                                className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
                                            >
                                                <div>
                                                    <p className="font-medium text-charcoal">
                                                        {item.name}
                                                    </p>
                                                    <p className="text-sm text-gray-400">
                                                        x{item.quantity}
                                                    </p>
                                                </div>
                                                <p className="font-medium text-charcoal">
                                                    ${item.price * item.quantity}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* 總計 */}
                        <div className="mt-6 pt-4 border-t-2 border-dashed border-gray-200">
                            <div className="flex items-center justify-between">
                                <span className="font-serif text-lg font-bold text-charcoal">
                                    總計
                                </span>
                                <span className="font-serif text-2xl font-bold text-caramel">
                                    ${menuData.total_price}
                                </span>
                            </div>
                            <p className="text-sm text-gray-400 mt-1">
                                約 ${Math.round(menuData.total_price / menuData.party_size)} / 人
                            </p>
                        </div>
                    </motion.div>

                    {/* 行動按鈕 */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="grid grid-cols-2 gap-4 mb-6"
                    >
                        <button
                            onClick={handleCopy}
                            className="flex items-center justify-center gap-2 px-6 py-4 bg-white rounded-xl shadow-subtle hover:shadow-medium transition-shadow font-medium text-charcoal"
                        >
                            {copied ? (
                                <>
                                    <Check className="w-5 h-5 text-green-500" />
                                    已複製
                                </>
                            ) : (
                                <>
                                    <Copy className="w-5 h-5" />
                                    複製菜單
                                </>
                            )}
                        </button>

                        <button
                            onClick={handleShare}
                            className="flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-caramel to-terracotta text-white rounded-xl shadow-medium hover:opacity-90 transition-opacity font-medium"
                        >
                            {shared ? (
                                <>
                                    <Check className="w-5 h-5" />
                                    已分享
                                </>
                            ) : (
                                <>
                                    <Share2 className="w-5 h-5" />
                                    分享給朋友
                                </>
                            )}
                        </button>
                    </motion.div>

                    {/* 提示 */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                        className="bg-caramel/10 rounded-xl p-4 flex items-start gap-3"
                    >
                        <MessageCircle className="w-5 h-5 text-caramel flex-shrink-0 mt-0.5" />
                        <div>
                            <p className="text-sm font-medium text-charcoal mb-1">
                                小提醒
                            </p>
                            <p className="text-sm text-gray-600">
                                實際價格以餐廳現場為準。如有任何飲食限制，請向服務人員確認。
                            </p>
                        </div>
                    </motion.div>

                    {/* 重新開始 */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.4 }}
                        className="text-center mt-8"
                    >
                        <button
                            onClick={() => router.push("/input")}
                            className="text-caramel hover:text-terracotta transition-colors font-medium"
                        >
                            探索其他餐廳 →
                        </button>
                    </motion.div>
                </div>
            </main>

            <CarteFooter />
        </div>
    );
}
