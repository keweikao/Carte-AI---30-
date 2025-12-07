/**
 * Animation Utilities
 *
 * Reusable animation configurations and helpers
 * following the design system specifications.
 */

import { Variants, Transition } from "framer-motion";

// Design System Duration Values (in seconds)
export const DURATION = {
  instant: 0.1, // --duration-instant: 100ms
  fast: 0.2, // --duration-fast: 200ms
  base: 0.3, // --duration-base: 300ms
  slow: 0.5, // --duration-slow: 500ms
  slower: 0.8, // --duration-slower: 800ms
} as const;

// Design System Easing Curves
export const EASING = {
  in: [0.4, 0, 1, 1] as [number, number, number, number], // --ease-in
  out: [0, 0, 0.2, 1] as [number, number, number, number], // --ease-out
  inOut: [0.4, 0, 0.2, 1] as [number, number, number, number], // --ease-in-out
  spring: [0.34, 1.56, 0.64, 1] as [number, number, number, number], // --ease-spring (bounce)
  smooth: [0.65, 0, 0.35, 1] as [number, number, number, number], // --ease-smooth
} as const;

// Common animation variants
export const fadeInVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
};

export const slideInUpVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export const slideInDownVariants: Variants = {
  hidden: { opacity: 0, y: -20 },
  visible: { opacity: 1, y: 0 },
};

export const slideInLeftVariants: Variants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0 },
};

export const slideInRightVariants: Variants = {
  hidden: { opacity: 0, x: 20 },
  visible: { opacity: 1, x: 0 },
};

export const scaleInVariants: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1 },
};

export const scaleInCenterVariants: Variants = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { opacity: 1, scale: 1 },
};

// Card swap animation (used in recommendation page)
export const cardSwapVariants: Variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 100 : -100,
    opacity: 0,
    rotate: direction > 0 ? 15 : -15,
  }),
  center: {
    x: 0,
    opacity: 1,
    rotate: 0,
  },
  exit: (direction: number) => ({
    x: direction > 0 ? -100 : 100,
    opacity: 0,
    rotate: direction > 0 ? -15 : 15,
  }),
};

// Price pulse animation
export const pricePulseVariants: Variants = {
  pulse: {
    scale: [1, 1.05, 1],
    transition: {
      duration: DURATION.base,
      ease: EASING.inOut,
    },
  },
};

// Celebration animation (for completed actions)
export const celebrateVariants: Variants = {
  celebrate: {
    scale: [1, 1.1, 1],
    rotate: [0, -5, 5, 0],
    transition: {
      duration: DURATION.slow,
      ease: EASING.spring,
    },
  },
};

// Common transitions
export const defaultTransition: Transition = {
  duration: DURATION.base,
  ease: EASING.inOut,
};

export const fastTransition: Transition = {
  duration: DURATION.fast,
  ease: EASING.out,
};

export const slowTransition: Transition = {
  duration: DURATION.slow,
  ease: EASING.smooth,
};

export const springTransition: Transition = {
  type: "spring",
  stiffness: 300,
  damping: 30,
};

// Stagger configuration
export const staggerContainer = (staggerDelay = 0.1): Transition => ({
  staggerChildren: staggerDelay,
});

/**
 * Check if user prefers reduced motion
 */
export const prefersReducedMotion = (): boolean => {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
};

/**
 * Get transition with reduced motion fallback
 */
export const getTransition = (
  normalTransition: Transition,
  reducedTransition?: Transition
): Transition => {
  if (prefersReducedMotion()) {
    return reducedTransition || {
      duration: DURATION.instant,
      ease: "linear",
    };
  }
  return normalTransition;
};

/**
 * Get variants with reduced motion fallback
 */
export const getVariants = (
  normalVariants: Variants,
  reducedVariants?: Variants
): Variants => {
  if (prefersReducedMotion()) {
    return reducedVariants || fadeInVariants;
  }
  return normalVariants;
};

/**
 * Create a delay function for sequential animations
 */
export const createDelayedTransition = (
  baseTransition: Transition,
  delay: number
): Transition => ({
  ...baseTransition,
  delay,
});

/**
 * Animation presets for common use cases
 */
export const ANIMATION_PRESETS = {
  // Page transitions
  pageEnter: {
    variants: slideInRightVariants,
    transition: defaultTransition,
  },
  pageExit: {
    variants: slideInLeftVariants,
    transition: defaultTransition,
  },

  // Modal/Dialog
  modalEnter: {
    variants: scaleInCenterVariants,
    transition: fastTransition,
  },
  modalExit: {
    variants: fadeInVariants,
    transition: fastTransition,
  },

  // Toast/Notification
  toastEnter: {
    variants: slideInDownVariants,
    transition: fastTransition,
  },
  toastExit: {
    variants: slideInUpVariants,
    transition: fastTransition,
  },

  // Card appearance
  cardEnter: {
    variants: slideInUpVariants,
    transition: defaultTransition,
  },

  // Button press
  buttonTap: {
    scale: 0.95,
    transition: { duration: DURATION.instant },
  },

  // Hover effects
  hoverScale: {
    scale: 1.05,
    transition: { duration: DURATION.fast },
  },
} as const;

/**
 * Create staggered list animation
 */
export const createStaggeredList = (itemCount: number, staggerDelay = 0.1) => {
  return Array.from({ length: itemCount }, (_, index) => ({
    delay: index * staggerDelay,
  }));
};

/**
 * Spring animation configurations
 */
export const SPRING_CONFIGS = {
  // Bouncy spring
  bouncy: {
    type: "spring" as const,
    stiffness: 400,
    damping: 25,
  },
  // Gentle spring
  gentle: {
    type: "spring" as const,
    stiffness: 200,
    damping: 30,
  },
  // Snappy spring
  snappy: {
    type: "spring" as const,
    stiffness: 500,
    damping: 35,
  },
  // Smooth spring
  smooth: {
    type: "spring" as const,
    stiffness: 100,
    damping: 20,
  },
} as const;

/**
 * Gesture animation configurations
 */
export const GESTURE_CONFIGS = {
  // Swipe to dismiss
  swipe: {
    drag: "x" as const,
    dragConstraints: { left: 0, right: 0 },
    dragElastic: 0.2,
  },
  // Pull to refresh
  pull: {
    drag: "y" as const,
    dragConstraints: { top: -100, bottom: 0 },
    dragElastic: 0.3,
  },
} as const;

/**
 * Performance optimization: Use will-change hint
 */
export const willChangeTransform = {
  willChange: "transform",
};

export const willChangeOpacity = {
  willChange: "opacity",
};

export const willChangeBoth = {
  willChange: "transform, opacity",
};
