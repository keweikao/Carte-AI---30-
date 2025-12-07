import { cn } from "@/lib/utils";

interface StepIndicatorProps {
    steps: string[];
    currentStep: number; // 0-based index
    className?: string;
}

export function StepIndicator({ steps, currentStep, className }: StepIndicatorProps) {
    return (
        <div className={cn("flex items-center gap-3 md:gap-4", className)}>
            {steps.map((label, index) => {
                const active = index <= currentStep;
                const isCurrent = index === currentStep;
                return (
                    <div key={label} className="flex items-center gap-2">
                        <div
                            className={cn(
                                "relative flex items-center justify-center",
                                "h-7 w-7 rounded-full border-2 transition-all",
                                active
                                    ? "border-terracotta bg-terracotta text-white shadow-card"
                                    : "border-[var(--color-border)] bg-cream-200 text-charcoal/60"
                            )}
                        >
                            <span className="text-sm font-medium">
                                {index + 1}
                            </span>
                            {isCurrent && (
                                <span className="absolute -bottom-3 left-1/2 h-2 w-[1px] -translate-x-1/2 rounded-full bg-terracotta" />
                            )}
                        </div>
                        <div className="flex flex-col">
                            <span
                                className={cn(
                                    "text-sm md:text-base font-body transition-colors",
                                    active ? "text-charcoal" : "text-charcoal/60"
                                )}
                            >
                                {label}
                            </span>
                            <div className="h-1 w-full rounded-full bg-cream-200 overflow-hidden">
                                <div
                                    className={cn(
                                        "h-full rounded-full transition-all",
                                        active ? "bg-gradient-to-r from-accent-start to-accent-end" : "bg-cream-200"
                                    )}
                                    style={{ width: active ? "100%" : "0%" }}
                                />
                            </div>
                        </div>
                        {index < steps.length - 1 && (
                            <div className="hidden md:block h-px w-10 bg-[var(--color-border)]" aria-hidden />
                        )}
                    </div>
                );
            })}
        </div>
    );
}
