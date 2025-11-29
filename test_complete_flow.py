"""
完整流程測試：Prefetch → Agent Progress → Recommendation

測試流程：
1. 觸發 prefetch (模擬使用者選擇餐廳)
2. 等待 prefetch 完成
3. 啟動推薦任務 (使用 async job)
4. 監控 Agent 進度推送
5. 驗證最終推薦結果
"""
import asyncio
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas.recommendation import UserInputV2, BudgetV2
from main import process_recommendation_async
from services.firestore_service import get_job_status
from agent.profile_agent import RestaurantProfileAgent
import uuid

async def test_complete_flow():
    """測試完整流程"""
    print("=" * 80)
    print("🧪 完整流程測試：Prefetch → Agent Progress → Recommendation")
    print("=" * 80)
    
    restaurant_name = "鼎泰豐"
    place_id = "ChIJtest123"
    
    # ========================================
    # Phase 1: Prefetch (模擬使用者選擇餐廳)
    # ========================================
    print("\n" + "─" * 80)
    print("📍 Phase 1: Prefetch Restaurant Data")
    print("─" * 80)
    print(f"🏪 餐廳: {restaurant_name}")
    print(f"📌 Place ID: {place_id}")
    
    profiler = RestaurantProfileAgent()
    
    print("\n🚀 啟動 Prefetch...")
    prefetch_start = time.time()
    
    try:
        # 執行 prefetch
        profile = await profiler.analyze(restaurant_name, place_id)
        prefetch_duration = time.time() - prefetch_start
        
        print(f"✅ Prefetch 完成！耗時: {prefetch_duration:.2f} 秒")
        print(f"📊 分析結果:")
        print(f"   - 驗證菜品數: {len(profile.get('verified_items', []))}")
        print(f"   - 資料來源: {', '.join(profile.get('data_sources', []))}")
        
    except Exception as e:
        print(f"❌ Prefetch 失敗: {e}")
        return
    
    # ========================================
    # Phase 2: 模擬使用者填寫偏好
    # ========================================
    print("\n" + "─" * 80)
    print("👤 Phase 2: User Fills Preferences")
    print("─" * 80)
    print("⏱️  模擬使用者填寫表單... (等待 2 秒)")
    await asyncio.sleep(2)
    print("✅ 使用者完成表單填寫")
    
    # ========================================
    # Phase 3: 啟動推薦任務 (Async Job)
    # ========================================
    print("\n" + "─" * 80)
    print("🤖 Phase 3: Start Recommendation Job")
    print("─" * 80)
    
    job_id = str(uuid.uuid4())
    print(f"📋 Job ID: {job_id}")
    
    request = UserInputV2(
        restaurant_name=restaurant_name,
        place_id=place_id,
        party_size=4,
        dining_style="Shared",
        budget=BudgetV2(type="Total", amount=2000),
        preferences=["不吃牛"],
        language="繁體中文"
    )
    
    print(f"👥 人數: {request.party_size}")
    print(f"💰 預算: NT$ {request.budget.amount}")
    print(f"🚫 限制: {', '.join(request.preferences)}")
    
    # 啟動非同步任務
    print("\n🚀 啟動推薦任務...")
    task = asyncio.create_task(
        process_recommendation_async(job_id, request, "mock_token")
    )
    
    # ========================================
    # Phase 4: 監控 Agent 進度 (模擬前端 Polling)
    # ========================================
    print("\n" + "─" * 80)
    print("📊 Phase 4: Monitor Agent Progress (Frontend Polling)")
    print("─" * 80)
    
    last_agent = None
    agent_timings = {}
    job_start = time.time()
    
    while True:
        await asyncio.sleep(1)  # 每秒 Polling (模擬前端)
        
        status = get_job_status(job_id)
        if not status:
            print("⚠️  無法取得狀態")
            continue
        
        current_status = status.get("status")
        current_agent = status.get("current_agent")
        current_step = status.get("current_step")
        total_steps = status.get("total_steps")
        logs = status.get("logs", [])
        
        # Agent 切換時顯示
        if current_agent and current_agent != last_agent:
            if last_agent:
                # 記錄上一個 Agent 的耗時
                agent_timings[last_agent] = time.time() - agent_timings.get(f"{last_agent}_start", job_start)
            
            # 記錄新 Agent 開始時間
            agent_timings[f"{current_agent}_start"] = time.time()
            
            print(f"\n{'🎯' if current_step == 1 else '⏭️ '} Agent 切換: {current_agent}")
            print(f"   進度: {current_step}/{total_steps}")
            print(f"   Logs:")
            for log in logs:
                print(f"      📝 {log}")
            
            last_agent = current_agent
        
        # 檢查完成狀態
        if current_status == "completed":
            if last_agent:
                agent_timings[last_agent] = time.time() - agent_timings.get(f"{last_agent}_start", job_start)
            
            total_duration = time.time() - job_start
            
            print("\n" + "=" * 80)
            print("✅ 推薦生成完成！")
            print("=" * 80)
            
            result = status.get("result")
            if result:
                print(f"\n📊 推薦結果:")
                print(f"   - 推薦菜品數: {len(result.get('items', []))}")
                print(f"   - 總價: NT$ {result.get('total_price', 0)}")
                print(f"   - 餐廳: {result.get('restaurant_name', '')}")
                
                print(f"\n⏱️  時間統計:")
                print(f"   - Prefetch: {prefetch_duration:.2f} 秒")
                print(f"   - 推薦生成: {total_duration:.2f} 秒")
                print(f"   - 總耗時: {prefetch_duration + total_duration:.2f} 秒")
                
                print(f"\n🤖 Agent 耗時:")
                for agent, duration in agent_timings.items():
                    if not agent.endswith("_start"):
                        print(f"   - {agent}: {duration:.2f} 秒")
                
                # 顯示推薦菜品
                print(f"\n🍽️  推薦菜單:")
                for idx, item in enumerate(result.get('items', [])[:5], 1):
                    dish = item.get('display', {})
                    print(f"   {idx}. {dish.get('dish_name')} - NT$ {dish.get('price')}")
                    print(f"      理由: {dish.get('reason', '')[:50]}...")
            
            break
        
        elif current_status == "failed":
            print("\n" + "=" * 80)
            print("❌ 推薦生成失敗")
            print("=" * 80)
            print(f"錯誤: {status.get('error')}")
            break
    
    # 等待任務完成
    try:
        await task
    except Exception as e:
        print(f"\n⚠️  任務執行錯誤: {e}")
    
    # ========================================
    # Phase 5: 驗證 Cache Hit
    # ========================================
    print("\n" + "─" * 80)
    print("🔍 Phase 5: Verify Cache Hit")
    print("─" * 80)
    
    print("🔄 再次請求相同餐廳...")
    second_start = time.time()
    
    try:
        profile2 = await profiler.analyze(restaurant_name, place_id)
        second_duration = time.time() - second_start
        
        print(f"✅ 第二次請求完成！耗時: {second_duration:.2f} 秒")
        
        if second_duration < 1.0:
            print(f"🎉 Cache Hit! 速度提升 {(prefetch_duration / second_duration):.1f}x")
        else:
            print(f"⚠️  可能沒有命中快取")
        
    except Exception as e:
        print(f"❌ 第二次請求失敗: {e}")
    
    print("\n" + "=" * 80)
    print("🏁 測試完成")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_complete_flow())
