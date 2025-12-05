"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";
import { cn } from "@/lib/utils";

interface HeaderProps {
    className?: string;
}

export function CarteHeader({ className }: HeaderProps) {
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const pathname = usePathname();

    // Scroll effect
    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50);
        };

        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    // Close mobile menu on route change
    useEffect(() => {
        setIsMobileMenuOpen(false);
    }, [pathname]);

    const navLinks = [
        { href: "#features", label: "功能介紹" },
        { href: "#how-it-works", label: "使用方式" },
        { href: "#about", label: "關於我們" },
    ];

    return (
        <header
            className={cn(
                "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
                isScrolled
                    ? "bg-white/80 backdrop-blur-md shadow-subtle"
                    : "bg-transparent",
                className
            )}
        >
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16 md:h-20">
                    {/* Logo */}
                    <Link
                        href="/"
                        className="flex items-center gap-2 group"
                    >
                        <span className="font-serif text-2xl md:text-3xl font-bold text-charcoal group-hover:text-caramel transition-colors">
                            Carte
                        </span>
                        <span className="text-sm font-medium text-caramel">AI</span>
                    </Link>

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex items-center gap-8">
                        {navLinks.map((link) => (
                            <a
                                key={link.href}
                                href={link.href}
                                className="text-sm font-medium text-charcoal hover:text-caramel transition-colors"
                            >
                                {link.label}
                            </a>
                        ))}
                    </nav>

                    {/* CTA Button */}
                    <div className="hidden md:block">
                        <Link
                            href="/zh/input"
                            className="inline-flex items-center justify-center px-6 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-caramel to-terracotta rounded-full hover:opacity-90 hover:shadow-medium transition-all"
                        >
                            開始探索
                        </Link>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        className="md:hidden p-2 text-charcoal hover:text-caramel transition-colors"
                        aria-label="Toggle menu"
                    >
                        {isMobileMenuOpen ? (
                            <X className="w-6 h-6" />
                        ) : (
                            <Menu className="w-6 h-6" />
                        )}
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMobileMenuOpen && (
                <div className="md:hidden bg-white border-t border-gray-200 shadow-medium">
                    <nav className="container mx-auto px-4 py-4 flex flex-col gap-4">
                        {navLinks.map((link) => (
                            <a
                                key={link.href}
                                href={link.href}
                                className="text-base font-medium text-charcoal hover:text-caramel transition-colors py-2"
                            >
                                {link.label}
                            </a>
                        ))}
                        <Link
                            href="/zh/input"
                            className="inline-flex items-center justify-center px-6 py-3 text-base font-medium text-white bg-gradient-to-r from-caramel to-terracotta rounded-full hover:opacity-90 transition-all mt-2"
                        >
                            開始探索
                        </Link>
                    </nav>
                </div>
            )}
        </header>
    );
}
