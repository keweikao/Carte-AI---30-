"use client";

import { motion, AnimatePresence, Variants } from "framer-motion";
import { usePathname } from "next/navigation";
import { ReactNode, useEffect, useState } from "react";

/**
 * PageTransition Component
 *
 * Provides smooth page transitions between routes using Framer Motion.
 * Follows the design system animation specifications:
 * - Duration: 100ms-800ms
 * - Easing: cubic-bezier curves
 * - Respects prefers-reduced-motion for accessibility
 *
 * Page Flow:
 * - Home (/) → Input (/input) → Recommendation (/recommendation) → Menu (/menu)
 */

interface PageTransitionProps {
  children: ReactNode;
  className?: string;
}

// Check if user prefers reduced motion
const prefersReducedMotion = (): boolean => {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
};

// Animation variants following design system
const pageVariants: Variants = {
  initial: (direction: number) => ({
    opacity: 0,
    x: direction > 0 ? 20 : -20,
    scale: 0.98,
  }),
  animate: {
    opacity: 1,
    x: 0,
    scale: 1,
  },
  exit: (direction: number) => ({
    opacity: 0,
    x: direction > 0 ? -20 : 20,
    scale: 0.98,
  }),
};

// Reduced motion variants (simple fade only)
const reducedMotionVariants: Variants = {
  initial: {
    opacity: 0,
  },
  animate: {
    opacity: 1,
  },
  exit: {
    opacity: 0,
  },
};

// Design system timing
const pageTransition = {
  duration: 0.3, // 300ms - --duration-base
  ease: [0.4, 0, 0.2, 1] as [number, number, number, number], // --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
};

const reducedMotionTransition = {
  duration: 0.1, // 100ms - --duration-instant
  ease: "linear" as const,
};

// Route order for determining direction
const routeOrder: Record<string, number> = {
  "/": 0,
  "/input": 1,
  "/recommendation": 2,
  "/menu": 3,
};

// Get route base (without query params)
const getRouteBase = (pathname: string): string => {
  return pathname.split("?")[0];
};

export function PageTransition({ children, className = "" }: PageTransitionProps) {
  const pathname = usePathname();
  const [direction, setDirection] = useState(0);
  const [prevPath, setPrevPath] = useState<string | null>(null);
  const [reducedMotion, setReducedMotion] = useState(() => prefersReducedMotion());

  // Check for reduced motion preference
  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const handleChange = () => setReducedMotion(mediaQuery.matches);

    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  // Calculate direction based on route order
  useEffect(() => {
    if (prevPath) {
      const prevRoute = getRouteBase(prevPath);
      const currentRoute = getRouteBase(pathname);

      const prevOrder = routeOrder[prevRoute] ?? 0;
      const currentOrder = routeOrder[currentRoute] ?? 0;

      setDirection(currentOrder > prevOrder ? 1 : -1);
    }
    setPrevPath(pathname);
  }, [pathname, prevPath]);

  const variants = reducedMotion ? reducedMotionVariants : pageVariants;
  const transition = reducedMotion ? reducedMotionTransition : pageTransition;

  return (
    <AnimatePresence mode="wait" custom={direction} initial={false}>
      <motion.div
        key={pathname}
        custom={direction}
        variants={variants}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={transition}
        className={className}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

/**
 * SlideInUp Component
 *
 * Utility component for slide-in-up animations
 * Used for cards, modals, and sequential content
 */
interface SlideInUpProps {
  children: ReactNode;
  delay?: number;
  className?: string;
}

export function SlideInUp({ children, delay = 0, className = "" }: SlideInUpProps) {
  const reducedMotion = prefersReducedMotion();

  const variants: Variants = reducedMotion
    ? {
      hidden: { opacity: 0 },
      visible: { opacity: 1 },
    }
    : {
      hidden: { opacity: 0, y: 20 },
      visible: { opacity: 1, y: 0 },
    };

  const transition = reducedMotion
    ? { duration: 0.1 }
    : {
      duration: 0.3,
      delay,
      ease: [0, 0, 0.2, 1] as [number, number, number, number] // --ease-out
    };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={variants}
      transition={transition}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/**
 * FadeIn Component
 *
 * Simple fade-in animation for content
 */
interface FadeInProps {
  children: ReactNode;
  delay?: number;
  duration?: number;
  className?: string;
}

export function FadeIn({
  children,
  delay = 0,
  duration = 0.3,
  className = ""
}: FadeInProps) {
  const reducedMotion = prefersReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{
        duration: reducedMotion ? 0.1 : duration,
        delay: reducedMotion ? 0 : delay
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/**
 * ScaleIn Component
 *
 * Scale animation for emphasis
 * Used for buttons, badges, and interactive elements
 */
interface ScaleInProps {
  children: ReactNode;
  delay?: number;
  className?: string;
}

export function ScaleIn({ children, delay = 0, className = "" }: ScaleInProps) {
  const reducedMotion = prefersReducedMotion();

  const variants: Variants = reducedMotion
    ? {
      hidden: { opacity: 0 },
      visible: { opacity: 1 },
    }
    : {
      hidden: { opacity: 0, scale: 0.95 },
      visible: { opacity: 1, scale: 1 },
    };

  const transition = reducedMotion
    ? { duration: 0.1 }
    : {
      duration: 0.2,
      delay,
      ease: [0, 0, 0.2, 1] as [number, number, number, number]
    };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={variants}
      transition={transition}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/**
 * Stagger Container
 *
 * Container for staggered animations of children
 */
interface StaggerContainerProps {
  children: ReactNode;
  staggerDelay?: number;
  className?: string;
}

export function StaggerContainer({
  children,
  staggerDelay = 0.1,
  className = ""
}: StaggerContainerProps) {
  const reducedMotion = prefersReducedMotion();

  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: reducedMotion ? 0 : staggerDelay,
      },
    },
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/**
 * Stagger Item
 *
 * Individual item in a stagger container
 */
interface StaggerItemProps {
  children: ReactNode;
  className?: string;
}

export function StaggerItem({ children, className = "" }: StaggerItemProps) {
  const reducedMotion = prefersReducedMotion();

  const variants: Variants = reducedMotion
    ? {
      hidden: { opacity: 0 },
      visible: { opacity: 1 },
    }
    : {
      hidden: { opacity: 0, y: 10 },
      visible: { opacity: 1, y: 0 },
    };

  const transition = reducedMotion
    ? { duration: 0.1 }
    : { duration: 0.2, ease: [0, 0, 0.2, 1] as const };

  return (
    <motion.div
      variants={variants}
      transition={transition}
      className={className}
    >
      {children}
    </motion.div>
  );
}
