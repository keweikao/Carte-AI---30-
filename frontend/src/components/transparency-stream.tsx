import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, ChefHat } from 'lucide-react';

interface TransparencyStreamProps {
    progress: number;
    restaurantName?: string;
    partySize?: number;
}

export function TransparencyStream({
    progress,
    restaurantName = "餐廳",
    partySize = 2,
}: TransparencyStreamProps) {
    // 模擬進度 - 當後端 progress 在 0-10% 時，用前端模擬動畫
    const [simulatedProgress, setSimulatedProgress] = useState(0);

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
            </div>
        </motion.div>
    );
}
