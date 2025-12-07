"use client";

import { PageTransition } from "@/components/page-transition";

/**
 * Root Template Component
 *
 * This template wraps all pages and enables smooth page transitions.
 * In Next.js App Router, template.tsx re-renders on navigation,
 * making it perfect for page transition animations.
 *
 * The PageTransition component handles:
 * - Smooth slide animations between routes
 * - Direction-aware transitions (forward/backward)
 * - Accessibility support (prefers-reduced-motion)
 * - Design system compliant timing and easing
 */

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <PageTransition className="min-h-screen">
      {children}
    </PageTransition>
  );
}
