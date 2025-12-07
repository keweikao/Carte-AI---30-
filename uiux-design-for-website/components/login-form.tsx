"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"

export function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    // 處理登入邏輯
    setTimeout(() => setIsLoading(false), 1000)
  }

  return (
    <Card className="w-full max-w-md border-border bg-card/80 backdrop-blur-sm">
      <div className="p-8">
        {/* Form Header */}
        <div className="mb-8 space-y-2">
          <h2 className="text-2xl font-bold text-foreground">歡迎回來</h2>
          <p className="text-sm text-muted-foreground">登入你的 Carte 帳戶</p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Email Input */}
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium text-foreground">
              電子郵件
            </label>
            <Input
              id="email"
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
              className="border-border bg-background text-foreground placeholder:text-muted-foreground"
            />
          </div>

          {/* Password Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label htmlFor="password" className="text-sm font-medium text-foreground">
                密碼
              </label>
              <a href="#" className="text-xs text-primary hover:text-primary/80 transition-colors">
                忘記密碼？
              </a>
            </div>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              className="border-border bg-background text-foreground placeholder:text-muted-foreground"
            />
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={isLoading || !email || !password}
            className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
          >
            {isLoading ? "登入中..." : "登入"}
          </Button>
        </form>

        {/* Divider */}
        <div className="my-6 relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-border"></div>
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-card px-2 text-muted-foreground">或</span>
          </div>
        </div>

        {/* Social Login */}
        <div className="grid grid-cols-2 gap-3">
          <Button type="button" variant="outline" className="border-border hover:bg-secondary bg-transparent">
            Google
          </Button>
          <Button type="button" variant="outline" className="border-border hover:bg-secondary bg-transparent">
            GitHub
          </Button>
        </div>

        {/* Sign Up Link */}
        <div className="mt-8 text-center text-sm">
          <span className="text-muted-foreground">沒有帳戶？ </span>
          <a href="/signup" className="font-medium text-primary hover:text-primary/80 transition-colors">
            立即註冊
          </a>
        </div>
      </div>
    </Card>
  )
}
