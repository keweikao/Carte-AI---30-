import { useState, useEffect } from 'react';
import { TransparencyStream } from './transparency-stream';

interface AgentFocusLoaderProps<T = unknown> {
    jobId: string;
    onComplete: (result: T) => void;
    onError: (error: string) => void;
    // Context data for Transparency Stream
    restaurantName?: string;
    reviewCount?: number;
    partySize?: number;
    dietary?: string;
}

export function AgentFocusLoader<T = unknown>({
    jobId,
    onComplete,
    onError,
    restaurantName,
    reviewCount,
    partySize,
    dietary
}: AgentFocusLoaderProps<T>) {
    const [currentAgent, setCurrentAgent] = useState<string>('VisualAgent');
    const [currentStep, setCurrentStep] = useState<number>(1);
    const [totalSteps, setTotalSteps] = useState<number>(4);
    const [isFirstVisit, setIsFirstVisit] = useState<boolean>(false);
    const [progress, setProgress] = useState<number>(0);

    useEffect(() => {
        const pollInterval = setInterval(async () => {
            try {
                const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
                const response = await fetch(`${apiUrl}/v2/recommendations/status/${jobId}`);

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();

                // 更新狀態
                if (data.current_agent && data.current_agent !== currentAgent) {
                    setCurrentAgent(data.current_agent);
                }

                if (data.current_step) {
                    setCurrentStep(data.current_step);
                }

                if (data.total_steps) {
                    setTotalSteps(data.total_steps);
                }

                // Calculate progress percentage
                if (data.progress !== undefined) {
                    setProgress(data.progress);
                } else {
                    // Fallback: calculate based on steps
                    setProgress(Math.round((currentStep / totalSteps) * 100));
                }

                // 檢查是否為首次訪問 (Cache Miss)
                if (data.metadata && data.metadata.is_cache_hit === false) {
                    setIsFirstVisit(true);
                }

                // 檢查完成狀態
                if (data.status === 'completed') {
                    clearInterval(pollInterval);
                    onComplete(data.result);
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval);
                    onError(data.error || '推薦生成失敗');
                }
            } catch (error) {
                console.error('Polling error:', error);
                // 不要立即失敗，繼續嘗試
            }
        }, 1000); // 每秒 Polling

        return () => clearInterval(pollInterval);
    }, [jobId, currentAgent, currentStep, totalSteps, onComplete, onError]);

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-br from-cream-50 via-white to-cream-100 relative">
            {/* Cold Start Notification */}
            {isFirstVisit && (
                <div className="mb-8 text-center space-y-2 animate-in fade-in slide-in-from-bottom-4 duration-700 max-w-md">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-caramel/10 to-terracotta/10 rounded-full border border-caramel/20">
                        <span className="text-2xl">✨</span>
                        <p className="text-caramel-900 font-semibold">您是第一位探索這家餐廳的美食家！</p>
                    </div>
                    <p className="text-sm text-charcoal-600">AI 正在進行深度分析，請稍候片刻...</p>
                </div>
            )}

            {/* Transparency Stream - Main Content */}
            <div className="w-full max-w-lg">
                <TransparencyStream
                    progress={progress}
                    restaurantName={restaurantName}
                    reviewCount={reviewCount}
                    partySize={partySize}
                    dietary={dietary}
                />
            </div>
        </div>
    );
}
