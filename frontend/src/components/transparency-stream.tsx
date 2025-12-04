import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Filter, ChefHat } from 'lucide-react';

interface TransparencyStreamProps {
    progress: number;
    restaurantName?: string;
    reviewCount?: number;
    partySize?: number;
    dietary?: string;
}

interface StreamMessage {
    text: string;
    phase: 'perception' | 'filtering' | 'decision';
}

export function TransparencyStream({
    progress,
    restaurantName = "餐廳",
    reviewCount = 0,
    partySize = 2,
    dietary = ""
}: TransparencyStreamProps) {
    const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
    const [displayText, setDisplayText] = useState('');
    const [isTyping, setIsTyping] = useState(false);

    // Generate messages based on progress and context
    const messages: StreamMessage[] = [
        // Phase 1: Perception (0-30%)
        {
            text: `正在掃描 **${restaurantName}** 的菜單...`,
            phase: 'perception'
        },
        {
            text: reviewCount > 0
                ? `提示：這家店有 **${reviewCount}** 則評論，我來幫你讀完。`
                : `提示：正在分析餐廳資訊...`,
            phase: 'perception'
        },
        // Phase 2: Filtering (30-70%)
        {
            text: `發現您有 **${partySize}** 位，正在計算份量...`,
            phase: 'filtering'
        },
        ...(dietary ? [{
            text: `偵測到 **${dietary}**，正在移除相關菜色...`,
            phase: 'filtering' as const
        }] : []),
        {
            text: `發現：網友強烈推薦這裡的招牌菜。`,
            phase: 'filtering'
        },
        // Phase 3: Decision (70-100%)
        {
            text: `正在平衡整桌菜的口味...`,
            phase: 'decision'
        },
        {
            text: `準備上菜！正在生成您的專屬菜單...`,
            phase: 'decision'
        }
    ];

    // Determine current phase based on progress
    const currentPhase: 'perception' | 'filtering' | 'decision' =
        progress < 30 ? 'perception' :
            progress < 70 ? 'filtering' : 'decision';

    // Get phase icon and styling
    const getPhaseConfig = () => {
        switch (currentPhase) {
            case 'perception':
                return {
                    Icon: Search,
                    label: '探索中',
                    color: 'from-caramel to-caramel-600',  // Warm caramel gradient
                    bgColor: 'bg-cream-50',
                    textColor: 'text-charcoal',
                    badgeBg: 'bg-caramel',
                    badgeText: 'text-white'
                };
            case 'filtering':
                return {
                    Icon: Filter,
                    label: '篩選中',
                    color: 'from-terracotta to-terracotta-600',  // Terracotta gradient
                    bgColor: 'bg-terracotta-50',
                    textColor: 'text-charcoal',
                    badgeBg: 'bg-terracotta',
                    badgeText: 'text-white'
                };
            case 'decision':
                return {
                    Icon: ChefHat,
                    label: '生成中',
                    color: 'from-charcoal to-charcoal-700',  // Deep charcoal gradient
                    bgColor: 'bg-charcoal-50',
                    textColor: 'text-charcoal',
                    badgeBg: 'bg-charcoal',
                    badgeText: 'text-white'
                };
        }
    };

    const phaseConfig = getPhaseConfig();
    const PhaseIcon = phaseConfig.Icon;

    // Get relevant messages for current phase
    const phaseMessages = messages.filter(m => m.phase === currentPhase);

    // Select message based on progress within phase
    const currentMessage = phaseMessages[currentMessageIndex % phaseMessages.length] || messages[0];

    // Typewriter effect
    useEffect(() => {
        if (!currentMessage) return;

        setIsTyping(true);
        setDisplayText('');

        const fullText = currentMessage.text;
        let charIndex = 0;

        const typeInterval = setInterval(() => {
            if (charIndex < fullText.length) {
                setDisplayText(fullText.substring(0, charIndex + 1));
                charIndex++;
            } else {
                setIsTyping(false);
                clearInterval(typeInterval);

                // Wait 2 seconds before switching to next message
                setTimeout(() => {
                    setCurrentMessageIndex(prev => prev + 1);
                }, 2000);
            }
        }, 30); // 30ms per character for smooth typing

        return () => clearInterval(typeInterval);
    }, [currentMessage, currentMessageIndex]);

    // Highlight keywords (text between **)
    const renderHighlightedText = (text: string) => {
        const parts = text.split(/(\*\*.*?\*\*)/g);
        return parts.map((part, index) => {
            if (part.startsWith('**') && part.endsWith('**')) {
                const content = part.slice(2, -2);
                return (
                    <span key={index} className="font-bold text-charcoal">
                        {content}
                    </span>
                );
            }
            return <span key={index}>{part}</span>;
        });
    };

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full mx-auto"
        >
            <div className="bg-white rounded-3xl shadow-2xl p-8 sm:p-10 border border-gray-100">
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
                        className={`w-20 h-20 rounded-full bg-gradient-to-br ${phaseConfig.color} flex items-center justify-center shadow-lg`}
                    >
                        <PhaseIcon className="w-10 h-10 text-white" strokeWidth={2.5} />
                    </motion.div>
                </div>

                {/* Phase Label */}
                <div className="text-center mb-6">
                    <span className={`inline-block px-4 py-1.5 rounded-full text-sm font-semibold ${phaseConfig.bgColor} ${phaseConfig.textColor}`}>
                        {phaseConfig.label}
                    </span>
                </div>

                {/* Dynamic Message Stream */}
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentMessage?.text}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        transition={{ duration: 0.3 }}
                        className="text-center min-h-[80px] flex items-center justify-center px-4"
                    >
                        <p className="text-lg sm:text-xl text-gray-700 leading-relaxed font-medium">
                            {renderHighlightedText(displayText)}
                            {isTyping && (
                                <motion.span
                                    animate={{ opacity: [0, 1, 0] }}
                                    transition={{ duration: 0.8, repeat: Infinity }}
                                    className="inline-block ml-1 text-gray-500"
                                >
                                    |
                                </motion.span>
                            )}
                        </p>
                    </motion.div>
                </AnimatePresence>

                {/* Progress Indicator */}
                <div className="mt-8 space-y-3">
                    <div className="flex justify-between text-sm font-semibold">
                        <span className="text-gray-600">{Math.round(progress)}%</span>
                        <span className={`capitalize ${phaseConfig.textColor}`}>{phaseConfig.label}</span>
                    </div>
                    <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden shadow-inner">
                        <motion.div
                            className={`h-full bg-gradient-to-r ${phaseConfig.color} shadow-lg`}
                            initial={{ width: 0 }}
                            animate={{ width: `${progress}%` }}
                            transition={{ duration: 0.3, ease: "easeOut" }}
                        />
                    </div>
                </div>
            </div>

            {/* Background Gradient Animation */}
            <motion.div
                className="absolute inset-0 -z-10 blur-3xl opacity-10 pointer-events-none"
                animate={{
                    background: [
                        'radial-gradient(circle at 20% 50%, rgb(59, 130, 246) 0%, transparent 50%)',
                        'radial-gradient(circle at 80% 50%, rgb(168, 85, 247) 0%, transparent 50%)',
                        'radial-gradient(circle at 50% 80%, rgb(249, 115, 22) 0%, transparent 50%)'
                    ]
                }}
                transition={{
                    duration: 8,
                    repeat: Infinity,
                    repeatType: "reverse"
                }}
            />
        </motion.div>
    );
}
