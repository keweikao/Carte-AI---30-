import type { Metadata } from "next";
import { Cormorant_Garamond, Noto_Sans_TC, Caveat } from "next/font/google";
import "../../app/globals.css";

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
    default: "Carte AI: Dining Agent",
    template: "%s | Carte AI: Dining Agent"
  },
  description: "Carte AI 點餐助手 分析數千則 Google 評論，為您推薦最適合的菜色。精準避雷、預算控制、飲食客製化，30秒快速決定吃什麼！",
  keywords: ["AI點餐", "餐廳推薦", "美食推薦", "Google評論分析", "智慧點餐", "台灣美食"],
  authors: [{ name: "Carte AI Team" }],
  creator: "Carte AI 點餐助手",
  publisher: "Carte AI 點餐助手",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://www.carte.tw'),
  alternates: {
    canonical: '/',
  },
  icons: {
    icon: '/logo-icon.svg',
    shortcut: '/logo-icon.svg',
    apple: '/logo-icon.svg',
  },
  openGraph: {
    title: "Carte AI 點餐助手 - 智慧餐廳點餐助手",
    description: "30秒快速決定吃什麼！AI 分析 Google 評論，推薦最適合您的菜色",
    url: 'https://www.carte.tw',
    siteName: 'Carte AI 點餐助手',
    locale: 'zh_TW',
    type: 'website',
    images: [
      {
        url: '/website_preview.png',
        width: 1200,
        height: 630,
        alt: 'Carte AI - 智慧餐廳點餐助手',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: "Carte AI 點餐助手 - 智慧餐廳點餐助手",
    description: "30秒快速決定吃什麼！AI 分析 Google 評論，推薦最適合您的菜色",
    images: ['/website_preview.png'],
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

  manifest: '/manifest.json',
};

import AuthProvider from "@/components/AuthProvider";
import { Header } from "@/components/header";
import { Toaster } from "@/components/ui/toaster";
import { NetworkStatus } from "@/components/network-status";
import { Analytics } from "@/lib/analytics";
import Script from "next/script";
import { WebVitalsReporter } from "@/components/web-vitals-reporter";
import { PWAInstaller } from "@/components/pwa-installer";
import { PWAProvider } from "@/contexts/PWAContext";

import { InAppBrowserGuard } from "@/components/InAppBrowserGuard";

import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

// ... (keep existing imports)

export default async function LocaleLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  // Read directly from process.env to ensure we get the runtime value from Cloud Run
  const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID;

  // Providing all messages to the client
  // side is the easiest way to get started
  const messages = await getMessages();

  return (
    <html lang={locale} className="light">
      <head>
        <meta name="application-name" content="Carte AI 點餐助手" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Carte AI" />
        <meta name="mobile-web-app-capable" content="yes" />
        <link rel="apple-touch-icon" href="/icon-192x192.png" />
        <link rel="apple-touch-icon" sizes="192x192" href="/icon-192x192.png" />
        <link rel="apple-touch-icon" sizes="512x512" href="/icon-512x512.png" />
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
                    send_page_view: false,
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
        <NextIntlClientProvider messages={messages}>
          <PWAProvider>
            <InAppBrowserGuard />
            <AuthProvider>
              <Header />
              {children}
              <Toaster />
              <NetworkStatus />
              <PWAInstaller />
              <Analytics gaId={GA_MEASUREMENT_ID} />
              <WebVitalsReporter />
            </AuthProvider>
          </PWAProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
