"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AlertTriangle, RefreshCcw } from "lucide-react";

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<ErrorFallbackProps>;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export interface ErrorFallbackProps {
  error: Error;
  resetError: () => void;
}

/**
 * Default Error Fallback Component
 * Displays a magazine-style error message with retry functionality
 */
function DefaultErrorFallback({ error, resetError }: ErrorFallbackProps) {
  return (
    <div className="min-h-[60vh] flex items-center justify-center px-4 py-12">
      <Card className="max-w-2xl w-full bg-cream-50 border-caramel-100 shadow-card">
        <div className="p-8 md:p-12">
          {/* Error Icon */}
          <div className="flex justify-center mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-terracotta/10 blur-2xl rounded-full" />
              <div className="relative bg-terracotta/10 rounded-full p-4">
                <AlertTriangle className="w-12 h-12 text-terracotta" />
              </div>
            </div>
          </div>

          {/* Error Message */}
          <div className="text-center space-y-4 mb-8">
            <h1 className="font-display text-3xl md:text-4xl text-charcoal font-semibold">
              糟糕！出了點問題
            </h1>
            <p className="text-charcoal/70 text-lg leading-relaxed">
              我們遇到了一個意外的錯誤。別擔心，這不是你的問題。
            </p>
          </div>

          {/* Error Details (for development) */}
          {process.env.NODE_ENV === "development" && (
            <div className="mb-6 p-4 bg-charcoal/5 rounded-lg border border-charcoal/10">
              <p className="text-xs font-mono text-charcoal/60 mb-2">
                開發模式錯誤詳情：
              </p>
              <p className="text-sm font-mono text-terracotta break-all">
                {error.message}
              </p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button
              onClick={resetError}
              className="bg-terracotta hover:bg-terracotta-700 text-white px-6 py-6 text-base"
            >
              <RefreshCcw className="w-4 h-4 mr-2" />
              重新嘗試
            </Button>
            <Button
              onClick={() => (window.location.href = "/")}
              variant="outline"
              className="border-caramel-700 text-caramel-900 hover:bg-caramel-50 px-6 py-6 text-base"
            >
              返回首頁
            </Button>
          </div>

          {/* Support Information */}
          <div className="mt-8 pt-6 border-t border-charcoal/10 text-center">
            <p className="text-sm text-charcoal/60">
              如果問題持續發生，請{" "}
              <a
                href="mailto:support@carte.com"
                className="text-terracotta hover:underline font-medium"
              >
                聯繫客服團隊
              </a>
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}

/**
 * ErrorBoundary Component
 * Catches React errors and displays a fallback UI
 *
 * Usage:
 * ```tsx
 * <ErrorBoundary>
 *   <YourComponent />
 * </ErrorBoundary>
 * ```
 *
 * Custom fallback:
 * ```tsx
 * <ErrorBoundary fallback={CustomErrorFallback}>
 *   <YourComponent />
 * </ErrorBoundary>
 * ```
 */
export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log error to console in development
    if (process.env.NODE_ENV === "development") {
      console.error("ErrorBoundary caught an error:", error, errorInfo);
    }

    // Here you can also log to an error reporting service
    // logErrorToService(error, errorInfo);
  }

  resetError = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return (
        <FallbackComponent
          error={this.state.error}
          resetError={this.resetError}
        />
      );
    }

    return this.props.children;
  }
}

/**
 * Hook-based error boundary wrapper
 * Use this in client components where you need error boundary functionality
 */
export function withErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  fallback?: React.ComponentType<ErrorFallbackProps>
) {
  return function WithErrorBoundaryWrapper(props: P) {
    return (
      <ErrorBoundary fallback={fallback}>
        <Component {...props} />
      </ErrorBoundary>
    );
  };
}
