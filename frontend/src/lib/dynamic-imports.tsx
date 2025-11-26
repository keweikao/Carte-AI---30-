/**
 * Centralized dynamic imports for performance optimization
 * These components are loaded on-demand to reduce initial bundle size
 */

import dynamic from 'next/dynamic';

// Heavy animation library - only load when needed
export const ConfettiDynamic = dynamic(() => import('canvas-confetti').then(mod => mod.default), {
  ssr: false,
});

// Modal components - only load when user interacts
export const RatingModalDynamic = dynamic(
  () => import('@/components/rating-modal').then(mod => ({ default: mod.RatingModal })),
  {
    ssr: false,
    loading: () => null,
  }
);

// Feature showcase - can be lazy loaded as it's below the fold
export const FeatureShowcaseDynamic = dynamic(
  () => import('@/components/feature-showcase').then(mod => ({ default: mod.FeatureShowcase })),
  {
    ssr: true,
  }
);
