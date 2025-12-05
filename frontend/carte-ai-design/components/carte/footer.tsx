import Link from "next/link"

export function Footer() {
  return (
    <footer className="bg-charcoal text-white py-12 md:py-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 md:gap-12">
          {/* Brand */}
          <div className="md:col-span-2">
            <Link href="/" className="inline-block">
              <span className="font-serif text-3xl tracking-tight">Carte</span>
              <span className="ml-2 text-xs font-medium text-caramel bg-caramel/20 px-2 py-0.5 rounded-full">AI</span>
            </Link>
            <p className="mt-4 text-white/60 text-sm leading-relaxed max-w-md">
              AI 驅動的智慧點餐助手，為您分析菜單、閱讀評論， 推薦最適合您的美味佳餚。
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white/40 mb-4">快速連結</h4>
            <ul className="space-y-3">
              <li>
                <Link href="/input" className="text-sm text-white/70 hover:text-white transition-colors">
                  開始使用
                </Link>
              </li>
              <li>
                <Link href="#features" className="text-sm text-white/70 hover:text-white transition-colors">
                  功能介紹
                </Link>
              </li>
              <li>
                <Link href="#how-it-works" className="text-sm text-white/70 hover:text-white transition-colors">
                  使用方式
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white/40 mb-4">法律資訊</h4>
            <ul className="space-y-3">
              <li>
                <Link href="/privacy" className="text-sm text-white/70 hover:text-white transition-colors">
                  隱私政策
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-sm text-white/70 hover:text-white transition-colors">
                  服務條款
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs text-white/40">© {new Date().getFullYear()} Carte AI. All rights reserved.</p>
          <p className="text-xs text-white/40">Made with care for food lovers</p>
        </div>
      </div>
    </footer>
  )
}
