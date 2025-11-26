"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ThumbsUp, ThumbsDown, Check, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface RatingModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit?: (data: { rating: "up" | "down"; comment: string }) => void;
}

export function RatingModal({ isOpen, onClose, onSubmit }: RatingModalProps) {
  const router = useRouter();
  const [step, setStep] = useState<"rating" | "feedback" | "done">("rating");
  const [rating, setRating] = useState<"up" | "down" | null>(null);
  const [comment, setComment] = useState("");

  const handleRatingSelect = (selectedRating: "up" | "down") => {
    setRating(selectedRating);
    setStep("feedback");
  };

  const handleSubmit = () => {
    if (rating && onSubmit) {
      onSubmit({ rating, comment });
    }
    setStep("done");
  };

  const handleClose = () => {
    setStep("rating");
    setRating(null);
    setComment("");
    onClose();
  };

  const handleDone = () => {
    handleClose();
    // 導航回 input 頁面
    router.push("/input");
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4"
        onClick={handleClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.9, opacity: 0, y: 20 }}
          className="bg-background w-full max-w-sm rounded-3xl p-6 shadow-2xl"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Close Button */}
          <button
            onClick={handleClose}
            className="absolute top-4 right-4 text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-5 h-5" />
          </button>

          {/* Rating Step */}
          {step === "rating" && (
            <div className="text-center space-y-6">
              <h3 className="text-2xl font-bold text-foreground">推薦結果滿意嗎？</h3>
              <p className="text-muted-foreground">您的回饋能讓 AI 點餐更精準</p>

              <div className="flex justify-center gap-4">
                <Button
                  variant="outline"
                  className="flex-1 h-32 rounded-2xl flex flex-col gap-3 border-border hover:bg-secondary hover:border-primary hover:text-primary transition-all"
                  onClick={() => handleRatingSelect("down")}
                >
                  <ThumbsDown className="w-8 h-8" />
                  <span className="font-bold">沒幫助</span>
                </Button>
                <Button
                  variant="outline"
                  className="flex-1 h-32 rounded-2xl flex flex-col gap-3 border-border hover:bg-secondary hover:border-primary hover:text-primary transition-all"
                  onClick={() => handleRatingSelect("up")}
                >
                  <ThumbsUp className="w-8 h-8" />
                  <span className="font-bold">有幫助</span>
                </Button>
              </div>
            </div>
          )}

          {/* Feedback Step */}
          {step === "feedback" && (
            <div className="space-y-6">
              <div className="text-center">
                <h3 className="text-xl font-bold text-foreground">
                  建議增加什麼功能？(選填)
                </h3>
              </div>

              <div className="space-y-3">
                <Input
                  placeholder="例如：希望能有圖片..."
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  className="bg-secondary border-transparent h-12"
                />
              </div>

              <div className="flex flex-wrap gap-2 justify-center">
                {["更便宜", "更多圖片", "介面更快", "更多選擇"].map((tag) => (
                  <Badge
                    key={tag}
                    variant="neutral"
                    className="cursor-pointer border-border hover:bg-primary hover:text-primary-foreground hover:border-primary transition-all py-2 px-3"
                    onClick={() =>
                      setComment((prev) => (prev ? `${prev}, ${tag}` : tag))
                    }
                  >
                    {tag}
                  </Badge>
                ))}
              </div>

              <Button
                className="w-full py-6 text-lg bg-primary hover:bg-primary/90 text-primary-foreground rounded-xl"
                onClick={handleSubmit}
              >
                完成並送出
              </Button>
            </div>
          )}

          {/* Done Step */}
          {step === "done" && (
            <div className="text-center py-8 space-y-6">
              <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto text-primary">
                <Check className="w-8 h-8" />
              </div>
              <h3 className="text-2xl font-bold text-foreground">感謝您的回饋！</h3>
              <p className="text-muted-foreground">系統已記錄您的喜好。</p>

              <Button
                variant="primary"
                className="w-full py-6 text-base bg-primary"
                onClick={handleDone}
              >
                回到搜尋頁
              </Button>
            </div>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
