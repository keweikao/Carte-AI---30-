'use client';

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Search, Home, ArrowLeft } from "lucide-react";

/**
 * 404 Not Found Page
 * Magazine-style design matching the application's aesthetic
 */
export default function NotFound() {
  return (
    <div className="min-h-screen bg-cream-100 flex items-center justify-center px-4 py-12">
      <div className="max-w-4xl w-full">
        {/* Main Content Card */}
        <Card className="bg-cream-50 border-caramel-100 shadow-floating overflow-hidden">
          <div className="relative">
            {/* Decorative Background */}
            <div className="absolute inset-0 bg-gradient-to-br from-caramel-50/50 to-terracotta-50/30" />

            <div className="relative p-8 md:p-16">
              {/* 404 Typography */}
              <div className="text-center mb-8">
                <h1 className="font-display text-[120px] md:text-[180px] leading-none text-caramel-700/20 font-bold select-none">
                  404
                </h1>
                <div className="-mt-16 md:-mt-24">
                  <h2 className="font-display text-4xl md:text-5xl text-charcoal font-semibold mb-4">
                    找不到這個頁面
                  </h2>
                  <p className="text-lg md:text-xl text-charcoal/70 max-w-2xl mx-auto leading-relaxed">
                    抱歉，您要找的頁面似乎不存在。可能是連結錯誤，或者這個頁面已經被移除了。
                  </p>
                </div>
              </div>

              {/* Suggestions Section */}
              <div className="mt-12 mb-8">
                <h3 className="font-display text-2xl text-charcoal font-semibold text-center mb-6">
                  您可以試試...
                </h3>

                <div className="grid md:grid-cols-3 gap-4 max-w-3xl mx-auto">
                  {/* Suggestion Cards */}
                  <div className="bg-white/60 backdrop-blur-sm rounded-lg p-5 border border-caramel-100/50">
                    <div className="bg-sage-50 rounded-full w-12 h-12 flex items-center justify-center mb-3">
                      <Home className="w-6 h-6 text-sage-700" />
                    </div>
                    <h4 className="font-display text-lg font-semibold text-charcoal mb-2">
                      返回首頁
                    </h4>
                    <p className="text-sm text-charcoal/60">
                      回到主頁面，重新開始您的美食探索
                    </p>
                  </div>

                  <div className="bg-white/60 backdrop-blur-sm rounded-lg p-5 border border-caramel-100/50">
                    <div className="bg-terracotta-50 rounded-full w-12 h-12 flex items-center justify-center mb-3">
                      <Search className="w-6 h-6 text-terracotta-700" />
                    </div>
                    <h4 className="font-display text-lg font-semibold text-charcoal mb-2">
                      搜尋餐廳
                    </h4>
                    <p className="text-sm text-charcoal/60">
                      使用搜尋功能尋找您想要的餐廳
                    </p>
                  </div>

                  <div className="bg-white/60 backdrop-blur-sm rounded-lg p-5 border border-caramel-100/50">
                    <div className="bg-caramel-50 rounded-full w-12 h-12 flex items-center justify-center mb-3">
                      <ArrowLeft className="w-6 h-6 text-caramel-700" />
                    </div>
                    <h4 className="font-display text-lg font-semibold text-charcoal mb-2">
                      返回上一頁
                    </h4>
                    <p className="text-sm text-charcoal/60">
                      回到您剛才瀏覽的頁面
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-12">
                <Link href="/" prefetch={true}>
                  <Button
                    size="lg"
                    className="bg-terracotta hover:bg-terracotta-700 text-white px-8 py-6 text-base w-full sm:w-auto"
                  >
                    <Home className="w-5 h-5 mr-2" />
                    返回首頁
                  </Button>
                </Link>

                <Button
                  size="lg"
                  variant="outline"
                  onClick={() => window.history.back()}
                  className="border-caramel-700 text-caramel-900 hover:bg-caramel-50 px-8 py-6 text-base w-full sm:w-auto"
                >
                  <ArrowLeft className="w-5 h-5 mr-2" />
                  返回上一頁
                </Button>
              </div>

              {/* Decorative Quote */}
              <div className="mt-12 pt-8 border-t border-charcoal/10">
                <blockquote className="text-center">
                  <p className="font-handwriting text-2xl text-caramel-900 mb-2">
                    "迷路也是一種探索"
                  </p>
                  <p className="text-sm text-charcoal/50">
                    但我們還是希望幫您找到正確的路
                  </p>
                </blockquote>
              </div>
            </div>
          </div>
        </Card>

        {/* Help Text */}
        <div className="mt-6 text-center">
          <p className="text-sm text-charcoal/60">
            如果您認為這是系統錯誤，請{" "}
            <a
              href="mailto:support@carte.com"
              className="text-terracotta hover:underline font-medium"
            >
              聯繫我們的支援團隊
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
