"use client";

import { toast } from "@/lib/use-toast";
import { AlertCircle, XCircle, AlertTriangle } from "lucide-react";

/**
 * API Error Types
 */
export enum ErrorType {
  NETWORK = "NETWORK",
  VALIDATION = "VALIDATION",
  AUTHENTICATION = "AUTHENTICATION",
  AUTHORIZATION = "AUTHORIZATION",
  NOT_FOUND = "NOT_FOUND",
  SERVER = "SERVER",
  UNKNOWN = "UNKNOWN",
}

/**
 * API Error Class
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public type: ErrorType = ErrorType.UNKNOWN,
    public details?: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Parse API error response
 */
export function parseApiError(error: unknown): ApiError {
  // Network error
  if (error instanceof TypeError && error.message === "Failed to fetch") {
    return new ApiError(
      "無法連接到伺服器，請檢查您的網路連接",
      0,
      ErrorType.NETWORK
    );
  }

  // Fetch API error with response
  if (error && typeof error === "object" && "response" in error) {
    const response = (error as { response: Response }).response;

    switch (response.status) {
      case 400:
        return new ApiError(
          "請求資料格式錯誤",
          400,
          ErrorType.VALIDATION,
          error
        );
      case 401:
        return new ApiError(
          "請先登入以繼續",
          401,
          ErrorType.AUTHENTICATION,
          error
        );
      case 403:
        return new ApiError(
          "您沒有權限執行此操作",
          403,
          ErrorType.AUTHORIZATION,
          error
        );
      case 404:
        return new ApiError("找不到請求的資源", 404, ErrorType.NOT_FOUND, error);
      case 500:
        return new ApiError(
          "伺服器發生錯誤，請稍後再試",
          500,
          ErrorType.SERVER,
          error
        );
      case 502:
      case 503:
      case 504:
        return new ApiError(
          "伺服器暫時無法使用，請稍後再試",
          response.status,
          ErrorType.SERVER,
          error
        );
      default:
        return new ApiError(
          "發生未知錯誤，請稍後再試",
          response.status,
          ErrorType.UNKNOWN,
          error
        );
    }
  }

  // Standard Error object
  if (error instanceof Error) {
    return new ApiError(error.message, undefined, ErrorType.UNKNOWN, error);
  }

  // Unknown error
  return new ApiError(
    "發生未知錯誤，請稍後再試",
    undefined,
    ErrorType.UNKNOWN,
    error
  );
}

/**
 * Show error toast notification
 */
export function showErrorToast(error: ApiError | Error | unknown) {
  const apiError = error instanceof ApiError ? error : parseApiError(error);

  const errorConfig = {
    [ErrorType.NETWORK]: {
      icon: AlertTriangle,
      title: "網路連接問題",
      description: apiError.message,
    },
    [ErrorType.VALIDATION]: {
      icon: AlertCircle,
      title: "資料驗證失敗",
      description: apiError.message,
    },
    [ErrorType.AUTHENTICATION]: {
      icon: XCircle,
      title: "身份驗證失敗",
      description: apiError.message,
    },
    [ErrorType.AUTHORIZATION]: {
      icon: XCircle,
      title: "權限不足",
      description: apiError.message,
    },
    [ErrorType.NOT_FOUND]: {
      icon: AlertCircle,
      title: "找不到資源",
      description: apiError.message,
    },
    [ErrorType.SERVER]: {
      icon: XCircle,
      title: "伺服器錯誤",
      description: apiError.message,
    },
    [ErrorType.UNKNOWN]: {
      icon: XCircle,
      title: "發生錯誤",
      description: apiError.message,
    },
  };

    const config = errorConfig[apiError.type];            
                                                          
    toast({    title: config.title,
    description: config.description,
    variant: "destructive",
  });

  // Log error in development
  if (process.env.NODE_ENV === "development") {
    console.error("API Error:", apiError);
  }
}

/**
 * Fetch wrapper with automatic error handling
 *
 * Usage:
 * ```tsx
 * const data = await fetchWithErrorHandling('/api/restaurants', {
 *   method: 'GET',
 * });
 * ```
 */
export async function fetchWithErrorHandling<T>(
  url: string,
  options?: RequestInit,
  showToast = true
): Promise<T> {
  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      const error = new ApiError(
        `HTTP error! status: ${response.status}`,
        response.status,
        ErrorType.UNKNOWN
      );
      throw { response, error };
    }

    return await response.json();
  } catch (error) {
    const apiError = parseApiError(error);

    if (showToast) {
      showErrorToast(apiError);
    }

    throw apiError;
  }
}

/**
 * Async function wrapper with error handling
 *
 * Usage:
 * ```tsx
 * const loadData = withErrorHandling(async () => {
 *   const data = await fetch('/api/data');
 *   return data;
 * });
 *
 * await loadData(); // Automatically shows toast on error
 * ```
 */
export function withErrorHandling<T extends (...args: unknown[]) => Promise<unknown>>(
  fn: T,
  showToast = true
): T {
  return (async (...args: unknown[]) => {
    try {
      return await fn(...args);
    } catch (error) {
      if (showToast) {
        showErrorToast(error);
      }
      throw error;
    }
  }) as T;
}
