import Header from "@/components/header"
import RestaurantCard from "@/components/restaurant-card"
import { Button } from "@/components/ui/button"

export default function DiscoverPage() {
  const restaurants = [
    {
      id: 1,
      name: "海底撈",
      rating: 4.8,
      ratingCount: 128,
      price: 860,
      perPerson: "人均 NTS 430",
      cuisine: "火鍋",
      description: "海底撈精緻用餐體驗...",
      tags: ["火鍋", "頂級服務", "家庭友善"],
    },
    {
      id: 2,
      name: "四宮格鍋底（番茄清湯組合）",
      rating: 4.8,
      ratingCount: 128,
      price: 150,
      cuisine: "火鍋組合",
    },
    {
      id: 3,
      name: "撥派清牛肉（半份）",
      rating: 4.8,
      ratingCount: 128,
      price: 190,
      cuisine: "牛肉",
    },
  ]

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header title="推薦餐廳" />

      <main className="flex-1 p-6 max-w-4xl mx-auto w-full">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-foreground mb-2 text-balance">為你精選的餐廳</h1>
            <p className="text-muted-foreground text-lg">根據你的偏好和預算推薦</p>
          </div>
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90">新增偏好</Button>
        </div>

        <div className="space-y-4">
          {restaurants.map((restaurant) => (
            <RestaurantCard key={restaurant.id} {...restaurant} />
          ))}
        </div>

        <div className="mt-8 p-4 bg-accent/10 border border-accent/20 rounded-lg">
          <Button className="w-full bg-primary text-primary-foreground hover:bg-primary/90 py-6 text-lg">
            完成餐廳點餐
          </Button>
        </div>
      </main>
    </div>
  )
}
