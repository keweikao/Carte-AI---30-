"""
測試 Agent 進度推送功能
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas.recommendation import UserInputV2, BudgetV2
from main import process_recommendation_async
from services.firestore_service import get_job_status
import uuid

async def test_progress_tracking():
    """測試進度追蹤功能"""
    print("=" * 60)
    print("測試 Agent 進度追蹤")
    print("=" * 60)
    
    # 建立測試請求
    job_id = str(uuid.uuid4())
    print(f"\n📋 Job ID: {job_id}")
    
    request = UserInputV2(
        restaurant_name="鼎泰豐",
        place_id="ChIJtest123",
        party_size=4,
        dining_style="Shared",
        budget=BudgetV2(type="Total", amount=2000),
        preferences=["不吃牛"],
        language="繁體中文"
    )
    
    print(f"📍 餐廳: {request.restaurant_name}")
    print(f"👥 人數: {request.party_size}")
    print(f"💰 預算: NT$ {request.budget.amount}")
    
    # 啟動非同步任務
    print("\n🚀 啟動推薦任務...")
    task = asyncio.create_task(
        process_recommendation_async(job_id, request, "mock_token")
    )
    
    # Polling 監控進度
    print("\n📊 監控進度:")
    print("-" * 60)
    
    last_agent = None
    while True:
        await asyncio.sleep(1)
        
        status = get_job_status(job_id)
        if not status:
            print("⚠️  無法取得狀態")
            continue
        
        current_status = status.get("status")
        current_agent = status.get("current_agent")
        current_step = status.get("current_step")
        total_steps = status.get("total_steps")
        logs = status.get("logs", [])
        
        # 如果 Agent 切換了，顯示新的 Agent
        if current_agent and current_agent != last_agent:
            print(f"\n🤖 {current_agent} (步驟 {current_step}/{total_steps})")
            for log in logs:
                print(f"   📝 {log}")
            last_agent = current_agent
        
        # 檢查是否完成
        if current_status == "completed":
            print("\n" + "=" * 60)
            print("✅ 推薦生成完成！")
            result = status.get("result")
            if result:
                print(f"📊 推薦了 {len(result.get('items', []))} 道菜")
                print(f"💰 總價: NT$ {result.get('total_price', 0)}")
            break
        
        elif current_status == "failed":
            print("\n" + "=" * 60)
            print("❌ 推薦生成失敗")
            print(f"錯誤: {status.get('error')}")
            break
    
    # 等待任務完成
    try:
        await task
    except Exception as e:
        print(f"\n⚠️  任務執行錯誤: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_progress_tracking())
