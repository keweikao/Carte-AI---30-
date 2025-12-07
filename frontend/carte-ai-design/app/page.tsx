import Link from "next/link"
import { Header } from "@/components/carte/header"
import { Footer } from "@/components/carte/footer"
import { Search, Users, Sparkles, MessageSquare, ChefHat, Star, ArrowRight, CheckCircle2 } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-cream">
      <Header />

      {/* Hero Section */}
      <section className="pt-24 pb-16 md:pt-32 md:pb-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-caramel/10 rounded-full mb-8">
              <Sparkles className="w-4 h-4 text-caramel" />
              <span className="text-sm font-medium text-charcoal">AI 智慧推薦</span>
            </div>

            {/* Headline */}
            <h1 className="font-serif text-4xl md:text-6xl lg:text-7xl text-charcoal leading-tight text-balance">
              讓 AI 成為您的
              <span className="block text-terracotta">私人美食顧問</span>
            </h1>

            {/* Subheadline */}
            <p className="mt-6 text-lg md:text-xl text-charcoal/60 leading-relaxed max-w-2xl mx-auto text-pretty">
              不再為「點什麼」煩惱。Carte AI 分析菜單與數百則評論， 為您的聚餐、約會、商務宴請推薦最完美的菜色組合。
            </p>

            {/* CTA Buttons */}
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/input"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-semibold text-white rounded-full gradient-primary shadow-lg hover:shadow-xl hover:scale-105 transition-all"
              >
                告訴我該點什麼
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href="#how-it-works"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-medium text-charcoal bg-white rounded-full border-2 border-charcoal/10 hover:border-charcoal/20 transition-all"
              >
                了解更多
              </Link>
            </div>

            {/* Trust Indicators */}
            <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-sm text-charcoal/50">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-caramel" />
                <span>免費使用</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-caramel" />
                <span>無需註冊</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-caramel" />
                <span>即時推薦</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 md:py-24 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="font-serif text-3xl md:text-4xl text-charcoal">為什麼選擇 Carte AI</h2>
            <p className="mt-4 text-charcoal/60 max-w-2xl mx-auto">結合 AI 分析與真實評論，提供最貼心的點餐建議</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="group p-8 bg-cream rounded-3xl hover:shadow-lg transition-all">
              <div className="w-14 h-14 flex items-center justify-center bg-caramel/10 rounded-2xl mb-6 group-hover:scale-110 transition-transform">
                <Search className="w-7 h-7 text-caramel" />
              </div>
              <h3 className="font-serif text-xl text-charcoal mb-3">智能菜單分析</h3>
              <p className="text-charcoal/60 leading-relaxed">
                輸入餐廳名稱，AI 自動分析完整菜單， 找出招牌菜與隱藏美食。
              </p>
            </div>

            {/* Feature 2 */}
            <div className="group p-8 bg-cream rounded-3xl hover:shadow-lg transition-all">
              <div className="w-14 h-14 flex items-center justify-center bg-terracotta/10 rounded-2xl mb-6 group-hover:scale-110 transition-transform">
                <MessageSquare className="w-7 h-7 text-terracotta" />
              </div>
              <h3 className="font-serif text-xl text-charcoal mb-3">評論整合分析</h3>
              <p className="text-charcoal/60 leading-relaxed">自動讀取數百則 Google 評論， 萃取最受好評的菜色推薦。</p>
            </div>

            {/* Feature 3 */}
            <div className="group p-8 bg-cream rounded-3xl hover:shadow-lg transition-all">
              <div className="w-14 h-14 flex items-center justify-center bg-charcoal/10 rounded-2xl mb-6 group-hover:scale-110 transition-transform">
                <Users className="w-7 h-7 text-charcoal" />
              </div>
              <h3 className="font-serif text-xl text-charcoal mb-3">個人化推薦</h3>
              <p className="text-charcoal/60 leading-relaxed">根據人數、場合、飲食偏好， 量身打造最適合的菜色組合。</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-16 md:py-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="font-serif text-3xl md:text-4xl text-charcoal">簡單四步驟</h2>
            <p className="mt-4 text-charcoal/60 max-w-2xl mx-auto">從搜尋餐廳到獲得推薦，只需一分鐘</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Step 1 */}
            <div className="relative">
              <div className="text-6xl font-serif text-caramel/20 mb-4">01</div>
              <h3 className="font-serif text-xl text-charcoal mb-2">搜尋餐廳</h3>
              <p className="text-sm text-charcoal/60">輸入餐廳名稱，系統自動取得菜單與評論資料</p>
            </div>

            {/* Step 2 */}
            <div className="relative">
              <div className="text-6xl font-serif text-caramel/20 mb-4">02</div>
              <h3 className="font-serif text-xl text-charcoal mb-2">選擇模式</h3>
              <p className="text-sm text-charcoal/60">分食合菜或個人定食，選擇最適合的用餐方式</p>
            </div>

            {/* Step 3 */}
            <div className="relative">
              <div className="text-6xl font-serif text-caramel/20 mb-4">03</div>
              <h3 className="font-serif text-xl text-charcoal mb-2">設定偏好</h3>
              <p className="text-sm text-charcoal/60">告訴我們人數、場合與飲食限制</p>
            </div>

            {/* Step 4 */}
            <div className="relative">
              <div className="text-6xl font-serif text-caramel/20 mb-4">04</div>
              <h3 className="font-serif text-xl text-charcoal mb-2">獲得推薦</h3>
              <p className="text-sm text-charcoal/60">AI 分析完成，為您呈現完美菜單</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonial Section */}
      <section className="py-16 md:py-24 bg-charcoal text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex justify-center gap-1 mb-6">
            {[...Array(5)].map((_, i) => (
              <Star key={i} className="w-5 h-5 fill-caramel text-caramel" />
            ))}
          </div>
          <blockquote className="font-serif text-2xl md:text-3xl leading-relaxed text-balance">
            「以前帶客戶吃飯總是很緊張，現在有 Carte AI， 每次都能完美掌握菜色搭配，賓主盡歡！」
          </blockquote>
          <div className="mt-8">
            <p className="font-medium">陳先生</p>
            <p className="text-sm text-white/60">科技公司業務總監</p>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-16 md:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="p-8 md:p-12 bg-white rounded-[2rem] shadow-floating">
            <ChefHat className="w-16 h-16 text-caramel mx-auto mb-6" />
            <h2 className="font-serif text-3xl md:text-4xl text-charcoal mb-4">準備好享受美食了嗎？</h2>
            <p className="text-charcoal/60 mb-8 max-w-xl mx-auto">讓 AI 為您規劃下一頓完美的餐點</p>
            <Link
              href="/input"
              className="inline-flex items-center justify-center gap-2 px-10 py-4 text-lg font-semibold text-white rounded-full gradient-primary shadow-lg hover:shadow-xl hover:scale-105 transition-all"
            >
              開始體驗
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}
