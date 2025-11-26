import type React from "react"
import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { AuthProvider } from "@/lib/auth-context"
import { ReferralProvider } from "@/lib/referral-context"

import { Noto_Sans_TC } from "next/font/google"

const geist = Geist({ subsets: ["latin"] })
const geistMono = Geist_Mono({ subsets: ["latin"] })
const notoSansTC = Noto_Sans_TC({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Carte - AI 用餐決策顧問",
  description: "智慧分析 Google 評論，精準推薦最適合的菜色組合",
  generator: "v0.app",
  icons: {
    icon: [
      {
        url: "/icon-light-32x32.png",
        media: "(prefers-color-scheme: light)",
      },
      {
        url: "/icon-dark-32x32.png",
        media: "(prefers-color-scheme: dark)",
      },
      {
        url: "/icon.svg",
        type: "image/svg+xml",
      },
    ],
    apple: "/apple-icon.png",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="zh-TW">
      <body className={`font-sans antialiased`}>
        <AuthProvider>
          <ReferralProvider>
            {children}
            <Analytics />
          </ReferralProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
