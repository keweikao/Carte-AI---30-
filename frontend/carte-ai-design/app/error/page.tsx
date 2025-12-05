"use client"

import { useSearchParams } from "next/navigation"
import { Suspense } from "react"
import { ErrorState } from "@/components/carte/error-state"

function ErrorContent() {
  const searchParams = useSearchParams()
  const errorType = (searchParams.get("type") as "network" | "server" | "timeout" | "generic") || "generic"

  const handleRetry = () => {
    window.history.back()
  }

  return <ErrorState type={errorType} onRetry={handleRetry} />
}

export default function ErrorPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-cream" />}>
      <ErrorContent />
    </Suspense>
  )
}
