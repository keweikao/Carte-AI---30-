import { Sparkles } from "lucide-react";
import Image from "next/image";

export function BrandHeader() {
  return (
    <div className="space-y-6">
      {/* Brand Icon + Name */}
      <div className="flex items-center gap-3">
        <div className="w-14 h-14 flex items-center justify-center">
          <Image
            src="/icon_small.png"
            alt="Carte AI Logo"
            width={56}
            height={56}
            className="w-14 h-14 object-contain"
            priority
          />
        </div>
        <div>
          <h1 className="text-4xl font-bold text-foreground">Carte AI 點餐助手</h1>
          <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
            <Sparkles className="w-3.5 h-3.5 text-primary" />
            <span>AI 驅動的用餐助手</span>
          </div>
        </div>
      </div>

      {/* Value Proposition */}
      <div className="space-y-3">
        <h2 className="text-2xl sm:text-3xl font-bold text-foreground leading-tight">
          一個人的美食探險<br className="hidden sm:inline" /><span className="sm:hidden"> </span>
          <span className="text-primary">一群人的完美饗宴</span>
        </h2>
        <p className="text-base sm:text-lg text-muted-foreground leading-relaxed">
          結合 Google Maps 真實評論與 AI 智慧分析。<br className="hidden sm:inline" /><span className="sm:hidden"> </span>
          無論是想獨自嚐鮮，還是聚餐不知道怎麼點，<br className="hidden sm:inline" /><span className="sm:hidden"> </span>
          Carte AI 點餐助手 都能為你量身打造最佳菜單。
        </p>
      </div>
    </div>
  );
}
