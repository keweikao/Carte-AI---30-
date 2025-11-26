import type { Metadata } from "next";
import { Cormorant_Garamond, Noto_Sans_TC, Caveat } from "next/font/google";
import "./globals.css";

const display = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-display",
  display: "swap",
  preload: true,
});

const body = Noto_Sans_TC({
  subsets: ["latin"],
  weight: ["400", "500", "700", "900"],
  variable: "--font-body",
  display: "swap",
  preload: true,
});

const handwriting = Caveat({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-handwriting",
  display: "swap",
  preload: false,
});

export const metadata: Metadata = {
  title: {
    default: "Carte AI - 智慧餐廳點餐助手 | 30秒快速決定吃什麼",
    template: "%s | Carte AI"
  },
  description: "Carte AI 分析數千則 Google 評論，為您推薦最適合的菜色。精準避雷、預算控制、飲食客製化，30秒快速決定吃什麼！",
  keywords: ["AI點餐", "餐廳推薦", "美食推薦", "Google評論分析", "智慧點餐", "台灣美食"],
  authors: [{ name: "Carte AI Team" }],
  creator: "Carte AI",
  publisher: "Carte AI",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://dining-frontend-u33peegeaa-de.a.run.app'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: "Carte AI - 智慧餐廳點餐助手",
    description: "30秒快速決定吃什麼！AI 分析 Google 評論，推薦最適合您的菜色",
    url: 'https://dining-frontend-u33peegeaa-de.a.run.app',
    siteName: 'Carte AI',
    locale: 'zh_TW',
    type: 'website',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Carte AI - 智慧餐廳點餐助手',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: "Carte AI - 智慧餐廳點餐助手",
    description: "30秒快速決定吃什麼！AI 分析 Google 評論，推薦最適合您的菜色",
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/manifest.json',
};

import AuthProvider from "@/components/AuthProvider";
import { Header } from "@/components/header";
import { Toaster } from "@/components/ui/toaster";
import { NetworkStatus } from "@/components/network-status";
import { Analytics, GA_MEASUREMENT_ID } from "@/lib/analytics";
import Script from "next/script";
import { WebVitalsReporter } from "@/components/web-vitals-reporter";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-Hant" className="light">
      <head>
        {GA_MEASUREMENT_ID && (
          <>
            <Script
              strategy="afterInteractive"
              src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}
            />
            <Script
              id="google-analytics"
              strategy="afterInteractive"
              dangerouslySetInnerHTML={{
                __html: `
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());
                  gtag('config', '${GA_MEASUREMENT_ID}', {
                    page_path: window.location.pathname,
                  });
                `,
              }}
            />
          </>
        )}
      </head>
      <body
        className={[
          display.variable,
          body.variable,
          handwriting.variable,
          "font-body",
          "antialiased",
          "bg-cream-100",
          "text-charcoal",
        ].join(" ")}
      >
        <AuthProvider>
          <Header />
          {children}
          <Toaster />
          <NetworkStatus />
          <Analytics />
          <WebVitalsReporter />
        </AuthProvider>
      </body>
    </html>
  );
}
