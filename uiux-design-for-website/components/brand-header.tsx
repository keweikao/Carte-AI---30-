export function BrandHeader() {
  return (
    <div className="space-y-6">
      {/* Logo & Brand */}
      <div>
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl text-foreground">Carte</h1>
        <p className="mt-2 text-lg text-muted-foreground">你的個人美食指南</p>
      </div>

      {/* Main Value Proposition */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold text-foreground">智慧推薦，品味生活</h2>
        <p className="text-base text-muted-foreground leading-relaxed">
          AI 分析你的用餐習慣，推薦符合你味蕾的餐廳和菜色。省時、省心、更省力。
        </p>
      </div>

      {/* Key Benefits - Quick highlights */}
      <ul className="space-y-2 pt-4">
        <li className="flex items-center gap-3 text-sm">
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-primary/20 text-primary">
            ✓
          </span>
          <span className="text-foreground">個性化推薦引擎</span>
        </li>
        <li className="flex items-center gap-3 text-sm">
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-primary/20 text-primary">
            ✓
          </span>
          <span className="text-foreground">實時用餐評分</span>
        </li>
        <li className="flex items-center gap-3 text-sm">
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-primary/20 text-primary">
            ✓
          </span>
          <span className="text-foreground">社群美食發現</span>
        </li>
      </ul>
    </div>
  )
}
