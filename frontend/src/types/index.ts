// ==================== API 回應類型 ====================

export interface MenuItem {
  dish_id: string | null;
  dish_name: string;
  dish_name_local?: string;
  price: number;
  quantity: number;
  category: string;
  reason: string;
  review_count?: number;
  price_estimated?: boolean;
}

export interface DishSlotResponse {
  category: string;
  display: MenuItem;
  alternatives: MenuItem[];
}

export interface RecommendationResponse {
  recommendation_id: string;
  restaurant_name: string;
  cuisine_type: string;
  total_price: number;
  per_person: number;
  items: DishSlotResponse[];
  category_summary: Record<string, number>;
}

// ==================== 前端狀態類型 ====================

export type DishStatus = 'pending' | 'selected';

export interface DishSlot {
  category: string;
  display: MenuItem;
  alternatives: MenuItem[];
  replacedDishes: string[];  // 已換掉的菜名
  status: DishStatus;
}

export interface UserInput {
  restaurant_name: string;
  people_count: number;
  budget_per_person: number;
  dining_mode: 'sharing' | 'individual';
  dietary_restrictions: string[];
  preferences: string;
}

// ==================== UI 狀態類型 ====================

export interface PriceDiff {
  amount: number;
  timestamp: number;
}

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}