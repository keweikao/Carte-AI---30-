/**
 * Haptic Feedback Utilities
 *
 * Provides haptic feedback functions for mobile devices
 * with graceful fallback for unsupported browsers.
 */

/**
 * Light haptic feedback for subtle interactions
 * Duration: 10ms
 */
export const hapticLight = (): void => {
  if (typeof window !== "undefined" && "vibrate" in navigator) {
    navigator.vibrate(10)
  }
}

/**
 * Medium haptic feedback for standard interactions
 * Duration: 20ms
 */
export const hapticMedium = (): void => {
  if (typeof window !== "undefined" && "vibrate" in navigator) {
    navigator.vibrate(20)
  }
}

/**
 * Heavy haptic feedback for important actions
 * Duration: 30ms
 */
export const hapticHeavy = (): void => {
  if (typeof window !== "undefined" && "vibrate" in navigator) {
    navigator.vibrate(30)
  }
}

/**
 * Success haptic feedback (double tap pattern)
 * Pattern: vibrate 20ms, pause 50ms, vibrate 20ms
 */
export const hapticSuccess = (): void => {
  if (typeof window !== "undefined" && "vibrate" in navigator) {
    navigator.vibrate([20, 50, 20])
  }
}

/**
 * Error haptic feedback (triple tap pattern)
 * Pattern: vibrate 10ms, pause 20ms, vibrate 10ms, pause 20ms, vibrate 10ms
 */
export const hapticError = (): void => {
  if (typeof window !== "undefined" && "vibrate" in navigator) {
    navigator.vibrate([10, 20, 10, 20, 10])
  }
}

/**
 * Warning haptic feedback (longer single vibration)
 * Duration: 40ms
 */
export const hapticWarning = (): void => {
  if (typeof window !== "undefined" && "vibrate" in navigator) {
    navigator.vibrate(40)
  }
}

/**
 * Check if haptic feedback is supported
 */
export const isHapticSupported = (): boolean => {
  return typeof window !== "undefined" && "vibrate" in navigator
}

/**
 * Custom haptic pattern
 * @param pattern - Array of vibration durations in ms [vibrate, pause, vibrate, ...]
 */
export const hapticCustom = (pattern: number | number[]): void => {
  if (typeof window !== "undefined" && "vibrate" in navigator) {
    navigator.vibrate(pattern)
  }
}
