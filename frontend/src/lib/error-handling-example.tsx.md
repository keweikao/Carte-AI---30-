/**
 * Error Handling Examples
 *
 * This file demonstrates how to use the error handling system in your application.
 * DO NOT import this file directly - it's for reference only.
 */

// ============================================================================
// Example 1: Using ErrorBoundary with a component
// ============================================================================

import { ErrorBoundary } from "@/components/error-boundary";

function MyPage() {
  return (
    <ErrorBoundary>
      <MyComponent />
    </ErrorBoundary>
  );
}

// ============================================================================
// Example 2: Using withErrorBoundary HOC
// ============================================================================

import { withErrorBoundary } from "@/components/error-boundary";

function MyComponent() {
  // Component that might throw errors
  return <div>Content</div>;
}

export default withErrorBoundary(MyComponent);

// ============================================================================
// Example 3: Custom Error Fallback
// ============================================================================

import type { ErrorFallbackProps } from "@/components/error-boundary";

function CustomErrorFallback({ error, resetError }: ErrorFallbackProps) {
  return (
    <div>
      <h1>Oops! Something went wrong</h1>
      <p>{error.message}</p>
      <button onClick={resetError}>Try again</button>
    </div>
  );
}

function MyPageWithCustomFallback() {
  return (
    <ErrorBoundary fallback={CustomErrorFallback}>
      <MyComponent />
    </ErrorBoundary>
  );
}

// ============================================================================
// Example 4: Using API Error Handler
// ============================================================================

import { fetchWithErrorHandling, showErrorToast } from "@/lib/api-error-handler";

async function loadRestaurants() {
  try {
    // Automatically shows error toast on failure
    const data = await fetchWithErrorHandling<Restaurant[]>(
      "/api/restaurants",
      { method: "GET" }
    );
    return data;
  } catch (error) {
    // Error already shown as toast
    console.error("Failed to load restaurants:", error);
  }
}

// ============================================================================
// Example 5: Using API Error Handler without automatic toast
// ============================================================================

async function loadRestaurantsWithoutToast() {
  try {
    const data = await fetchWithErrorHandling<Restaurant[]>(
      "/api/restaurants",
      { method: "GET" },
      false // Don't show toast automatically
    );
    return data;
  } catch (error) {
    // Handle error manually
    console.error("Failed to load restaurants:", error);
  }
}

// ============================================================================
// Example 6: Using withErrorHandling wrapper
// ============================================================================

import { withErrorHandling } from "@/lib/api-error-handler";

const loadData = withErrorHandling(async (id: string) => {
  const response = await fetch(`/api/data/${id}`);
  if (!response.ok) throw new Error("Failed to fetch");
  return response.json();
});

// Usage - automatically shows error toast
await loadData("123");

// ============================================================================
// Example 7: Manual error toast
// ============================================================================

import { showErrorToast, ApiError, ErrorType } from "@/lib/api-error-handler";

try {
  // Your code that might throw
  throw new Error("Something went wrong");
} catch (error) {
  // Show error toast manually
  showErrorToast(error);
}

// Or with custom ApiError
try {
  throw new ApiError(
    "找不到餐廳資料",
    404,
    ErrorType.NOT_FOUND
  );
} catch (error) {
  showErrorToast(error);
}

// ============================================================================
// Example 8: Using Network Status Hook
// ============================================================================

import { useNetworkStatus } from "@/components/network-status";

function MyComponent() {
  const isOnline = useNetworkStatus();

  if (!isOnline) {
    return <div>您目前離線，請檢查網路連接</div>;
  }

  return <div>正常內容</div>;
}

// ============================================================================
// Example 9: Complete API Call with Error Handling
// ============================================================================

import { useState } from "react";
import { fetchWithErrorHandling } from "@/lib/api-error-handler";
import { useNetworkStatus } from "@/components/network-status";

function RestaurantList() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(false);
  const isOnline = useNetworkStatus();

  async function loadRestaurants() {
    if (!isOnline) {
      return; // Network status component will show toast
    }

    setLoading(true);
    try {
      const data = await fetchWithErrorHandling<Restaurant[]>(
        "/api/restaurants"
      );
      setRestaurants(data);
    } catch (error) {
      // Error already handled by fetchWithErrorHandling
    } finally {
      setLoading(false);
    }
  }

  return (
    <ErrorBoundary>
      <div>
        {loading && <div>載入中...</div>}
        {restaurants.map((restaurant) => (
          <div key={restaurant.id}>{restaurant.name}</div>
        ))}
      </div>
    </ErrorBoundary>
  );
}

// ============================================================================
// Example 10: Testing Error Boundary
// ============================================================================

function ThrowErrorComponent() {
  // This will trigger the ErrorBoundary
  throw new Error("Test error");
  return <div>This won't render</div>;
}

function TestErrorBoundary() {
  return (
    <ErrorBoundary>
      <ThrowErrorComponent />
    </ErrorBoundary>
  );
}

// ============================================================================
// Type Definitions (for reference)
// ============================================================================

interface Restaurant {
  id: string;
  name: string;
  // ... other fields
}
