"use client"

import Link from "next/link"
import { Menu, X } from "lucide-react"
import { useState } from "react"

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-cream/80 backdrop-blur-md border-b border-charcoal/5">
      <nav className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <span className="font-serif text-2xl text-charcoal tracking-tight">Carte</span>
            <span className="text-xs font-medium text-caramel bg-caramel/10 px-2 py-0.5 rounded-full">AI</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <Link href="#features" className="text-sm text-charcoal/70 hover:text-charcoal transition-colors">
              功能介紹
            </Link>
            <Link href="#how-it-works" className="text-sm text-charcoal/70 hover:text-charcoal transition-colors">
              使用方式
            </Link>
            <Link
              href="/input"
              className="px-5 py-2 text-sm font-medium text-white bg-charcoal rounded-full hover:bg-charcoal/90 transition-all hover:scale-105"
            >
              開始使用
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 text-charcoal"
            aria-label={isMenuOpen ? "關閉選單" : "開啟選單"}
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-charcoal/10">
            <div className="flex flex-col gap-4">
              <Link
                href="#features"
                className="text-charcoal/70 hover:text-charcoal transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                功能介紹
              </Link>
              <Link
                href="#how-it-works"
                className="text-charcoal/70 hover:text-charcoal transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                使用方式
              </Link>
              <Link
                href="/input"
                className="w-full py-3 text-center font-medium text-white bg-charcoal rounded-full"
                onClick={() => setIsMenuOpen(false)}
              >
                開始使用
              </Link>
            </div>
          </div>
        )}
      </nav>
    </header>
  )
}
