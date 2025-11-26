export function FeatureShowcase() {
  const features = [
    {
      title: "智慧推薦",
      description: "根據你的口味和習慣推薦最適合的餐廳",
      icon: "🎯",
    },
    {
      title: "社群互動",
      description: "分享美食發現，加入美食愛好者社群",
      icon: "👥",
    },
    {
      title: "即時評分",
      description: "查看用餐評價，做出最佳選擇",
      icon: "⭐",
    },
  ]

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {features.map((feature, index) => (
        <div
          key={index}
          className="rounded-lg border border-border bg-card/50 p-4 backdrop-blur-sm transition-all hover:bg-card hover:border-primary/30"
        >
          <div className="mb-3 text-2xl">{feature.icon}</div>
          <h3 className="font-semibold text-foreground">{feature.title}</h3>
          <p className="mt-1 text-sm text-muted-foreground">{feature.description}</p>
        </div>
      ))}
    </div>
  )
}
