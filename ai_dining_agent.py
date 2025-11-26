import json
import re
from typing import List, Dict, Any
from token_optimizer_minimal import TokenOptimizer
from api_cache_minimal import APICache

class DiningAgent:
    def __init__(self, restaurant_name: str, total_budget: float, mode: str, tags: List[str], note: str):
        self.restaurant_name = restaurant_name
        self.total_budget = total_budget
        self.mode = mode
        self.tags = tags
        self.note = note
        self.search_results = []
        self.signature_candidates = []
        self.recommendations = []
        self.constraints_applied = []
        self.total_estimated_cost = 0.0

        # 初始化 Token 優化器（極簡版）
        self.token_optimizer = TokenOptimizer(
            threshold=1000,
            cache_dir="temp/agent_outputs"
        )

        # 初始化 API 快取系統（策略 1）
        self.api_cache = APICache(
            cache_dir="temp/api_cache",
            default_ttl_hours=1  # 餐廳資料快取 1 小時
        )

    def run(self) -> Dict[str, Any]:
        # 1. 資料獲取
        self._search_restaurant_info()
        
        # 2. 提取招牌菜
        # 注意：這裡的 _extract_signature_dishes 應該接收原始搜尋結果，並從中解析
        # 但由於目前 _search_restaurant_info 返回的是模擬結果，這裡也將使用模擬的菜色列表
        # 在實際應用中，這裡會解析 self.search_results
        self._extract_signature_dishes(self.search_results) # 傳入模擬的搜尋結果

        # 3. 生成推薦清單 (飲食偏好處理已整合在 _generate_recommendations 內部)
        # 這裡需要一個包含所有菜色詳細資訊的列表，目前使用模擬菜單
        # _generate_recommendations 會在內部呼叫 _apply_dietary_rules
        recommendation_output = self._generate_recommendations(self.signature_candidates) # 傳入招牌候選菜色
        
        return recommendation_output

    def _search_restaurant_info(self) -> List[str]:
        queries = [
            f"{self.restaurant_name} 評論",
            f"{self.restaurant_name} 菜單 價格",
            f"{self.restaurant_name} 招牌菜"
        ]
        all_results = []
        for query in queries:
            # 這裡需要呼叫 google_web_search 工具
            # 由於直接在 Python 程式碼中呼叫工具需要特殊的處理方式
            # 我將模擬工具的行為，並將結果儲存。
            # 在實際執行時，這會被替換為真正的工具呼叫。
            # 為了示範，我將使用一個佔位符。
            # 實際的 google_web_search 會返回一個字典，其中包含 'web_search_response' 鍵
            # 該鍵的值是一個包含搜尋結果的字串。
            # 這裡我們假設它返回一個字串列表。
            # 
            # 由於我無法直接在 Python 程式碼中執行工具，我將在這裡留下一個註釋，
            # 說明這裡應該是 google_web_search 的呼叫。
            #
            # 實際的工具呼叫會像這樣：
            # search_response = default_api.google_web_search(query=query)
            # if 'web_search_response' in search_response:
            #     all_results.append(search_response['web_search_response']['output'])
            # else:
            #     all_results.append(f"搜尋 {query} 失敗或無結果。")
            
            # 為了讓程式碼可以運行，這裡先用一個模擬的結果
            # 實際使用時，這裡會是真實的 API 回應

            # 定義模擬 API 函式
            def mock_api_search(q):
                return f"模擬搜尋結果：{q} 的相關資訊。" + (" 詳細內容..." * 500)

            # 策略 1：使用 API 快取（避免重複呼叫）
            cached_result = self.api_cache.get_or_call(
                cache_key=query,
                api_function=mock_api_search,
                q=query,
                ttl_hours=1  # 餐廳資料快取 1 小時
            )

            # 策略 2：使用 Token 優化器（節省 token）
            optimized_result = self.token_optimizer.optimize(
                cached_result,
                source=f"restaurant_search_{query[:20]}"
            )
            all_results.append(optimized_result)

        self.search_results = all_results
        return all_results

    def _extract_signature_dishes(self, search_results: List[str]) -> List[str]:
        """
        從搜尋結果中提取招牌菜

        注意：search_results 可能包含優化後的檔案參考（dict 格式）
        LLM 如果看到檔案參考，會自動讀取完整內容
        """
        dish_mentions = {}

        # 為了示範，我們將模擬一些菜色名稱
        # 在實際應用中，這會從 search_results 中解析出來
        potential_dishes = [
            "麻婆豆腐", "宮保雞丁", "糖醋排骨", "清蒸魚", "蒜泥白肉",
            "炸雞", "炒飯", "烘蛋", "滷肉飯", "牛肉麵", "水煮牛肉"
        ]

        for result in search_results:
            # 處理優化後的結果（可能是 dict 或 str）
            result_text = ""

            if isinstance(result, dict) and 'file' in result:
                # 這是優化後的檔案參考
                # LLM 會看到這個並自動使用 Read 工具讀取檔案
                # 為了在 Python 中運行，我們也讀取檔案
                try:
                    with open(result['file'], 'r') as f:
                        result_text = f.read()
                except:
                    # 如果讀取失敗，使用預覽
                    result_text = result.get('preview', '')
            else:
                # 直接的文字結果
                result_text = str(result)

            # 從文字中尋找菜色
            for dish in potential_dishes:
                if dish in result_text:
                    dish_mentions[dish] = dish_mentions.get(dish, 0) + 1

        # 根據提及次數排序，取 Top 3
        sorted_dishes = sorted(dish_mentions.items(), key=lambda item: item[1], reverse=True)
        self.signature_candidates = [dish for dish, count in sorted_dishes[:3]]
        return self.signature_candidates

    def _apply_dietary_rules(self, dishes: List[Dict[str, Any]], tags: List[str]) -> List[Dict[str, Any]]:
        filtered_dishes = []
        self.constraints_applied = []

        for dish in dishes:
            keep_dish = True
            dish_name = dish.get("name", "")
            dish_tags = dish.get("tags", []) # 假設菜色有自己的標籤，例如 ['牛肉', '辣']

            # [不吃牛]
            if "不吃牛" in tags and ("牛肉" in dish_name or "牛" in dish_tags):
                keep_dish = False
                if "不吃牛" not in self.constraints_applied:
                    self.constraints_applied.append("不吃牛")

            # [不吃辣]
            if "不吃辣" in tags and ("麻辣" in dish_name or "辣" in dish_tags):
                keep_dish = False
                if "不吃辣" not in self.constraints_applied:
                    self.constraints_applied.append("不吃辣")
            
            # [海鮮過敏]
            if "海鮮過敏" in tags and any(allergen in dish_name or allergen in dish_tags for allergen in ["蝦", "蟹", "貝", "海鮮"]):
                keep_dish = False
                if "海鮮過敏" not in self.constraints_applied:
                    self.constraints_applied.append("海鮮過敏")

            # 處理其他偏好，這些偏好不直接排除菜色，而是影響推薦理由或優先級
            # [要喝酒], [有長輩], [有小孩] 會在 _generate_recommendations 中處理推薦理由

            if keep_dish:
                filtered_dishes.append(dish)
        
        return filtered_dishes

    def _generate_recommendations(self, candidate_dishes: List[Dict[str, Any]]) -> Dict[str, Any]:
        final_recommendations = []
        current_cost = 0.0
        is_over_budget = False
        
        # 為了示範，我們需要一個模擬的完整菜單，包含更多細節
        # 在實際應用中，這會從搜尋結果中解析出來
        mock_full_menu = [
            {"id": "d001", "name": "麻婆豆腐", "category": "主菜", "price_unit": 280, "tags": ["辣"]},
            {"id": "d002", "name": "宮保雞丁", "category": "主菜", "price_unit": 320, "tags": ["辣"]},
            {"id": "d003", "name": "糖醋排骨", "category": "主菜", "price_unit": 350, "tags": []},
            {"id": "d004", "name": "清蒸魚", "category": "主菜", "price_unit": 450, "tags": ["海鮮"]},
            {"id": "d005", "name": "蒜泥白肉", "category": "冷盤", "price_unit": 220, "tags": []},
            {"id": "d006", "name": "炸雞", "category": "主菜", "price_unit": 250, "tags": ["炸物"]},
            {"id": "d007", "name": "炒飯", "category": "主食", "price_unit": 180, "tags": []},
            {"id": "d008", "name": "烘蛋", "category": "蔬菜", "price_unit": 150, "tags": []},
            {"id": "d009", "name": "滷肉飯", "category": "主食", "price_unit": 80, "tags": []},
            {"id": "d010", "name": "牛肉麵", "category": "主食", "price_unit": 200, "tags": ["牛肉"]},
            {"id": "d011", "name": "水煮牛肉", "category": "主菜", "price_unit": 380, "tags": ["牛肉", "辣"]},
            {"id": "d012", "name": "可樂", "category": "飲料", "price_unit": 50, "tags": []},
            {"id": "d013", "name": "啤酒", "category": "飲料", "price_unit": 120, "tags": ["酒"]},
            {"id": "d014", "name": "涼拌海帶絲", "category": "冷盤", "price_unit": 100, "tags": []},
            {"id": "d015", "name": "季節時蔬", "category": "蔬菜", "price_unit": 160, "tags": []},
            {"id": "d016", "name": "蝦仁炒飯", "category": "主食", "price_unit": 200, "tags": ["海鮮"]},
        ]

        # 過濾掉不符合飲食偏好的菜色
        available_dishes = self._apply_dietary_rules(mock_full_menu, self.tags)
        
        # 確保至少一道招牌菜
        signature_added = False
        for sig_dish_name in self.signature_candidates:
            for dish in available_dishes:
                if dish["name"] == sig_dish_name and dish["name"] not in [r["name"] for r in final_recommendations]:
                    reason = "網友熱推招牌菜"
                    if "有長輩" in self.tags and "軟嫩" in reason: # 簡化判斷
                        reason += "，口感軟嫩適合長輩"
                    if "有小孩" in self.tags and "不辣" in reason: # 簡化判斷
                        reason += "，不辣易入口適合小孩"
                    
                    final_recommendations.append({
                        "id": dish["id"],
                        "name": dish["name"],
                        "category": dish["category"],
                        "quantity": 1,
                        "price_unit": dish["price_unit"],
                        "is_signature": True,
                        "reason": reason
                    })
                    current_cost += dish["price_unit"]
                    signature_added = True
                    break
            if signature_added:
                break
        
        # 如果沒有招牌菜符合條件，則隨機選一個符合條件的菜色作為招牌
        if not signature_added and available_dishes:
            # 這裡可以加入更智能的選擇邏輯，目前先選第一個
            dish = available_dishes[0]
            reason = "因無符合條件招牌菜，推薦此熱門菜色"
            final_recommendations.append({
                "id": dish["id"],
                "name": dish["name"],
                "category": dish["category"],
                "quantity": 1,
                "price_unit": dish["price_unit"],
                "is_signature": True,
                "reason": reason
            })
            current_cost += dish["price_unit"]

        # 根據模式添加其他菜色
        if self.mode == "sharing":
            # 分食模式：平衡 [冷盤/前菜] + [肉類/主食] + [蔬菜/澱粉] + [湯/飲料]
            categories_needed = {"冷盤": 1, "主菜": 1, "蔬菜": 1, "主食": 1, "飲料": 1}
            
            # 考慮已添加的招牌菜
            for rec in final_recommendations:
                if rec["category"] in categories_needed:
                    categories_needed[rec["category"]] -= 1
            
            for category, count in categories_needed.items():
                for _ in range(count):
                    for dish in available_dishes:
                        if dish["category"] == category and dish["name"] not in [r["name"] for r in final_recommendations]:
                            if current_cost + dish["price_unit"] <= self.total_budget * 1.1: # 允許10%誤差
                                reason = f"符合分食模式的{category}需求"
                                if "要喝酒" in self.tags and "酒" in dish.get("tags", []):
                                    reason += "，適合下酒"
                                if "有長輩" in self.tags and "軟嫩" in reason:
                                    reason += "，口感軟嫩適合長輩"
                                if "有小孩" in self.tags and "不辣" in reason:
                                    reason += "，不辣易入口適合小孩"

                                final_recommendations.append({
                                    "id": dish["id"],
                                    "name": dish["name"],
                                    "category": dish["category"],
                                    "quantity": 1,
                                    "price_unit": dish["price_unit"],
                                    "is_signature": False,
                                    "reason": reason
                                })
                                current_cost += dish["price_unit"]
                                break
            
            # 處理 [要喝酒] 偏好
            if "要喝酒" in self.tags and not any("酒" in r.get("tags", []) for r in final_recommendations):
                for dish in available_dishes:
                    if "酒" in dish.get("tags", []) and current_cost + dish["price_unit"] <= self.total_budget * 1.1:
                        final_recommendations.append({
                            "id": dish["id"],
                            "name": dish["name"],
                            "category": dish["category"],
                            "quantity": 1,
                            "price_unit": dish["price_unit"],
                            "is_signature": False,
                            "reason": "符合要喝酒偏好"
                        })
                        current_cost += dish["price_unit"]
                        break

        elif self.mode == "individual":
            # 獨享模式：主餐 + 飲品
            main_course_added = False
            drink_added = False

            # 先嘗試添加主餐
            for dish in available_dishes:
                if dish["category"] == "主菜" or dish["category"] == "主食":
                    if current_cost + dish["price_unit"] <= self.total_budget:
                        reason = "獨享模式主餐"
                        final_recommendations.append({
                            "id": dish["id"],
                            "name": dish["name"],
                            "category": dish["category"],
                            "quantity": 1,
                            "price_unit": dish["price_unit"],
                            "is_signature": False,
                            "reason": reason
                        })
                        current_cost += dish["price_unit"]
                        main_course_added = True
                        break
            
            # 再嘗試添加飲品
            for dish in available_dishes:
                if dish["category"] == "飲料":
                    if current_cost + dish["price_unit"] <= self.total_budget:
                        reason = "獨享模式飲品"
                        final_recommendations.append({
                            "id": dish["id"],
                            "name": dish["name"],
                            "category": dish["category"],
                            "quantity": 1,
                            "price_unit": dish["price_unit"],
                            "is_signature": False,
                            "reason": reason
                        })
                        current_cost += dish["price_unit"]
                        drink_added = True
                        break

        # 檢查是否超預算
        if current_cost > self.total_budget:
            is_over_budget = True
        
        self.total_estimated_cost = current_cost

        return {
            "restaurant_name": self.restaurant_name,
            "mode": self.mode,
            "budget_summary": {
                "total_budget": self.total_budget,
                "total_estimated_cost": self.total_estimated_cost,
                "is_over_budget": is_over_budget
            },
            "constraints_applied": self.constraints_applied,
            "recommendations": final_recommendations,
            "token_optimization_stats": self.get_optimization_stats(),
            "api_cache_stats": self.get_cache_stats()
        }

    def get_optimization_stats(self) -> str:
        """取得 Token 優化統計資料（極簡版）"""
        return self.token_optimizer.stats()

    def get_cache_stats(self) -> dict:
        """取得 API 快取統計"""
        return self.api_cache.get_stats()

    def print_cache_stats(self):
        """列印 API 快取統計"""
        self.api_cache.print_stats()

    def print_optimization_stats(self):
        """列印 Token 優化統計（極簡版）"""
        print(self.token_optimizer.stats())
