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
  title: "AI Dining Agent",
  description: "Your personalized dining assistant",
};

import AuthProvider from "@/components/AuthProvider";
import { Header } from "@/components/header";
import { Toaster } from "@/components/ui/toaster";
import { NetworkStatus } from "@/components/network-status";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-Hant" className="light">
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
        </AuthProvider>
      </body>
    </html>
  );
}
