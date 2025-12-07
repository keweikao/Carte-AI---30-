import { Star } from "lucide-react"
import { Button } from "@/components/ui/button"

interface RestaurantCardProps {
  id: number
  name: string
  rating: number
  ratingCount: number
  price: number
  perPerson?: string
  cuisine: string
  description?: string
  tags?: string[]
}

export default function RestaurantCard({
  id,
  name,
  rating,
  ratingCount,
  price,
  perPerson,
  cuisine,
  description,
  tags,
}: RestaurantCardProps) {
  return (
    <div className="rounded-lg border border-border bg-card p-6 hover:border-primary/30 hover:shadow-lg transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-foreground mb-1">{name}</h3>
          <div className="flex items-center gap-2 mb-2">
            <Star className="w-4 h-4 fill-primary text-primary" />
            <span className="font-medium text-foreground">{rating}</span>
            <span className="text-sm text-muted-foreground">{ratingCount}評</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-primary">NTS {price}</div>
          {perPerson && <p className="text-sm text-muted-foreground">{perPerson}</p>}
        </div>
      </div>

      {description && <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{description}</p>}

      {tags && tags.length > 0 && (
        <div className="flex gap-2 mb-4 flex-wrap">
          {tags.map((tag) => (
            <span key={tag} className="px-3 py-1 bg-secondary text-secondary-foreground text-xs rounded-full">
              {tag}
            </span>
          ))}
        </div>
      )}

      <Button variant="outline" className="w-full border-primary/20 text-primary hover:bg-primary/10 bg-transparent">
        查看菜色
      </Button>
    </div>
  )
}
