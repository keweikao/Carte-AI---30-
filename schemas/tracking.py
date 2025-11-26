from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ----- Swap Tracking Schemas -----

class DishSnapshot(BaseModel):
    """單一菜品的快照資料"""
    dish_name: str = Field(..., description="菜品名稱")
    category: str = Field(..., description="菜品類別（如：冷菜、熱菜、刺身、壽司）")
    price: int = Field(..., description="菜品價格")
    reason: Optional[str] = Field(None, description="推薦理由")

class SwapRequest(BaseModel):
    """換菜請求"""
    recommendation_id: str = Field(..., description="推薦 ID")
    original_dish: DishSnapshot = Field(..., description="原始菜品")
    new_dish: DishSnapshot = Field(..., description="替換後的菜品")
    timestamp: Optional[datetime] = Field(None, description="換菜時間（自動記錄）")

class SwapResponse(BaseModel):
    """換菜回應"""
    status: str = Field("success", description="狀態")
    message: str = Field(..., description="回應訊息")
    swap_count: int = Field(..., description="本次推薦的總換菜次數")

# ----- Finalize Tracking Schemas -----

class FinalSelectionItem(BaseModel):
    """最終選擇的菜品"""
    dish_name: str = Field(..., description="菜品名稱")
    category: str = Field(..., description="菜品類別")
    price: int = Field(..., description="菜品價格")
    was_swapped: bool = Field(False, description="是否曾被換過")
    swap_count: int = Field(0, description="被換過的次數")

class FinalizeRequest(BaseModel):
    """點餐完成請求"""
    recommendation_id: str = Field(..., description="推薦 ID")
    final_selections: List[FinalSelectionItem] = Field(..., description="最終選擇的菜品列表")
    total_price: int = Field(..., description="最終總價")
    session_duration_seconds: Optional[int] = Field(None, description="點餐流程時長（秒）")

class FinalizeResponse(BaseModel):
    """點餐完成回應"""
    status: str = Field("success", description="狀態")
    message: str = Field(..., description="回應訊息")
    order_id: str = Field(..., description="訂單 ID")
    summary: dict = Field(..., description="訂單摘要")

# ----- Session Data Structure (for internal use) -----

class RecommendationSession(BaseModel):
    """推薦 session 的完整記錄（內部使用）"""
    recommendation_id: str
    user_id: str
    restaurant_name: str
    restaurant_cuisine_type: str

    # 使用者輸入
    user_input: dict  # UserInputV2 serialized

    # 系統建議
    initial_recommendations: List[dict]  # List of MenuItemV2 serialized
    initial_total_price: int

    # 互動歷史
    swap_history: List[dict] = Field(default_factory=list)  # List of SwapRequest serialized

    # 最終結果
    final_selections: Optional[List[dict]] = None  # List of FinalSelectionItem serialized
    final_total_price: Optional[int] = None

    # 元資料
    created_at: datetime
    finalized_at: Optional[datetime] = None
    session_duration_seconds: Optional[int] = None
    total_swap_count: int = 0

    # 統計
    category_adherence: Optional[dict] = None  # 類別遵循度統計
    budget_adherence: Optional[float] = None  # 預算遵循度（0-1）
