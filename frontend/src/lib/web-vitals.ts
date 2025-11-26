import { onCLS, onFCP, onLCP, onTTFB, onINP, Metric } from 'web-vitals';
import { event } from './analytics';

function sendToAnalytics(metric: Metric) {
  // Send to Google Analytics
  event({
    action: metric.name,
    category: 'Web Vitals',
    label: metric.id,
    value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
  });

  // Log to console in development
  if (process.env.NODE_ENV === 'development') {
    console.log('[Web Vitals]', {
      name: metric.name,
      value: metric.value,
      rating: metric.rating,
      delta: metric.delta,
    });
  }
}

export function reportWebVitals() {
  try {
    onCLS(sendToAnalytics);
    // onFID is deprecated, replaced by INP (Interaction to Next Paint)
    onFCP(sendToAnalytics);
    onLCP(sendToAnalytics);
    onTTFB(sendToAnalytics);
    onINP(sendToAnalytics);
  } catch (err) {
    console.error('Failed to report web vitals:', err);
  }
}
