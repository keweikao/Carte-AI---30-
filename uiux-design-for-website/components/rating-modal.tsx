"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { X } from "lucide-react"

interface RatingModalProps {
  isOpen: boolean
  onClose: () => void
  sessionId: string
}

export function RatingModal({ isOpen, onClose, sessionId }: RatingModalProps) {
  const [rating, setRating] = useState(0)
  const [feedback, setFeedback] = useState("")
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async () => {
    if (rating === 0) return

    setLoading(true)
    try {
      await fetch("/api/ratings/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          rating,
          feedback: feedback || null,
        }),
      })
      setSubmitted(true)
      setTimeout(onClose, 2000)
    } catch (error) {
      console.error("Failed to submit rating:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-sm rounded-lg border border-border bg-card p-8 shadow-lg">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-foreground">評分這個推薦</h2>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors">
            <X className="h-5 w-5" />
          </button>
        </div>

        {!submitted ? (
          <>
            <p className="mb-6 text-center text-muted-foreground">這個推薦有幫助嗎？</p>

            {/* Star Rating */}
            <div className="mb-6 flex justify-center gap-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setRating(star)}
                  className="text-4xl transition-transform hover:scale-110 focus:outline-none"
                >
                  {star <= rating ? "⭐" : "☆"}
                </button>
              ))}
            </div>

            {rating > 0 && (
              <div className="mb-6">
                <textarea
                  placeholder="有其他想說的嗎？(選填)"
                  value={feedback}
                  onChange={(e) => setFeedback(e.target.value)}
                  className="w-full rounded-lg border border-border bg-input p-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  rows={3}
                />
              </div>
            )}

            <div className="flex gap-3">
              <Button
                variant="outline"
                className="flex-1 border-border text-foreground hover:bg-secondary bg-transparent"
                onClick={onClose}
              >
                稍後再說
              </Button>
              <Button
                className="flex-1 bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
                onClick={handleSubmit}
                disabled={rating === 0 || loading}
              >
                {loading ? "提交中..." : "提交評分"}
              </Button>
            </div>
          </>
        ) : (
          <div className="text-center py-4">
            <p className="mb-2 text-lg font-semibold text-primary">✓ 感謝你的反饋！</p>
            <p className="text-sm text-muted-foreground">這幫助我們改進推薦品質</p>
          </div>
        )}
      </div>
    </div>
  )
}
