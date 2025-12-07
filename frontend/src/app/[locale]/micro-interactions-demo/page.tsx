"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { ArrowLeft, Sparkles, Heart, Star, Coffee, Zap } from "lucide-react";

/**
 * Micro-Interactions Demo Page
 *
 * Demonstrates all the optimized micro-interactions:
 * - Button hover ripple effects
 * - Input focus animations
 * - Card hover shadow transitions
 * - Haptic feedback (mobile)
 */

export default function MicroInteractionsDemoPage() {
  const [inputValue, setInputValue] = useState("");
  const [count, setCount] = useState(0);

  return (
    <div className="min-h-screen bg-gradient-to-b from-cream-50 to-cream-100 p-8">
      <div className="max-w-5xl mx-auto space-y-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-charcoal mb-2 font-display">
              微互動展示
            </h1>
            <p className="text-charcoal/60 font-body">
              體驗優化後的按鈕、輸入框和卡片互動效果
            </p>
          </div>
          <Link href="/">
            <Button variant="outline">
              <ArrowLeft className="w-4 h-4 mr-2" />
              返回首頁
            </Button>
          </Link>
        </div>

        {/* Button Demos */}
        <section>
          <h2 className="text-2xl font-bold text-charcoal mb-4 font-display flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-terracotta" />
            按鈕波紋效果
          </h2>
          <Card>
            <CardHeader>
              <CardTitle>互動式按鈕</CardTitle>
              <CardDescription>
                點擊按鈕查看波紋動畫、懸停縮放和輕觸回饋（手機端振動）
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-4">
                <Button variant="primary" onClick={() => setCount(count + 1)}>
                  <Heart className="w-4 h-4" />
                  主要按鈕 ({count})
                </Button>
                <Button variant="secondary">
                  <Star className="w-4 h-4" />
                  次要按鈕
                </Button>
                <Button variant="outline">
                  <Coffee className="w-4 h-4" />
                  外框按鈕
                </Button>
                <Button variant="ghost">
                  <Zap className="w-4 h-4" />
                  幽靈按鈕
                </Button>
              </div>
            </CardContent>
            <CardFooter>
              <div className="text-sm text-charcoal/60">
                <strong>提示：</strong> 在桌面端可看到懸停效果，在手機端可感受輕微振動回饋
              </div>
            </CardFooter>
          </Card>
        </section>

        {/* Input Demos */}
        <section>
          <h2 className="text-2xl font-bold text-charcoal mb-4 font-display flex items-center gap-2">
            <Zap className="w-6 h-6 text-sage" />
            輸入框聚焦動畫
          </h2>
          <Card>
            <CardHeader>
              <CardTitle>動態輸入框</CardTitle>
              <CardDescription>
                點擊輸入框查看聚焦時的縮放、上移和光暈效果
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-charcoal">
                  用戶名
                </label>
                <Input
                  type="text"
                  placeholder="請輸入用戶名..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-charcoal">
                  電子郵件
                </label>
                <Input
                  type="email"
                  placeholder="example@email.com"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-charcoal">
                  密碼
                </label>
                <Input
                  type="password"
                  placeholder="請輸入密碼..."
                />
              </div>
            </CardContent>
            <CardFooter>
              <div className="text-sm text-charcoal/60">
                <strong>提示：</strong> 聚焦時輸入框會輕微放大並上移，並出現柔和的光暈效果
              </div>
            </CardFooter>
          </Card>
        </section>

        {/* Card Demos */}
        <section>
          <h2 className="text-2xl font-bold text-charcoal mb-4 font-display flex items-center gap-2">
            <Star className="w-6 h-6 text-caramel" />
            卡片懸停效果
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Heart className="w-5 h-5 text-terracotta" />
                  特色卡片 1
                </CardTitle>
                <CardDescription>
                  懸停時會上浮並增強陰影
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-charcoal/70">
                  這張卡片展示了流暢的懸停動畫，包括位移、縮放和陰影變化。
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Coffee className="w-5 h-5 text-sage" />
                  特色卡片 2
                </CardTitle>
                <CardDescription>
                  使用彈簧物理效果
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-charcoal/70">
                  動畫採用彈簧配置，提供自然且富有彈性的互動感受。
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-caramel" />
                  特色卡片 3
                </CardTitle>
                <CardDescription>
                  支援無障礙設定
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-charcoal/70">
                  所有動畫都遵循 prefers-reduced-motion 設定。
                </p>
              </CardContent>
            </Card>

            <Card variant="selected">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Star className="w-5 h-5 text-terracotta" />
                  已選擇卡片
                </CardTitle>
                <CardDescription>
                  具有特殊邊框樣式
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-charcoal/70">
                  選中狀態的卡片會保持浮動陰影和特殊邊框顏色。
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="w-5 h-5 text-sage" />
                  效能優化
                </CardTitle>
                <CardDescription>
                  使用 GPU 加速
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-charcoal/70">
                  所有動畫都使用 transform 屬性，確保流暢的 60fps 渲染。
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Heart className="w-5 h-5 text-terracotta" />
                  設計系統
                </CardTitle>
                <CardDescription>
                  遵循動畫規範
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-charcoal/70">
                  時長、緩動曲線和彈簧配置都來自統一的設計系統。
                </p>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Technical Info */}
        <Card className="bg-charcoal text-cream-50">
          <CardHeader>
            <CardTitle className="text-cream-50">技術細節</CardTitle>
            <CardDescription className="text-cream-100/70">
              實作說明與性能指標
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold mb-2 text-caramel">按鈕效果</h3>
                <ul className="space-y-1 text-sm text-cream-100/80">
                  <li>✓ 點擊波紋動畫（500ms）</li>
                  <li>✓ 懸停縮放（1.02x，200ms）</li>
                  <li>✓ 按壓縮放（0.97x，100ms）</li>
                  <li>✓ 觸覺回饋（10ms 振動）</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-2 text-sage">輸入框效果</h3>
                <ul className="space-y-1 text-sm text-cream-100/80">
                  <li>✓ 聚焦縮放（1.01x）</li>
                  <li>✓ 上移動畫（-1px）</li>
                  <li>✓ 徑向漸層光暈</li>
                  <li>✓ 彈簧物理效果</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-2 text-terracotta">卡片效果</h3>
                <ul className="space-y-1 text-sm text-cream-100/80">
                  <li>✓ 懸停上浮（-4px）</li>
                  <li>✓ 輕微縮放（1.01x）</li>
                  <li>✓ 陰影過渡（200ms）</li>
                  <li>✓ 彈簧動畫曲線</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-2 text-cream-50">無障礙支援</h3>
                <ul className="space-y-1 text-sm text-cream-100/80">
                  <li>✓ prefers-reduced-motion 支援</li>
                  <li>✓ 降級至簡單淡入</li>
                  <li>✓ 無動畫時直接切換</li>
                  <li>✓ 保持功能完整性</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Accessibility Notice */}
        <Card className="border-2 border-sage bg-sage/5">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-sage" />
              無障礙優先
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-charcoal/80">
              所有動畫都遵循 <code className="px-2 py-1 bg-sage/10 rounded text-sage font-mono text-sm">prefers-reduced-motion</code> 系統設定。
              如果您啟用了減少動畫選項，所有動畫將自動簡化或停用，同時保持完整功能。
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
