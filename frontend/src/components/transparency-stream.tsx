import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Filter, ChefHat, Lightbulb } from 'lucide-react';
import { TRIVIA_QUESTIONS, TRIVIA_CATEGORIES } from '../data/trivia';

interface TransparencyStreamProps {
    progress: number;
    restaurantName?: string;
    partySize?: number;
    reviewCount?: number;
    dietary?: string;
}

export function TransparencyStream({
    progress,
    restaurantName = "餐廳",
    partySize = 2,
    reviewCount,
    dietary,
}: TransparencyStreamProps) {
    // 模擬進度 - 當後端 progress 在 0-10% 時，用前端模擬動畫
    const [simulatedProgress, setSimulatedProgress] = useState(0);

    // Trivia 狀態
    const [triviaIndex, setTriviaIndex] = useState(() => Math.floor(Math.random() * TRIVIA_QUESTIONS.length));
    const [showAnswer, setShowAnswer] = useState(false);

    // 模擬進度動畫
    useEffect(() => {
        if (progress <= 10) {
            const interval = setInterval(() => {
                setSimulatedProgress((prev: number) => {
                    if (prev >= 25) return prev; // 最高模擬到25%
                    return prev + 1;
                });
            }, 300);
            return () => clearInterval(interval);
        }
    }, [progress]);

    // Trivia 輪換邏輯 - 每 5 秒切換問題/答案
    useEffect(() => {
        const triviaInterval = setInterval(() => {
            setShowAnswer(prev => {
                if (!prev) {
                    // 顯示答案
                    return true;
                } else {
                    // 換下一題
                    setTriviaIndex(prevIndex => {
                        let nextIndex = Math.floor(Math.random() * TRIVIA_QUESTIONS.length);
                        while (nextIndex === prevIndex && TRIVIA_QUESTIONS.length > 1) {
                            nextIndex = Math.floor(Math.random() * TRIVIA_QUESTIONS.length);
                        }
                        return nextIndex;
                    });
                    return false;
                }
            });
        }, 5000);
        return () => clearInterval(triviaInterval);
    }, []);

    // 使用較高的值
    const displayProgress = Math.max(progress, simulatedProgress);

    // 根據進度決定階段
    const currentPhase: 'perception' | 'filtering' | 'decision' =
        displayProgress < 30 ? 'perception' :
            displayProgress < 70 ? 'filtering' : 'decision';

    // 階段配置 - 包含固定文字
    const phaseConfigs = {
        perception: {
            Icon: Search,
            label: '探索中',
            message: `正在掃描 ${restaurantName} 的菜單與評論...`,
            color: 'from-caramel to-caramel-600',
            bgColor: 'bg-cream-100',
            textColor: 'text-charcoal-800'
        },
        filtering: {
            Icon: Filter,
            label: '篩選中',
            message: `發現 ${partySize} 位用餐，正在計算最佳份量組合...`,
            color: 'from-terracotta to-terracotta-600',
            bgColor: 'bg-terracotta-50',
            textColor: 'text-charcoal-800'
        },
        decision: {
            Icon: ChefHat,
            label: '生成中',
            message: '正在為您量身打造專屬推薦菜單...',
            color: 'from-charcoal to-charcoal-700',
            bgColor: 'bg-charcoal-50',
            textColor: 'text-charcoal-800'
        }
    };

    const config = phaseConfigs[currentPhase];
    const PhaseIcon = config.Icon;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full mx-auto"
        >
            <div className="bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-cream-200">
                {/* Phase Icon with Pulse Animation */}
                <div className="flex justify-center mb-8">
                    <motion.div
                        key={currentPhase}
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{
                            scale: [1, 1.15, 1],
                            opacity: 1
                        }}
                        transition={{
                            scale: {
                                duration: 1.5,
                                repeat: Infinity,
                                repeatType: "reverse"
                            },
                            opacity: { duration: 0.3 }
                        }}
                        className={`w-20 h-20 rounded-full bg-gradient-to-br ${config.color} flex items-center justify-center shadow-lg`}
                    >
                        <PhaseIcon className="w-10 h-10 text-white" strokeWidth={2.5} />
                    </motion.div>
                </div>

                {/* Phase Label */}
                <div className="text-center mb-6">
                    <span className={`inline-block px-4 py-1.5 rounded-full text-sm font-semibold ${config.bgColor} ${config.textColor}`}>
                        {config.label}
                    </span>
                </div>

                {/* Static Message - 直接顯示固定文字 */}
                <motion.div
                    key={currentPhase}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className="text-center min-h-[60px] flex items-center justify-center px-4"
                >
                    <p className="text-lg sm:text-xl text-charcoal-800 leading-relaxed font-medium">
                        {config.message}
                    </p>
                </motion.div>

                {/* Progress Indicator */}
                <div className="mt-8 space-y-3">
                    <div className="flex justify-between text-sm font-semibold">
                        <span className="text-charcoal-600">{Math.round(displayProgress)}%</span>
                        <span className={config.textColor}>{config.label}</span>
                    </div>
                    <div className="h-3 bg-cream-200 rounded-full overflow-hidden shadow-inner">
                        <motion.div
                            className={`h-full bg-gradient-to-r ${config.color} shadow-lg`}
                            initial={{ width: 0 }}
                            animate={{ width: `${displayProgress}%` }}
                            transition={{ duration: 0.5, ease: "easeOut" }}
                        />
                    </div>
                </div>

                {/* 溫馨提醒 */}
                {(!reviewCount || reviewCount === 0) && displayProgress < 50 && (
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 2 }}
                        className="text-xs text-muted-foreground mt-6 text-center italic"
                    >
                        💡 溫馨提醒：第一次搜尋這家餐廳，AI 需要一點時間細讀評論，請耐心等候...
                    </motion.p>
                )}

                {/* 餐廳小知識 Trivia Card */}
                {TRIVIA_QUESTIONS.length > 0 && TRIVIA_QUESTIONS[triviaIndex] && (
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={`${triviaIndex}-${showAnswer}`}
                            initial={{ y: 20, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            exit={{ y: -20, opacity: 0 }}
                            transition={{ duration: 0.4 }}
                            className="mt-6 bg-cream-50 p-4 rounded-xl border border-cream-200 relative overflow-hidden"
                        >
                            <div className="absolute top-0 left-0 w-1 h-full bg-terracotta" />
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <Lightbulb className="w-4 h-4 text-terracotta" />
                                    <span className="text-xs font-bold text-terracotta uppercase tracking-wider">
                                        {showAnswer ? "💡 答案揭曉" : "🤔 你知道嗎？"}
                                    </span>
                                </div>
                                <span className="text-[10px] px-2 py-0.5 rounded-full bg-cream-100 text-charcoal-600">
                                    {TRIVIA_CATEGORIES[TRIVIA_QUESTIONS[triviaIndex].category]?.zh || "小知識"}
                                </span>
                            </div>
                            <p className="text-charcoal text-sm leading-relaxed pl-1">
                                {showAnswer
                                    ? TRIVIA_QUESTIONS[triviaIndex].answer.zh
                                    : TRIVIA_QUESTIONS[triviaIndex].question.zh
                                }
                            </p>
                        </motion.div>
                    </AnimatePresence>
                )}
            </div>
        </motion.div>
    );
}
