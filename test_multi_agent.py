"""
Test script for Multi-Agent Recommendation System

This script tests the Multi-Agent system independently without integrating into the main flow.
"""

import asyncio
import json
from agent.recommendation_agents import OrchestratorAgent
from schemas.recommendation import UserInputV2, BudgetV2

async def test_multi_agent_system():
    print("="*80)
    print("🧪 Testing Multi-Agent Recommendation System")
    print("="*80)
    
    # Prepare test data
    user_input = UserInputV2(
        restaurant_name='欣葉臺菜',
        party_size=4,
        dining_style='Shared',
        budget=BudgetV2(type='Total', amount=3000),
        preferences=[],
        occasion='business',
        language='繁體中文'
    )
    
    # Mock candidate pool (simulating Gemini's output)
    candidates = [
        {
            "dish_name": "招牌煎豬肝",
            "dish_name_local": "招牌煎豬肝",
            "price": 580,
            "quantity": 1,
            "category": "主菜",
            "reason": "欣葉經典招牌菜，豬肝軟嫩入味",
            "tag": "必點"
        },
        {
            "dish_name": "佛跳牆 (小份)",
            "dish_name_local": "佛跳牆",
            "price": 800,
            "quantity": 1,
            "category": "湯品",
            "reason": "高級台菜代表，用料豐富",
            "tag": "招牌"
        },
        {
            "dish_name": "干貝小魚花生",
            "dish_name_local": "干貝小魚花生",
            "price": 350,
            "quantity": 1,
            "category": "冷盤",
            "reason": "酥脆開胃，海味十足",
            "tag": "人氣"
        },
        {
            "dish_name": "地瓜稀飯",
            "dish_name_local": "地瓜稀飯",
            "price": 55,
            "quantity": 4,
            "category": "主食",
            "reason": "台菜經典配餐",
            "tag": None
        },
        {
            "dish_name": "杏仁豆腐湯",
            "dish_name_local": "杏仁豆腐湯",
            "price": 120,
            "quantity": 2,
            "category": "甜點",
            "reason": "口感特別，甜度完美",
            "tag": "人氣"
        },
        {
            "dish_name": "香烤烏魚子",
            "dish_name_local": "香烤烏魚子",
            "price": 600,
            "quantity": 1,
            "category": "開胃菜",
            "reason": "高級台菜必備開胃菜",
            "tag": "招牌"
        },
        {
            "dish_name": "三杯雞",
            "dish_name_local": "三杯雞",
            "price": 480,
            "quantity": 1,
            "category": "主菜",
            "reason": "台式經典，香氣濃郁",
            "tag": None
        },
        {
            "dish_name": "炒青菜",
            "dish_name_local": "炒青菜",
            "price": 180,
            "quantity": 1,
            "category": "蔬菜",
            "reason": "清爽解膩",
            "tag": None
        },
        {
            "dish_name": "白斬雞 (半隻)",
            "dish_name_local": "白斬雞",
            "price": 450,
            "quantity": 1,
            "category": "主菜",
            "reason": "皮Q肉嫩，沾醬美味",
            "tag": None
        },
        {
            "dish_name": "手打魷魚羹",
            "dish_name_local": "手打魷魚羹",
            "price": 280,
            "quantity": 1,
            "category": "湯品",
            "reason": "手工製作，Q彈鮮美",
            "tag": None
        },
        {
            "dish_name": "涼拌川耳",
            "dish_name_local": "涼拌川耳",
            "price": 220,
            "quantity": 1,
            "category": "冷盤",
            "reason": "爽脆開胃",
            "tag": None
        },
        {
            "dish_name": "芋頭煮米粉",
            "dish_name_local": "芋頭煮米粉",
            "price": 550,
            "quantity": 1,
            "category": "主食",
            "reason": "暖胃飽足，芋頭鬆軟",
            "tag": "人氣"
        },
        {
            "dish_name": "炸花枝丸",
            "dish_name_local": "炸花枝丸",
            "price": 400,
            "quantity": 1,
            "category": "點心",
            "reason": "外酥內嫩，花枝Q彈",
            "tag": None
        },
        {
            "dish_name": "蒜泥白肉",
            "dish_name_local": "蒜泥白肉",
            "price": 380,
            "quantity": 1,
            "category": "冷盤",
            "reason": "清爽不膩，蒜香濃郁",
            "tag": None
        },
        {
            "dish_name": "紅燒獅子頭",
            "dish_name_local": "紅燒獅子頭",
            "price": 520,
            "quantity": 1,
            "category": "主菜",
            "reason": "肉質鬆軟，湯汁濃郁",
            "tag": None
        }
    ]
    
    # Mock aggregated data (from Multi-Agent analysis)
    aggregated_data = [
        {
            "dish_name": "招牌煎豬肝",
            "status": "Must Order",
            "source": "aggregator",
            "confidence_score": 95
        },
        {
            "dish_name": "佛跳牆",
            "status": "Must Order",
            "source": "aggregator",
            "confidence_score": 90
        },
        {
            "dish_name": "干貝小魚花生",
            "status": "Hidden Gem",
            "source": "search",
            "confidence_score": 85
        }
    ]
    
    print(f"\n📊 Test Scenario:")
    print(f"   Restaurant: {user_input.restaurant_name}")
    print(f"   Party Size: {user_input.party_size}")
    print(f"   Dining Style: {user_input.dining_style}")
    print(f"   Budget: ${user_input.budget.amount} TWD")
    print(f"   Occasion: {user_input.occasion}")
    print(f"   Candidates: {len(candidates)} dishes")
    print(f"   Verified Signatures: {len(aggregated_data)} dishes")
    
    # Run Multi-Agent System
    orchestrator = OrchestratorAgent()
    
    try:
        optimized_menu = await orchestrator.run(
            user_input=user_input,
            candidates=candidates,
            aggregated_data=aggregated_data
        )
        
        # Display results
        print("\n" + "="*80)
        print("📋 Final Optimized Menu")
        print("="*80)
        
        total = 0
        for i, dish in enumerate(optimized_menu, 1):
            price = dish.get('price', 0)
            quantity = dish.get('quantity', 1)
            subtotal = price * quantity
            total += subtotal
            
            print(f"\n{i}. {dish.get('dish_name')} (${price} x {quantity} = ${subtotal})")
            print(f"   分類：{dish.get('category')}")
            print(f"   標籤：{dish.get('tag') or 'N/A'}")
            print(f"   理由：{dish.get('reason')}")
        
        print("\n" + "="*80)
        print(f"💰 Total: ${total} TWD")
        print(f"👥 Per Person: ${total // user_input.party_size} TWD")
        print(f"📊 Budget Utilization: {total / user_input.budget.amount * 100:.1f}%")
        print(f"🍽️  Dish Count: {len(optimized_menu)}")
        print("="*80)
        
        # Analysis
        print("\n📈 Analysis:")
        categories = {}
        has_signature = False
        has_vegetable = False
        
        for dish in optimized_menu:
            cat = dish.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
            if dish.get('tag') in ['必點', '招牌']:
                has_signature = True
            if '蔬菜' in cat or '青菜' in dish.get('dish_name', ''):
                has_vegetable = True
        
        print(f"   ✅ Has Signature Dish: {has_signature}")
        print(f"   ✅ Has Vegetable: {has_vegetable}")
        print(f"   📊 Category Distribution: {categories}")
        
        # Check if targets met
        budget_ok = 0.8 <= (total / user_input.budget.amount) <= 1.0
        dish_count_ok = len(optimized_menu) >= user_input.party_size + 1
        
        print(f"\n🎯 Target Achievement:")
        print(f"   {'✅' if budget_ok else '❌'} Budget 80-100%: {total / user_input.budget.amount * 100:.1f}%")
        print(f"   {'✅' if dish_count_ok else '❌'} Dish Count >= {user_input.party_size + 1}: {len(optimized_menu)}")
        print(f"   {'✅' if has_signature else '❌'} Has Signature Dish")
        print(f"   {'✅' if has_vegetable else '❌'} Has Vegetable")
        
        if all([budget_ok, dish_count_ok, has_signature, has_vegetable]):
            print("\n🎉 All targets achieved! Multi-Agent system working perfectly!")
        else:
            print("\n⚠️  Some targets not met. System needs adjustment.")
        
        return optimized_menu
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    result = asyncio.run(test_multi_agent_system())
