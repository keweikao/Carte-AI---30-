import asyncio
import json
from agent.dining_agent import DiningAgent
from schemas.recommendation import UserInputV2, BudgetV2

async def test_recommendation():
    agent = DiningAgent()
    
    request = UserInputV2(
        restaurant_name='欣葉臺菜',
        party_size=4,
        dining_style='Shared',
        budget=BudgetV2(type='Total', amount=3000),
        preferences=[],
        occasion='business',
        language='繁體中文'
    )
    
    print('🔍 正在為您推薦欣葉臺菜的商務聚餐菜單...')
    print(f'📊 條件：4人 | 總預算 3000 TWD | 商務聚餐 | 無飲食限制')
    print('-' * 60)
    
    result = await agent.get_recommendations_v2(request)
    
    print(f'\n✨ {result.recommendation_summary}')
    print(f'\n📋 推薦菜單：')
    print('-' * 60)
    
    for i, slot in enumerate(result.items, 1):
        dish = slot.display
        print(f'{i}. {dish.dish_name} (${dish.price} x {dish.quantity})')
        print(f'   分類：{dish.category}')
        print(f'   推薦理由：{dish.reason}')
        if slot.alternatives:
            alt_names = ', '.join([alt.dish_name for alt in slot.alternatives[:2]])
            print(f'   替代選項：{alt_names}')
        print()
    
    print('-' * 60)
    print(f'💰 總價：${result.total_price} TWD')
    print(f'👥 人均：${result.total_price // 4} TWD')
    print(f'🏷️  幣別：{result.currency}')

if __name__ == '__main__':
    asyncio.run(test_recommendation())
