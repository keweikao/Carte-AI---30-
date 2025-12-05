import {
    WifiOff,
    ServerOff,
    Clock,
    MapPinOff,
    FileX,
    AlertCircle,
    LucideIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";

type ErrorType =
    | "network"
    | "server"
    | "timeout"
    | "restaurant_not_found"
    | "no_menu"
    | "generic";

interface ErrorStateProps {
    type: ErrorType;
    onRetry?: () => void;
    onBack?: () => void;
    className?: string;
}

const errorConfig: Record<
    ErrorType,
    {
        icon: LucideIcon;
        title: string;
        description: string;
        primaryAction: string;
        secondaryAction: string;
    }
> = {
    network: {
        icon: WifiOff,
        title: "網路連線失敗",
        description: "請檢查你的網路連線後重試",
        primaryAction: "重新嘗試",
        secondaryAction: "回首頁",
    },
    server: {
        icon: ServerOff,
        title: "伺服器忙碌中",
        description: "目前使用人數較多，請稍後再試",
        primaryAction: "重新嘗試",
        secondaryAction: "回首頁",
    },
    timeout: {
        icon: Clock,
        title: "請求逾時",
        description: "處理時間過長，請重新嘗試",
        primaryAction: "重新嘗試",
        secondaryAction: "回首頁",
    },
    restaurant_not_found: {
        icon: MapPinOff,
        title: "找不到餐廳資訊",
        description: "我們目前沒有這間餐廳的菜單資料",
        primaryAction: "搜尋其他餐廳",
        secondaryAction: "回報問題",
    },
    no_menu: {
        icon: FileX,
        title: "無法取得菜單",
        description: "這間餐廳的菜單資訊暫時無法取得",
        primaryAction: "搜尋其他餐廳",
        secondaryAction: "回報問題",
    },
    generic: {
        icon: AlertCircle,
        title: "發生錯誤",
        description: "請重新嘗試，如問題持續請聯繫我們",
        primaryAction: "重新嘗試",
        secondaryAction: "回首頁",
    },
};

export function ErrorState({
    type,
    onRetry,
    onBack,
    className,
}: ErrorStateProps) {
    const config = errorConfig[type];
    const Icon = config.icon;

    return (
        <div
            className={cn(
                "flex flex-col items-center justify-center text-center py-12 px-4 min-h-[400px]",
                className
            )}
        >
            {/* Icon */}
            <div className="mb-6 p-6 rounded-full bg-terracotta/10">
                <Icon className="w-12 h-12 text-terracotta" />
            </div>

            {/* Title */}
            <h2 className="text-2xl font-serif font-bold text-charcoal mb-3">
                {config.title}
            </h2>

            {/* Description */}
            <p className="text-base text-gray-500 max-w-md mb-8">
                {config.description}
            </p>

            {/* Actions */}
            <div className="flex flex-col sm:flex-row gap-3">
                {/* Primary Action */}
                {onRetry && (
                    <button
                        onClick={onRetry}
                        className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-white bg-gradient-to-r from-caramel to-terracotta rounded-full hover:opacity-90 hover:shadow-medium transition-all"
                    >
                        {config.primaryAction}
                    </button>
                )}

                {/* Secondary Action */}
                {onBack && (
                    <button
                        onClick={onBack}
                        className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-charcoal bg-transparent border-2 border-charcoal rounded-full hover:bg-charcoal hover:text-cream transition-all"
                    >
                        {config.secondaryAction}
                    </button>
                )}
            </div>

            {/* Help Text */}
            <p className="mt-8 text-sm text-gray-400">
                需要協助？{" "}
                <a
                    href="mailto:hello@carte.tw"
                    className="text-caramel hover:text-caramel-700 underline"
                >
                    聯絡我們
                </a>
            </p>
        </div>
    );
}
