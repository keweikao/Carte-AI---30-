import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { TRIVIA_QUESTIONS } from '../data/trivia';

export function TriviaCard() {
    const params = useParams();
    const locale = params.locale as string;
    const lang: 'zh' | 'en' = locale?.startsWith('en') ? 'en' : 'zh';

    const [currentIndex, setCurrentIndex] = useState(() =>
        Math.floor(Math.random() * TRIVIA_QUESTIONS.length)
    );

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentIndex(prev => {
                let nextIndex = Math.floor(Math.random() * TRIVIA_QUESTIONS.length);
                while (nextIndex === prev && TRIVIA_QUESTIONS.length > 1) {
                    nextIndex = Math.floor(Math.random() * TRIVIA_QUESTIONS.length);
                }
                return nextIndex;
            });
        }, 5000); // 每 5 秒切換

        return () => clearInterval(interval);
    }, []);

    const currentTrivia = TRIVIA_QUESTIONS[currentIndex];

    return (
        <AnimatePresence mode="wait">
            <motion.div
                key={currentIndex}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
                className="bg-primary/5 rounded-xl p-6 border border-primary/20"
            >
                <div className="flex items-start gap-3">
                    <span className="text-2xl flex-shrink-0">💡</span>
                    <div className="flex-1">
                        <h3 className="font-semibold mb-2 text-foreground">
                            {lang === 'en' ? 'Did you know?' : '您知道嗎？'}
                        </h3>
                        <p className="text-sm text-muted-foreground leading-relaxed mb-3">
                            {currentTrivia.question[lang]}
                        </p>
                        <p className="text-sm text-foreground leading-relaxed">
                            {currentTrivia.answer[lang]}
                        </p>
                    </div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
}
