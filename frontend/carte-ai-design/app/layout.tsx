import type React from "react"
import type { Metadata, Viewport } from "next"
import { Inter, Cormorant_Garamond } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
})

const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-cormorant",
  display: "swap",
})

export const metadata: Metadata = {
  title: "Carte AI - 智慧點餐助手",
  description: "AI 驅動的餐廳點餐推薦，解決「看不懂菜單」、「選擇困難」的用餐痛點",
  generator: "Carte AI",
  keywords: ["餐廳推薦", "AI點餐", "菜單推薦", "智慧點餐"],
  authors: [{ name: "Carte AI Team" }],
  icons: {
    icon: [
      { url: "/icon-light-32x32.png", media: "(prefers-color-scheme: light)" },
      { url: "/icon-dark-32x32.png", media: "(prefers-color-scheme: dark)" },
      { url: "/icon.svg", type: "image/svg+xml" },
    ],
    apple: "/apple-icon.png",
  },
}

export const viewport: Viewport = {
  themeColor: "#F9F6F0",
  width: "device-width",
  initialScale: 1,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="zh-TW" className={`${inter.variable} ${cormorant.variable}`}>
      <body className="font-sans antialiased min-h-screen bg-cream">
        {children}
        <Analytics />
      </body>
    </html>
  )
}
