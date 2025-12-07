"use client"

import { useState } from "react"
import { Search, MapPin, Star } from "lucide-react"

interface Restaurant {
  id: string
  name: string
  type: string
  rating: number
  priceLevel: string
  distance: string
  address: string
}

interface StepRestaurantProps {
  value: Restaurant | null
  onChange: (restaurant: Restaurant) => void
}

// Mock search results
const mockResults: Restaurant[] = [
  {
    id: "1",
    name: "鼎泰豐 (信義店)",
    type: "台式料理 · 小籠包",
    rating: 4.6,
    priceLevel: "$$$",
    distance: "0.5 km",
    address: "台北市信義區市府路45號",
  },
  {
    id: "2",
    name: "欣葉台菜創始店",
    type: "台菜 · 傳統料理",
    rating: 4.4,
    priceLevel: "$$",
    distance: "1.2 km",
    address: "台北市中山區雙城街34-1號",
  },
  {
    id: "3",
    name: "RAW",
    type: "法式料理 · 創意料理",
    rating: 4.8,
    priceLevel: "$$$$",
    distance: "2.1 km",
    address: "台北市中山區樂群三路301號",
  },
]

export function StepRestaurant({ value, onChange }: StepRestaurantProps) {
  const [query, setQuery] = useState("")
  const [showResults, setShowResults] = useState(false)
  const [results, setResults] = useState<Restaurant[]>([])

  const handleSearch = (searchQuery: string) => {
    setQuery(searchQuery)
    if (searchQuery.length > 0) {
      setResults(mockResults.filter((r) => r.name.toLowerCase().includes(searchQuery.toLowerCase())))
      setShowResults(true)
    } else {
      setResults([])
      setShowResults(false)
    }
  }

  const handleSelect = (restaurant: Restaurant) => {
    onChange(restaurant)
    setQuery(restaurant.name)
    setShowResults(false)
  }

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="text-center">
        <h2 className="font-serif text-2xl md:text-3xl text-charcoal mb-2">今天想去哪裡用餐？</h2>
        <p className="text-charcoal/60">搜尋餐廳名稱，我們會分析菜單與評論</p>
      </div>

      {/* Search Box */}
      <div className="relative">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-charcoal/40" />
          <input
            type="text"
            value={query}
            onChange={(e) => handleSearch(e.target.value)}
            onFocus={() => query && setShowResults(true)}
            placeholder="輸入餐廳名稱..."
            className="w-full pl-12 pr-4 py-4 text-lg bg-white border-2 border-charcoal/10 rounded-2xl
              focus:border-caramel focus:ring-4 focus:ring-caramel/10 outline-none
              transition-all placeholder:text-charcoal/30"
          />
        </div>

        {/* Search Results Dropdown */}
        {showResults && results.length > 0 && (
          <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-xl border border-charcoal/5 overflow-hidden z-20">
            {results.map((restaurant) => (
              <button
                key={restaurant.id}
                onClick={() => handleSelect(restaurant)}
                className={`
                  w-full p-4 text-left flex items-start gap-4
                  hover:bg-cream transition-colors
                  ${value?.id === restaurant.id ? "bg-cream" : ""}
                `}
              >
                {/* Restaurant Image Placeholder */}
                <div className="w-16 h-16 bg-charcoal/5 rounded-xl flex-shrink-0 flex items-center justify-center">
                  <MapPin className="w-6 h-6 text-charcoal/20" />
                </div>

                {/* Restaurant Info */}
                <div className="flex-1 min-w-0">
                  <h4 className="font-medium text-charcoal truncate">{restaurant.name}</h4>
                  <p className="text-sm text-charcoal/60 mt-0.5">{restaurant.type}</p>
                  <div className="flex items-center gap-3 mt-2 text-xs text-charcoal/50">
                    <span className="flex items-center gap-1">
                      <Star className="w-3 h-3 fill-caramel text-caramel" />
                      {restaurant.rating}
                    </span>
                    <span>{restaurant.priceLevel}</span>
                    <span>{restaurant.distance}</span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Selected Restaurant Card */}
      {value && !showResults && (
        <div className="p-4 bg-caramel/5 border-2 border-caramel/20 rounded-2xl">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 bg-caramel/10 rounded-xl flex-shrink-0 flex items-center justify-center">
              <MapPin className="w-6 h-6 text-caramel" />
            </div>
            <div className="flex-1">
              <h4 className="font-medium text-charcoal">{value.name}</h4>
              <p className="text-sm text-charcoal/60 mt-0.5">{value.type}</p>
              <div className="flex items-center gap-3 mt-2 text-xs text-charcoal/50">
                <span className="flex items-center gap-1">
                  <Star className="w-3 h-3 fill-caramel text-caramel" />
                  {value.rating}
                </span>
                <span>{value.priceLevel}</span>
              </div>
            </div>
            <button
              onClick={() => {
                onChange(null as unknown as Restaurant)
                setQuery("")
              }}
              className="text-sm text-terracotta hover:text-terracotta/80 transition-colors"
            >
              更換
            </button>
          </div>
        </div>
      )}

      {/* Recent Searches (placeholder) */}
      {!value && !showResults && (
        <div className="pt-4">
          <p className="text-xs text-charcoal/40 uppercase tracking-wider mb-3">熱門搜尋</p>
          <div className="flex flex-wrap gap-2">
            {["鼎泰豐", "欣葉", "RAW", "教父牛排"].map((name) => (
              <button
                key={name}
                onClick={() => handleSearch(name)}
                className="px-4 py-2 text-sm text-charcoal/70 bg-white border border-charcoal/10 rounded-full
                  hover:border-caramel/50 hover:bg-caramel/5 transition-all"
              >
                {name}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
