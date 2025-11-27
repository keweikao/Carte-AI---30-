"use client";

import { useEffect, useState, Suspense, useRef } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Share2, Printer, Star, Download, Copy, Check, Search } from "lucide-react";
import { motion } from "framer-motion";
import { Skeleton } from "@/components/ui/skeleton";
import type { MenuItem } from "@/types";
import { RatingModalDynamic } from "@/lib/dynamic-imports";
import { submitFeedback } from "@/lib/api";
import { useSession } from "next-auth/react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";

interface FinalMenu {
    recommendation_id: string;
    restaurant_name: string;
    cuisine_type: string;
    dishes: MenuItem[];
    total_price: number;
    party_size: number;
    currency?: string;
}

// Skeleton loading state for Menu Page
function MenuPageSkeleton() {
    return (
        <div className="min-h-screen bg-background pb-20">
            {/* Header */}
            <div className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur">
                <div className="container flex h-14 items-center justify-between px-4">
                    <Button variant="ghost" disabled className="gap-2">
                        <ArrowLeft className="w-4 h-4" />
                        返回修改
                    </Button>
                    <div className="flex gap-2">
                        <Button variant="outline" disabled className="gap-2">
                            <Printer className="w-4 h-4" />
                            列印
                        </Button>
                        <Button variant="outline" disabled className="gap-2">
                            <Share2 className="w-4 h-4" />
                            分享
                        </Button>
                        <Button disabled className="gap-2 bg-primary">
                            <Star className="w-4 h-4" />
                            評分
                        </Button>
                    </div>
                </div>
            </div>

            {/* Menu Content */}
            <div className="container max-w-4xl mx-auto px-4 py-8">
                {/* Header */}
                <div className="text-center mb-8">
                    <Skeleton className="h-6 w-20 mx-auto mb-4 rounded-full" />
                    <Skeleton className="h-10 w-64 mx-auto mb-2" />
                    <Skeleton className="h-5 w-40 mx-auto" />
                </div>

                {/* Price Summary */}
                <Card className="p-6 mb-8 bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
                    <div className="flex justify-between items-end">
                        <div>
                            <Skeleton className="h-4 w-20 mb-2" />
                            <Skeleton className="h-9 w-40" />
                        </div>
                        <div className="text-right">
                            <Skeleton className="h-4 w-16 mb-2" />
                            <Skeleton className="h-8 w-32" />
                        </div>
                    </div>
                </Card>

                {/* Dishes List */}
                <div className="space-y-4">
                    <Skeleton className="h-7 w-24 mb-4" />
                    {Array.from({ length: 5 }).map((_, index) => (
                        <Card key={index} className="p-4">
                            <div className="flex justify-between items-start gap-4">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-2">
                                        <Skeleton className="h-6 w-6" />
                                        <Skeleton className="h-6 w-40" />
                                        <Skeleton className="h-5 w-12 rounded-full" />
                                    </div>
                                    <Skeleton className="h-4 w-full mb-2" />
                                    <Skeleton className="h-4 w-4/5 mb-2" />
                                    <Skeleton className="h-3 w-24" />
                                </div>
                                <div className="text-right flex-shrink-0">
                                    <Skeleton className="h-6 w-20" />
                                </div>
                            </div>
                        </Card>
                    ))}
                </div>

                {/* Footer Note */}
                <div className="mt-8 text-center">
                    <Skeleton className="h-4 w-64 mx-auto" />
                </div>
            </div>
        </div>
    );
}

function MenuPageContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const { data: session } = useSession();
    const [menu, setMenu] = useState<FinalMenu | null>(null);
    const [showRatingModal, setShowRatingModal] = useState(false);
    const [copied, setCopied] = useState(false);
    const [shareImageUrl, setShareImageUrl] = useState<string | null>(null);
    const [showShareMenu, setShowShareMenu] = useState(false);
    const [showLocalLanguage, setShowLocalLanguage] = useState(false);
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        // Try to get menu from localStorage
        const storedMenu = localStorage.getItem('final_menu');
        if (storedMenu) {
            try {
                const parsedMenu = JSON.parse(storedMenu);
                // Use setTimeout to avoid synchronous state update warning
                setTimeout(() => setMenu(parsedMenu), 0);
            } catch (e) {
                console.error('Failed to parse stored menu:', e);
            }
        }

        // Or get from URL params (if passed)
        const recommendationId = searchParams.get('recommendation_id');
        if (recommendationId && !storedMenu) {
            // Could fetch from API if needed
            console.log('Recommendation ID:', recommendationId);
        }
    }, [searchParams]);

    const handleBack = () => {
        router.back();
    };

    const handlePrint = () => {
        window.print();
    };

    const generateShareImage = async () => {
        if (!menu || !canvasRef.current) return null;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        if (!ctx) return null;

        // Set canvas size
        canvas.width = 800;
        canvas.height = 650 + (menu.dishes.length * 65);

        // Background
        ctx.fillStyle = '#FFF8F0';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Header
        ctx.fillStyle = '#D4A574';
        ctx.fillRect(0, 0, canvas.width, 140);

        // Logo/Title
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 40px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('🍽️ Carte AI 推薦菜單', canvas.width / 2, 60);

        // Subtitle
        ctx.font = '18px sans-serif';
        ctx.fillStyle = '#FFFFFF';
        ctx.fillText('AI 智慧點餐助手', canvas.width / 2, 95);

        // Restaurant Name
        ctx.fillStyle = '#2D2D2D';
        ctx.font = 'bold 38px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(menu.restaurant_name, canvas.width / 2, 200);

        // Cuisine Type & Party Size
        ctx.font = '22px sans-serif';
        ctx.fillStyle = '#666';
        ctx.fillText(`${menu.cuisine_type} • ${menu.party_size} 人用餐 • ${menu.dishes.length} 道菜`, canvas.width / 2, 235);

        // Price Summary
        ctx.fillStyle = '#D4A574';
        ctx.fillRect(50, 280, canvas.width - 100, 120);
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 28px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(`總價: ${menu.currency || 'NT$'} ${menu.total_price.toLocaleString()}`, 80, 325);
        ctx.fillText(`人均: ${menu.currency || 'NT$'} ${Math.round(menu.total_price / menu.party_size).toLocaleString()}`, 80, 365);

        // Dishes
        let y = 450;
        ctx.fillStyle = '#2D2D2D';
        ctx.font = 'bold 26px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('推薦菜色', 50, y);
        y += 50;

        menu.dishes.forEach((dish, index) => {
            ctx.font = '22px sans-serif';
            ctx.fillStyle = '#2D2D2D';
            ctx.textAlign = 'left';

            // Truncate dish name if too long
            const maxWidth = 550;
            let dishName = dish.quantity > 1 ? `${dish.dish_name} ×${dish.quantity}` : dish.dish_name;
            const metrics = ctx.measureText(`${index + 1}. ${dishName}`);

            if (metrics.width > maxWidth) {
                while (ctx.measureText(`${index + 1}. ${dishName}...`).width > maxWidth && dishName.length > 10) {
                    dishName = dishName.slice(0, -1);
                }
                dishName += '...';
            }

            ctx.fillText(`${index + 1}. ${dishName}`, 50, y);

            // Price on the right
            ctx.textAlign = 'right';
            ctx.font = 'bold 22px sans-serif';
            ctx.fillText(`${menu.currency || 'NT$'} ${(dish.price * dish.quantity).toLocaleString()}`, canvas.width - 50, y);

            y += 65;
        });

        // Footer
        ctx.font = '20px sans-serif';
        ctx.fillStyle = '#999';
        ctx.textAlign = 'center';
        ctx.fillText('由 Carte AI 智慧推薦 • 祝您用餐愉快', canvas.width / 2, y + 40);
        ctx.font = 'bold 18px sans-serif';
        ctx.fillStyle = '#D4A574';
        ctx.fillText('立即體驗 → carte.ai', canvas.width / 2, y + 75);

        // Return a Promise that resolves with a Blob
        return new Promise<Blob | null>((resolve) => {
            canvas.toBlob((blob) => {
                resolve(blob);
            }, 'image/png');
        });
    };

    const handleShare = async () => {
        const imageBlob = await generateShareImage();
        const shareText = `🍽️ Carte AI 智慧推薦菜單\n\n我用 AI 點餐助手在「${menu?.restaurant_name}」找到了完美組合！\n\n💰 總價：${menu?.currency || 'NT$'} ${menu?.total_price.toLocaleString()}\n👥 ${menu?.party_size} 人份 · ${menu?.dishes.length} 道菜\n\n✨ 30 秒解決選擇困難，每一道都是精選！\n立即體驗 → carte.ai`;

        if (imageBlob && navigator.share) {
            try {
                const shareData: ShareData = {
                    files: [new File([imageBlob], 'carte_menu.png', { type: 'image/png' })],
                    title: 'Carte AI 智慧推薦菜單',
                    text: shareText,
                };
                if (navigator.canShare && navigator.canShare(shareData)) {
                    await navigator.share(shareData);
                } else {
                    alert('您的瀏覽器不支援直接分享圖片，將提供下載選項。');
                    // Fallback to existing download/copy if native share is not fully supported for images
                    setShareImageUrl(URL.createObjectURL(imageBlob));
                    setShowShareMenu(true);
                }
            } catch (error) {
                console.error('Error sharing:', error);
                // Fallback to existing download/copy if share fails
                alert('分享失敗，將提供下載選項。');
                setShareImageUrl(URL.createObjectURL(imageBlob));
                setShowShareMenu(true);
            }
        } else if (imageBlob) {
            // Fallback for browsers not supporting navigator.share
            alert('您的瀏覽器不支援直接分享，請下載圖片後手動分享。');
            setShareImageUrl(URL.createObjectURL(imageBlob));
            setShowShareMenu(true);
        }
    };

    const handleDownloadImage = () => {
        if (!shareImageUrl || !menu) return;

        const link = document.createElement('a');
        link.download = `${menu?.restaurant_name || 'menu'}_carte.png`;
        link.href = shareImageUrl;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        // Revoke the object URL after download
        URL.revokeObjectURL(shareImageUrl);
        setShareImageUrl(null);
    };

    const handleCopyImage = async () => {
        if (!shareImageUrl) return;

        try {
            const response = await fetch(shareImageUrl);
            const blob = await response.blob();
            // ClipboardItem is a standard API but may not be in all TS types
            await navigator.clipboard.write([
                new ClipboardItem({ 'image/png': blob })
            ]);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
            alert('圖片已複製到剪貼簿！');
        } catch (err) {
            console.error('Failed to copy image:', err);
            alert('複製失敗，請使用下載功能');
        }
    };

    const handleRatingSubmit = async (data: { rating: "up" | "down"; comment: string }) => {
        if (!menu || !session) return;

        try {
            // @ts-expect-error - id_token exists on session but not in type definition
            const token = session?.id_token;
            await submitFeedback({
                recommendation_id: menu.recommendation_id,
                rating: data.rating === "up" ? 5 : 1,
                selected_items: menu.dishes.map(d => d.dish_name),
                comment: data.comment
            }, token);
            setShowRatingModal(false);
            alert('感謝您的評分！');
        } catch (error) {
            console.error('Failed to submit feedback:', error);
            alert('評分提交失敗，請稍後再試。');
        }
    };

    const handleRating = () => {
        setShowRatingModal(true);
    };

    if (!menu) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <div className="text-center space-y-4">
                    <p className="text-muted-foreground">載入菜單中...</p>
                    <Button onClick={handleBack}>返回</Button>
                </div>
            </div>
        );
    }

    const perPerson = Math.round(menu.total_price / menu.party_size);

    return (
        <div className="min-h-screen bg-background pb-20">
            {/* Header - Hidden on print */}
            <div className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur print:hidden" role="banner">
                <div className="container flex h-14 items-center justify-between px-2 sm:px-4 gap-2">
                    <Button variant="ghost" onClick={() => router.push('/input')} className="gap-2" aria-label="返回上一頁修改菜單">
                        <ArrowLeft className="w-4 h-4" aria-hidden="true" />
                        返回修改
                    </Button>
                    <div className="flex gap-1 sm:gap-2" role="group" aria-label="菜單操作">
                        <Button variant="outline" onClick={() => router.push('/')} className="gap-1 sm:gap-2 px-2 sm:px-4" aria-label="搜尋新餐廳">
                            <Search className="w-4 h-4" aria-hidden="true" />
                            搜尋新餐廳
                        </Button>
                        <Button variant="outline" onClick={handlePrint} className="gap-1 sm:gap-2 px-2 sm:px-4" aria-label="列印菜單">
                            <Printer className="w-4 h-4" aria-hidden="true" />
                            列印
                        </Button>
                        <Button variant="outline" onClick={handleShare} className="gap-1 sm:gap-2 px-2 sm:px-4" aria-label="分享菜單">
                            <Share2 className="w-4 h-4" aria-hidden="true" />
                            分享
                        </Button>
                    </div>
                </div>
            </div>

            {/* Menu Content */}
            <div className="container max-w-4xl mx-auto px-4 py-8">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-8"
                >
                    <Badge variant="neutral" className="mb-4">
                        {menu.cuisine_type}
                    </Badge>
                    <h1 className="text-3xl sm:text-4xl font-bold text-foreground mb-2 font-display">
                        {menu.restaurant_name}
                    </h1>
                    <p className="text-muted-foreground mb-4">
                        {menu.party_size} 人用餐 • {menu.dishes.length} 道菜
                    </p>

                    <div className="flex justify-center">
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setShowLocalLanguage(!showLocalLanguage)}
                            className="gap-2"
                        >
                            {showLocalLanguage ? "顯示中文菜名" : "顯示原文菜名"}
                        </Button>
                    </div>
                </motion.div>

                {/* Price Summary */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <Card className="p-6 mb-8 bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
                        <div className="flex justify-between items-end">
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">菜單總價</p>
                                <h2 className="text-2xl sm:text-3xl font-bold text-foreground font-mono">
                                    {menu.currency || 'NT$'} {menu.total_price.toLocaleString()}
                                </h2>
                            </div>
                            <div className="text-right">
                                <p className="text-sm text-muted-foreground mb-1">人均約</p>
                                <p className="text-xl sm:text-2xl font-bold text-primary font-mono">
                                    {menu.currency || 'NT$'} {perPerson.toLocaleString()}
                                </p>
                            </div>
                        </div>
                    </Card>
                </motion.div>

                {/* Dishes List */}
                <div className="space-y-4">
                    <h3 className="text-xl font-semibold text-foreground mb-4">推薦菜色</h3>
                    <ul className="space-y-4" role="list" aria-label="最終菜單列表">
                        {menu.dishes.map((dish, index) => (
                            <motion.li
                                key={dish.dish_id || dish.dish_name}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.2 + index * 0.05 }}
                            >
                                <Card className="p-4 hover:shadow-md transition-shadow" role="article" aria-label={`菜品 ${index + 1}：${dish.dish_name}`}>
                                    <div className="flex justify-between items-start gap-4">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-2">
                                                <span className="text-lg font-semibold text-muted-foreground" aria-label={`第 ${index + 1} 道`}>
                                                    {index + 1}.
                                                </span>
                                                <h4 className="text-lg font-bold text-foreground">
                                                    {(showLocalLanguage && dish.dish_name_local) ? dish.dish_name_local : dish.dish_name} {dish.quantity > 1 && <span className="text-caramel">x{dish.quantity}</span>}
                                                </h4>
                                                {dish.category && (
                                                    <Badge variant="neutral" className="text-xs" aria-label={`類別：${dish.category}`}>
                                                        {dish.category}
                                                    </Badge>
                                                )}
                                            </div>
                                            <p className="text-sm text-muted-foreground leading-relaxed">
                                                {dish.reason}
                                            </p>
                                            {dish.review_count && (
                                                <p className="text-xs text-muted-foreground mt-2">
                                                    {dish.review_count} 則好評
                                                </p>
                                            )}
                                        </div>
                                        <div className="text-right flex-shrink-0">
                                            <p className="text-lg font-bold font-mono text-foreground" aria-label={`價格 ${dish.price * dish.quantity} 元`}>
                                                {menu.currency || 'NT$'} {(dish.price * dish.quantity).toLocaleString()}
                                            </p>
                                            {dish.quantity > 1 && (
                                                <p className="text-xs text-muted-foreground">
                                                    {dish.quantity} × {menu.currency || 'NT$'} {dish.price}
                                                </p>
                                            )}
                                            {dish.price_estimated && (
                                                <p className="text-xs text-muted-foreground">估價</p>
                                            )}
                                        </div>
                                    </div>
                                </Card>
                            </motion.li>
                        ))}
                    </ul>
                </div>

                {/* Rating Section */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="mt-12"
                >
                    <Card className="p-6 bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
                        <div className="text-center space-y-4">
                            <h3 className="text-lg font-semibold text-foreground">請為本次推薦菜色評分</h3>
                            <p className="text-sm text-muted-foreground">您的回饋能幫助我們提供更精準的推薦</p>
                            <Button onClick={handleRating} size="lg" className="gap-2">
                                <Star className="w-5 h-5" />
                                立即評分
                            </Button>
                        </div>
                    </Card>
                </motion.div>

                {/* Footer Note */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6 }}
                    className="mt-8 text-center space-y-4"
                >
                    <p className="text-sm text-muted-foreground">由 Carte AI 智慧推薦 • 祝您用餐愉快 🍽️</p>
                    <Button
                        variant="outline"
                        onClick={() => router.push('/')}
                        className="gap-2"
                    >
                        <Search className="w-4 h-4" />
                        搜尋新餐廳
                    </Button>
                </motion.div>
            </div>

            {/* Rating Modal */}
            <RatingModalDynamic
                isOpen={showRatingModal}
                onClose={() => setShowRatingModal(false)}
                onSubmit={handleRatingSubmit}
            />

            {/* Share Menu Dialog */}
            <Dialog open={showShareMenu} onOpenChange={setShowShareMenu}>
                <DialogContent className="sm:max-w-md">
                    <DialogHeader>
                        <DialogTitle>分享菜單</DialogTitle>
                        <DialogDescription>
                            您的瀏覽器不支援直接分享，您可以下載圖片或複製到剪貼簿。
                        </DialogDescription>
                    </DialogHeader>
                    <div className="flex flex-col items-center gap-4 py-4">
                        {shareImageUrl && (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img
                                src={shareImageUrl}
                                alt="Menu Preview"
                                className="w-full rounded-lg border shadow-sm max-h-[60vh] object-contain"
                            />
                        )}
                        <div className="flex gap-2 w-full">
                            <Button onClick={handleDownloadImage} className="flex-1 gap-2" variant="outline">
                                <Download className="w-4 h-4" /> 下載圖片
                            </Button>
                            <Button onClick={handleCopyImage} className="flex-1 gap-2" variant="outline">
                                {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                                {copied ? "已複製" : "複製圖片"}
                            </Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>

            {/* Hidden Canvas for generating share image */}
            <canvas ref={canvasRef} className="hidden" />
        </div>
    );
}

export default function MenuPage() {
    return (
        <Suspense fallback={<MenuPageSkeleton />}>
            <MenuPageContent />
        </Suspense>
    );
}
