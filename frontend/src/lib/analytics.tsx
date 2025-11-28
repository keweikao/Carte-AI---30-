'use client';

import { useEffect, Suspense } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';

export const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID;

// https://developers.google.com/analytics/devguides/collection/gtagjs/pages
export const pageview = (url: string) => {
  if (typeof window.gtag !== 'undefined') {
    window.gtag('config', GA_MEASUREMENT_ID as string, {
      page_path: url,
    });
  }
};

// https://developers.google.com/analytics/devguides/collection/gtagjs/events
export const event = ({
  action,
  category,
  label,
  value,
}: {
  action: string;
  category: string;
  label?: string;
  value?: number;
}) => {
  if (typeof window.gtag !== 'undefined') {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }
};

// Custom events for our app
export const trackRestaurantSearch = (restaurantName: string) => {
  event({
    action: 'search',
    category: 'Restaurant',
    label: restaurantName,
  });
};

export const trackRecommendationView = (recommendationId: string) => {
  event({
    action: 'view',
    category: 'Recommendation',
    label: recommendationId,
  });
};

export const trackDishSwap = (dishName: string) => {
  event({
    action: 'swap',
    category: 'Dish',
    label: dishName,
  });
};

export const trackDishSelect = (dishName: string) => {
  event({
    action: 'select',
    category: 'Dish',
    label: dishName,
  });
};

export const trackMenuComplete = (totalPrice: number, dishCount: number) => {
  event({
    action: 'complete',
    category: 'Menu',
    label: `${dishCount} dishes`,
    value: totalPrice,
  });
};

export const trackMenuShare = (method: 'download' | 'copy') => {
  event({
    action: 'share',
    category: 'Menu',
    label: method,
  });
};

export const trackRatingSubmit = (rating: 'up' | 'down') => {
  event({
    action: 'submit',
    category: 'Rating',
    label: rating,
  });
};

// Export wrapped in Suspense to avoid SSR issues
export function Analytics({ gaId }: { gaId?: string }) {
  return (
    <Suspense fallback={null}>
      <AnalyticsInner gaId={gaId} />
    </Suspense>
  );
}

// Analytics component to track page views
function AnalyticsInner({ gaId }: { gaId?: string }) {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const measurementId = gaId || GA_MEASUREMENT_ID;

  useEffect(() => {
    if (measurementId) {
      const url = pathname + (searchParams?.toString() ? `?${searchParams.toString()}` : '');
      // We need to pass the ID to pageview if we want to support dynamic ID, 
      // but pageview function is exported separately. 
      // For now, let's just assume pageview uses the global constant or we update it too.
      // Actually, pageview uses GA_MEASUREMENT_ID constant. 
      // If we want runtime ID, we should probably update pageview signature or window config.

      // Since we configured the ID in layout.tsx via gtag('config'), 
      // subsequent events just need to send 'page_view' event or update config.

      if (typeof window.gtag !== 'undefined') {
        window.gtag('config', measurementId as string, {
          page_path: url,
        });
      }
    }
  }, [pathname, searchParams, measurementId]);

  return null;
}

// Type declaration for gtag
declare global {
  interface Window {
    gtag: (
      command: 'config' | 'event',
      targetId: string,
      config?: Record<string, unknown>
    ) => void;
  }
}
