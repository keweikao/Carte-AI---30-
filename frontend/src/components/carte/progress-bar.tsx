"use client";

import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface ProgressBarProps {
    currentStep: number;
    totalSteps: number;
    labels?: string[];
    type?: "stepped" | "continuous";
    className?: string;
}

export function ProgressBar({
    currentStep,
    totalSteps,
    labels = [],
    type = "stepped",
    className,
}: ProgressBarProps) {
    const progress = (currentStep / totalSteps) * 100;

    if (type === "continuous") {
        return (
            <div className={cn("w-full space-y-2", className)}>
                {/* Progress Bar */}
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-gradient-to-r from-caramel to-terracotta transition-all duration-300 ease-out"
                        style={{ width: `${progress}%` }}
                    />
                </div>

                {/* Percentage */}
                <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-500">進度</span>
                    <span className="text-xs font-medium text-charcoal">
                        {Math.round(progress)}%
                    </span>
                </div>
            </div>
        );
    }

    // Stepped variant
    return (
        <div className={cn("w-full", className)}>
            {/* Step Labels */}
            {labels.length > 0 && (
                <div className="flex justify-between mb-2">
                    {labels.map((label, index) => (
                        <span
                            key={index}
                            className={cn(
                                "text-xs font-medium transition-colors duration-300",
                                index + 1 < currentStep
                                    ? "text-caramel"
                                    : index + 1 === currentStep
                                        ? "text-charcoal"
                                        : "text-gray-300"
                            )}
                        >
                            {label}
                        </span>
                    ))}
                </div>
            )}

            {/* Steps */}
            <div className="flex items-center justify-between">
                {Array.from({ length: totalSteps }).map((_, index) => {
                    const stepNumber = index + 1;
                    const isCompleted = stepNumber < currentStep;
                    const isCurrent = stepNumber === currentStep;
                    const isPending = stepNumber > currentStep;

                    return (
                        <div
                            key={index}
                            className="flex items-center flex-1"
                        >
                            {/* Step Circle */}
                            <div
                                className={cn(
                                    "flex items-center justify-center w-8 h-8 rounded-full border-2 transition-all duration-300",
                                    isCompleted &&
                                    "bg-caramel border-caramel text-white",
                                    isCurrent &&
                                    "bg-white border-caramel text-caramel scale-110",
                                    isPending &&
                                    "bg-white border-gray-200 text-gray-400"
                                )}
                            >
                                {isCompleted ? (
                                    <Check className="w-4 h-4" />
                                ) : (
                                    <span className="text-sm font-semibold">{stepNumber}</span>
                                )}
                            </div>

                            {/* Connector Line */}
                            {index < totalSteps - 1 && (
                                <div
                                    className={cn(
                                        "flex-1 h-0.5 mx-2 transition-all duration-300",
                                        stepNumber < currentStep
                                            ? "bg-caramel"
                                            : "bg-gray-200"
                                    )}
                                />
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Step Counter */}
            <div className="mt-3 text-center">
                <span className="text-sm text-gray-500">
                    步驟 {currentStep} / {totalSteps}
                </span>
            </div>
        </div>
    );
}
