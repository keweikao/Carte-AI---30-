"use client";

import { useEffect, useState } from "react";
import { toast } from "@/lib/use-toast";
import { WifiOff } from "lucide-react";

/**
 * Network Status Monitor
 * Automatically detects network connection status and shows toast notifications
 *
 * Usage:
 * Add to your root layout or app component:
 * ```tsx
 * <NetworkStatus />
 * ```
 */
export function NetworkStatus() {
  const [isOnline, setIsOnline] = useState(() =>
    typeof window !== 'undefined' ? navigator.onLine : true
  );
  const [hasShownOffline, setHasShownOffline] = useState(false);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      setHasShownOffline(false);

      toast({
        title: "網路已連接",
        description: "您已重新連接到網路",
        variant: "default",
      });
    };

    const handleOffline = () => {
      setIsOnline(false);

      if (!hasShownOffline) {
        setHasShownOffline(true);
        toast({
          title: "網路連接中斷",
          description: "請檢查您的網路連接。某些功能可能無法使用。",
          variant: "destructive",
        });
      }
    };

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, [hasShownOffline]);

  // This component doesn't render anything visible
  return null;
}

/**
 * Hook to check current network status
 * Returns true if online, false if offline
 *
 * Usage:
 * ```tsx
 * const isOnline = useNetworkStatus();
 * if (!isOnline) {
 *   // Show offline UI or disable features
 * }
 * ```
 */
export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(
    typeof window !== "undefined" ? navigator.onLine : true
  );

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return isOnline;
}
