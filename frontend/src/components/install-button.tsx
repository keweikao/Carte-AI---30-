'use client';

import { usePWA } from '@/contexts/PWAContext';
import { Download } from 'lucide-react';

export function InstallButton() {
    const { isInstallable, install } = usePWA();

    if (!isInstallable) {
        return null;
    }

    return (
        <button
            onClick={install}
            className="flex items-center gap-2 px-4 py-2 bg-sage-600 text-white rounded-full text-sm font-medium hover:bg-sage-700 transition-colors shadow-sm"
        >
            <Download className="w-4 h-4" />
            安裝 App
        </button>
    );
}
