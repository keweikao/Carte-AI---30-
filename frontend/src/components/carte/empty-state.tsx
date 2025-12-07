import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface EmptyStateProps {
    icon?: LucideIcon;
    title: string;
    description?: string;
    action?: {
        label: string;
        onClick: () => void;
    };
    className?: string;
}

export function EmptyState({
    icon: Icon,
    title,
    description,
    action,
    className,
}: EmptyStateProps) {
    return (
        <div
            className={cn(
                "flex flex-col items-center justify-center text-center py-12 px-4",
                className
            )}
        >
            {/* Icon */}
            {Icon && (
                <div className="mb-4 p-4 rounded-full bg-gray-100">
                    <Icon className="w-8 h-8 text-gray-400" />
                </div>
            )}

            {/* Title */}
            <h3 className="text-lg font-semibold text-charcoal mb-2">
                {title}
            </h3>

            {/* Description */}
            {description && (
                <p className="text-sm text-gray-500 max-w-sm mb-6">
                    {description}
                </p>
            )}

            {/* Action Button */}
            {action && (
                <button
                    onClick={action.onClick}
                    className="inline-flex items-center justify-center px-6 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-caramel to-terracotta rounded-full hover:opacity-90 hover:shadow-medium transition-all"
                >
                    {action.label}
                </button>
            )}
        </div>
    );
}
