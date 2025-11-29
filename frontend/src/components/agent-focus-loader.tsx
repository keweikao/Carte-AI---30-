import { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { AgentCard } from './agent-card';
import { TriviaCard } from './trivia-card';

interface AgentFocusLoaderProps<T = unknown> {
    jobId: string;
    onComplete: (result: T) => void;
    onError: (error: string) => void;
}

export function AgentFocusLoader<T = unknown>({ jobId, onComplete, onError }: AgentFocusLoaderProps<T>) {
    const [currentAgent, setCurrentAgent] = useState<string>('VisualAgent');
    const [logs, setLogs] = useState<string[]>([]);
    const [currentStep, setCurrentStep] = useState<number>(1);
    const [totalSteps, setTotalSteps] = useState<number>(4);
    const [isFirstVisit, setIsFirstVisit] = useState<boolean>(false);

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

                if (data.logs) {
                    setLogs(data.logs);
                }

                if (data.current_step) {
                    setCurrentStep(data.current_step);
                }

                if (data.total_steps) {
                    setTotalSteps(data.total_steps);
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
    }, [jobId, currentAgent, onComplete, onError]);

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-background">
            {/* Agent 卡片 */}
            <AnimatePresence mode="wait">
                <AgentCard
                    key={currentAgent}
                    agentName={currentAgent}
                    logs={logs}
                    currentStep={currentStep}
                    totalSteps={totalSteps}
                />
            </AnimatePresence>

            {/* 溫馨提示 */}
            {isFirstVisit && (
                <div className="mt-6 text-center space-y-1 animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <p className="text-primary font-medium">✨ 您是第一位探索這家餐廳的美食家！</p>
                    <p className="text-sm text-muted-foreground">AI 正在進行深度分析，請稍候片刻...</p>
                </div>
            )}

            {/* 小知識卡片 */}
            <div className="mt-8 w-full max-w-md">
                <TriviaCard />
            </div>
        </div>
    );
}
