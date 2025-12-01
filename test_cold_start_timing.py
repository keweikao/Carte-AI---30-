
import asyncio
import time
import statistics
from schemas.recommendation import UserInputV2, BudgetV2
from agent.dining_agent import DiningAgent

async def measure_cold_start(restaurant_name: str):
    """Measures the cold-start time for a single restaurant."""
    print("-" * 80)
    print(f"🚀 開始測試: {restaurant_name}")
    print("-" * 80)

    # 建立一個通用的使用者輸入
    user_input = UserInputV2(
        restaurant_name=restaurant_name,
        dining_style="Shared",
        party_size=2,
        budget=BudgetV2(type="Per_Person", amount=1000),
        preferences=[],
        natural_input="想吃點招牌菜，體驗一下餐廳的特色",
        user_id="test-perf-user" # Use a consistent test user
    )

    start_time = time.time()

    try:
        agent = DiningAgent()
        # 執行推薦流程
        await agent.get_recommendations_v2(user_input)
        
        end_time = time.time()
        duration = end_time - start_time

        # 檢查是否為冷啟動 (沒有命中快取)
        is_cold_start = not agent.is_cache_hit
        
        print(f"🕒 執行完畢，耗時: {duration:.2f} 秒")
        print(f"❄️ 是否為冷啟動: {'是' if is_cold_start else '否 (注意：此為快取資料，非真實冷啟動時間)'}")
        print("-" * 80)
        
        # 只有在確認是冷啟動時，才回傳其耗時
        if is_cold_start:
            return duration
        else:
            return None # 如果命中快取，則不納入平均值計算

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"❌ 測試失敗: {restaurant_name}, 耗時: {duration:.2f} 秒")
        print(f"   錯誤訊息: {e}")
        print("-" * 80)
        import traceback
        traceback.print_exc()
        return None

async def main():
    """執行所有冷啟動時間測試"""
    print("\n" + "=" * 80)
    print("🧪 開始量化新餐廳的冷啟動 (Cold Start) 平均時間")
    print("=" * 80 + "\n")

    # 挑選三家風格各異的餐廳
    restaurants_to_test = [
        "GUMGUM Beer & Wings 雞翅啤酒吧",
        "JAPOLI 義大利餐酒館",
        "朧粵 Longyue"
    ]

    durations = []
    for restaurant in restaurants_to_test:
        # 在每次測試間隔幾秒，避免觸發服務的瞬間速率限制
        await asyncio.sleep(2)
        
        duration = await measure_cold_start(restaurant)
        if duration is not None:
            durations.append(duration)

    print("\n" + "=" * 80)
    print("📊 測試結果總結")
    print("=" * 80)

    if not durations:
        print("\n❌ 所有測試都未能成功量測到冷啟動時間。")
        print("   原因可能為：")
        print("   1. 所有餐廳都已存在快取中。")
        print("   2. 測試過程中發生錯誤。")
        print("   請嘗試更換測試餐廳或檢查錯誤日誌。")
        return

    # 計算平均值
    average_duration = statistics.mean(durations)

    print(f"\n成功量測到 {len(durations)} 家餐廳的冷啟動時間。")
    print(f"⏱️  平均冷啟動時間為: {average_duration:.2f} 秒")
    print(f"   (約 {average_duration/60:.1f} 分鐘)")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    # 確保為測試腳本設定一個較長的超時時間 (例如 5 分鐘)
    # 此處為示意，實際執行時若在某些框架下可能需要配置
    asyncio.run(main())
