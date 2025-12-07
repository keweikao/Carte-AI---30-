'use client';

import { usePWA } from '@/contexts/PWAContext';

export function PWAInstaller() {
  const { isInstallable, install, ignore } = usePWA();

  // Show install button only if installable
  if (!isInstallable) {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 animate-in slide-in-from-bottom">
      <div className="bg-white border-2 border-charcoal shadow-lg rounded-lg p-4 max-w-sm">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <svg
              className="w-8 h-8 text-sage-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
              />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="font-display font-semibold text-charcoal mb-1">
              安裝 Carte AI
            </h3>
            <p className="text-sm text-charcoal/70 mb-3">
              將應用程式新增至主畫面，享受更快速的體驗
            </p>
            <div className="flex gap-2">
              <button
                onClick={install}
                className="px-4 py-2 bg-sage-600 text-white rounded-md text-sm font-medium hover:bg-sage-700 transition-colors"
              >
                安裝
              </button>
              <button
                onClick={ignore}
                className="px-4 py-2 bg-cream-200 text-charcoal rounded-md text-sm font-medium hover:bg-cream-300 transition-colors"
              >
                稍後
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

