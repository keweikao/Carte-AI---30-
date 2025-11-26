import { LoginForm } from "@/components/login-form"
import { BrandHeader } from "@/components/brand-header"
import { FeatureShowcase } from "@/components/feature-showcase"

export const metadata = {
  title: "Carte - AI 驅動的用餐助手",
  description: "智慧推薦餐廳和菜色，享受更好的用餐體驗",
}

export default function LoginPage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-background via-background to-primary/5">
      {/* Hero Section with Branding */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-12 py-16 lg:grid-cols-2 lg:gap-8 lg:py-24">
          {/* Left Column - Brand & Features */}
          <div className="flex flex-col justify-center space-y-8">
            <BrandHeader />
            <FeatureShowcase />
          </div>

          {/* Right Column - Login Form */}
          <div className="flex items-center justify-center">
            <LoginForm />
          </div>
        </div>
      </div>

      {/* Trust Section - Bottom */}
      <div className="border-t border-border bg-card/30 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm text-muted-foreground">被全台灣的美食愛好者信任 • 智慧推薦 • 個人化體驗</p>
        </div>
      </div>
    </main>
  )
}
