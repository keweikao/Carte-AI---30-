"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { X, Copy, Check } from "lucide-react"

interface ReferralModalProps {
  isOpen: boolean
  onClose: () => void
  referralCode: string | null
}

export function ReferralModal({ isOpen, onClose, referralCode }: ReferralModalProps) {
  const [copied, setCopied] = useState(false)

  if (!isOpen || !referralCode) return null

  const referralUrl = `${typeof window !== "undefined" ? window.location.origin : ""}/join?ref=${referralCode}`

  const handleCopy = () => {
    navigator.clipboard.writeText(referralUrl)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-sm rounded-lg border border-border bg-card p-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-foreground">邀請朋友</h2>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground">
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="mb-6 space-y-4">
          <div className="text-center">
            <p className="text-sm text-muted-foreground">每邀請一位朋友</p>
            <p className="text-2xl font-bold text-primary">+1 搜尋次數</p>
            <p className="mt-2 text-xs text-muted-foreground">你們都能獲得！</p>
          </div>

          <div className="space-y-2">
            <p className="text-xs font-medium text-foreground">邀請連結</p>
            <div className="flex gap-2">
              <input
                type="text"
                value={referralUrl}
                readOnly
                className="flex-1 rounded-lg border border-border bg-secondary/50 px-3 py-2 text-xs text-foreground"
              />
              <Button size="sm" variant="outline" onClick={handleCopy} className="px-3 bg-transparent">
                {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2">
            <Button size="sm" variant="outline" className="text-xs bg-transparent">
              WhatsApp
            </Button>
            <Button size="sm" variant="outline" className="text-xs bg-transparent">
              Line
            </Button>
            <Button size="sm" variant="outline" className="text-xs bg-transparent">
              複製
            </Button>
          </div>
        </div>

        <Button className="w-full bg-primary text-primary-foreground hover:bg-primary/90" onClick={onClose}>
          完成
        </Button>
      </div>
    </div>
  )
}
