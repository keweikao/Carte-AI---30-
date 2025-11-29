import { motion } from 'framer-motion';

interface AgentCardProps {
    agentName: string;
    logs: string[];
    currentStep: number;
    totalSteps: number;
}

const AGENT_CONFIG: Record<string, { icon: string; title: string }> = {
    VisualAgent: { icon: '📷', title: '菜單掃描專家' },
    ReviewAgent: { icon: '👂', title: '評論分析專家' },
    SearchAgent: { icon: '🕵️', title: '食記偵探' },
    Orchestrator: { icon: '🧠', title: '決策大師' }
};

export function AgentCard({ agentName, logs, currentStep, totalSteps }: AgentCardProps) {
    const config = AGENT_CONFIG[agentName] || { icon: '🤖', title: 'AI 專家' };

    return (
        <motion.div
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
            className="w-full max-w-md"
        >
            <div className="bg-white rounded-2xl p-8 text-center shadow-xl border border-gray-100">
                {/* Icon */}
                <motion.div
                    className="text-7xl mb-4"
                    animate={{
                        scale: [1, 1.05, 1],
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                >
                    {config.icon}
                </motion.div>

                {/* 名稱 */}
                <h2 className="text-2xl font-bold mb-2 text-foreground">
                    {agentName}
                </h2>

                {/* 職稱 */}
                <p className="text-muted-foreground mb-6">
                    {config.title}
                </p>

                {/* 呼吸燈 */}
                <div className="flex justify-center mb-6">
                    <motion.div
                        className="w-3 h-3 bg-primary rounded-full"
                        animate={{
                            scale: [1, 1.5, 1],
                            opacity: [1, 0.5, 1],
                        }}
                        transition={{
                            duration: 2,
                            repeat: Infinity,
                            ease: "easeInOut"
                        }}
                    />
                </div>

                {/* Log 訊息 */}
                <div className="space-y-2 text-left">
                    {logs.slice(0, 3).map((log, index) => (
                        <motion.p
                            key={index}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="text-sm text-muted-foreground leading-relaxed"
                        >
                            {log}
                        </motion.p>
                    ))}
                </div>

                {/* 進度指示 */}
                <div className="mt-6 text-xs text-muted-foreground">
                    步驟 {currentStep} / {totalSteps}
                </div>
            </div>
        </motion.div>
    );
}
