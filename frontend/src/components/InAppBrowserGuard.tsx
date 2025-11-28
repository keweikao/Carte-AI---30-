"use client";

import { useEffect, useState } from "react";

export function InAppBrowserGuard() {
    const [isInApp, setIsInApp] = useState(false);

    useEffect(() => {
        if (typeof window === "undefined") return;

        const userAgent = navigator.userAgent || navigator.vendor || (window as unknown as { opera?: string }).opera || "";
        // Detect Messenger, LINE, Instagram, Facebook app
        // FBAN/FBAV = Facebook App
        // Line = LINE App
        // Instagram = Instagram App
        if (/FBAN|FBAV|Line|Instagram/.test(userAgent)) {
            setIsInApp(true);
        }
    }, []);

    if (!isInApp) return null;

    return (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm">
            <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl text-center">
                <div className="mb-4 flex justify-center">
                    <div className="rounded-full bg-blue-100 p-3">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-600">
                            <circle cx="12" cy="12" r="10"></circle>
                            <circle cx="12" cy="12" r="4"></circle>
                            <line x1="4.93" y1="4.93" x2="9.17" y2="9.17"></line>
                            <line x1="14.83" y1="14.83" x2="19.07" y2="19.07"></line>
                            <line x1="14.83" y1="9.17" x2="19.07" y2="4.93"></line>
                            <line x1="14.83" y1="9.17" x2="18.36" y2="5.64"></line>
                            <line x1="4.93" y1="19.07" x2="9.17" y2="14.83"></line>
                        </svg>
                    </div>
                </div>
                <h2 className="mb-2 text-xl font-bold text-gray-900">請使用瀏覽器開啟</h2>
                <p className="mb-6 text-gray-600">
                    為了確保您的帳號安全，Google 不支援在 App 內建瀏覽器（如 Messenger, LINE）中登入。
                </p>
                <div className="rounded-lg bg-gray-50 p-4 text-left text-sm text-gray-700">
                    <p className="font-semibold mb-2">如何操作：</p>
                    <ol className="list-decimal pl-5 space-y-1">
                        <li>點擊畫面角落的 <span className="font-bold">「...」</span> 或 <span className="font-bold">分享圖示</span></li>
                        <li>選擇 <span className="font-bold">「以瀏覽器開啟」</span> (Open in Browser)</li>
                    </ol>
                </div>
            </div>
        </div>
    );
}
