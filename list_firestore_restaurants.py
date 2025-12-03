"""
列出 Firestore 中所有可用的餐廳
"""

from google.cloud import firestore

def list_restaurants():
    db = firestore.Client()
    
    print("\n" + "=" * 80)
    print("📋 Firestore 中的餐廳列表")
    print("=" * 80 + "\n")
    
    docs = db.collection('restaurant_profiles').limit(20).stream()
    
    count = 0
    for doc in docs:
        count += 1
        data = doc.to_dict()
        name = data.get('name', 'Unknown')
        place_id = doc.id
        menu_count = len(data.get('menu_items', []))
        updated_at = data.get('updated_at', 'N/A')
        
        print(f"{count}. {name}")
        print(f"   Place ID: {place_id}")
        print(f"   菜單項目: {menu_count}")
        print(f"   更新時間: {updated_at}")
        print()
    
    if count == 0:
        print("❌ Firestore 中沒有餐廳資料")
    else:
        print(f"✅ 共找到 {count} 家餐廳")
    
    print("=" * 80 + "\n")

if __name__ == "__main__":
    list_restaurants()
