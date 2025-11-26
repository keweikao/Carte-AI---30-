"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AlertTriangle, RefreshCcw, Home, Bug } from "lucide-react";

/**
 * Global Error Page (500)
 * Catches unhandled errors in the application
 * Magazine-style design matching the application's aesthetic
 */
export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to console in development
    if (process.env.NODE_ENV === "development") {
      console.error("Global error:", error);
    }

    // Here you can also log to an error reporting service
    // logErrorToService(error);
  }, [error]);

  return (
    <div className="min-h-screen bg-cream-100 flex items-center justify-center px-4 py-12">
      <div className="max-w-4xl w-full">
        {/* Main Content Card */}
        <Card className="bg-cream-50 border-caramel-100 shadow-floating overflow-hidden">
          <div className="relative">
            {/* Decorative Background */}
            <div className="absolute inset-0 bg-gradient-to-br from-terracotta-50/30 to-caramel-50/50" />

            <div className="relative p-8 md:p-16">
              {/* Error Icon */}
              <div className="flex justify-center mb-8">
                <div className="relative">
                  <div className="absolute inset-0 bg-terracotta/20 blur-3xl rounded-full" />
                  <div className="relative bg-gradient-to-br from-terracotta-50 to-terracotta-100 rounded-full p-6 shadow-card">
                    <AlertTriangle className="w-16 h-16 text-terracotta" />
                  </div>
                </div>
              </div>

              {/* Error Message */}
              <div className="text-center mb-8">
                <h1 className="font-display text-4xl md:text-5xl text-charcoal font-semibold mb-4">
                  系統遇到問題
                </h1>
                <p className="text-lg md:text-xl text-charcoal/70 max-w-2xl mx-auto leading-relaxed">
                  很抱歉，系統發生了預期外的錯誤。我們的工程團隊會儘快修復這個問題。
                </p>
              </div>

              {/* Error Details in Development Mode */}
              {process.env.NODE_ENV === "development" && (
                <div className="mb-8 max-w-2xl mx-auto">
                  <Card className="bg-charcoal-900 border-charcoal-700 p-6">
                    <div className="flex items-start gap-3 mb-3">
                      <Bug className="w-5 h-5 text-terracotta-50 flex-shrink-0 mt-1" />
                      <div>
                        <h3 className="font-display text-lg font-semibold text-terracotta-50 mb-2">
                          開發模式錯誤詳情
                        </h3>
                        <p className="font-mono text-sm text-red-300 break-all">
                          {error.message}
                        </p>
                        {error.digest && (
                          <p className="font-mono text-xs text-charcoal-100 mt-2">
                            Error Digest: {error.digest}
                          </p>
                        )}
                      </div>
                    </div>
                  </Card>
                </div>
              )}

              {/* What Happened Section */}
              <div className="mb-8 max-w-2xl mx-auto">
                <h3 className="font-display text-2xl text-charcoal font-semibold text-center mb-6">
                  發生什麼事了？
                </h3>

                <div className="space-y-4">
                  <div className="bg-white/60 backdrop-blur-sm rounded-lg p-5 border border-caramel-100/50">
                    <h4 className="font-display text-lg font-semibold text-charcoal mb-2">
                      可能的原因
                    </h4>
                    <ul className="space-y-2 text-charcoal/70">
                      <li className="flex items-start gap-2">
                        <span className="text-terracotta mt-1">•</span>
                        <span>伺服器暫時無法處理您的請求</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-terracotta mt-1">•</span>
                        <span>某些服務目前正在維護中</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-terracotta mt-1">•</span>
                        <span>應用程式遇到了未預期的情況</span>
                      </li>
                    </ul>
                  </div>

                  <div className="bg-white/60 backdrop-blur-sm rounded-lg p-5 border border-caramel-100/50">
                    <h4 className="font-display text-lg font-semibold text-charcoal mb-2">
                      您可以嘗試
                    </h4>
                    <ul className="space-y-2 text-charcoal/70">
                      <li className="flex items-start gap-2">
                        <span className="text-sage-700 mt-1">✓</span>
                        <span>重新載入頁面</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-sage-700 mt-1">✓</span>
                        <span>清除瀏覽器快取後再試一次</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-sage-700 mt-1">✓</span>
                        <span>稍後再回來試試</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <Button
                  onClick={reset}
                  size="lg"
                  className="bg-terracotta hover:bg-terracotta-700 text-white px-8 py-6 text-base w-full sm:w-auto"
                >
                  <RefreshCcw className="w-5 h-5 mr-2" />
                  重新嘗試
                </Button>

                <Button
                  size="lg"
                  onClick={() => (window.location.href = "/")}
                  className="bg-white border border-caramel-700 text-caramel-900 hover:bg-caramel-50 px-8 py-6 text-base w-full sm:w-auto"
                >
                  <Home className="w-5 h-5 mr-2" />
                  返回首頁
                </Button>
              </div>

              {/* Support Section */}
              <div className="mt-12 pt-8 border-t border-charcoal/10">
                <div className="text-center">
                  <p className="text-sm text-charcoal/60 mb-4">
                    問題持續發生嗎？
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center items-center text-sm">
                    <a
                      href="mailto:support@carte.com"
                      className="text-terracotta hover:underline font-medium"
                    >
                      聯繫客服團隊
                    </a>
                    <span className="hidden sm:inline text-charcoal/30">|</span>
                    <a
                      href="/help"
                      className="text-terracotta hover:underline font-medium"
                    >
                      查看說明文件
                    </a>
                    <span className="hidden sm:inline text-charcoal/30">|</span>
                    <a
                      href="/status"
                      className="text-terracotta hover:underline font-medium"
                    >
                      系統狀態
                    </a>
                  </div>
                </div>
              </div>

              {/* Decorative Quote */}
              <div className="mt-8">
                <blockquote className="text-center">
                  <p className="font-handwriting text-xl text-caramel-900">
                    "即使是最好的系統，偶爾也需要休息一下"
                  </p>
                </blockquote>
              </div>
            </div>
          </div>
        </Card>

        {/* Technical Info for Support */}
        {error.digest && (
          <div className="mt-6 text-center">
            <p className="text-xs text-charcoal/40">
              錯誤代碼: {error.digest.substring(0, 8)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
