#!/usr/bin/env python3
"""
刪除 Firestore 中的忠南飯館快取
"""

from google.cloud import firestore

# 忠南飯館的 Place ID
PLACE_ID = "ChIJvfRr2NWrQjQRZSTAyJ3KtLE"

print("=" * 80)
print("🗑️  刪除 Firestore 快取")
print("=" * 80)

try:
    # 初始化 Firestore
    db = firestore.Client(project="gen-lang-client-0415289079", database="carted-data")
    
    # 刪除文件
    doc_ref = db.collection("restaurants").document(PLACE_ID)
    
    # 檢查是否存在
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        name = data.get('name', 'Unknown')
        print(f"\n📍 找到快取資料:")
        print(f"   Place ID: {PLACE_ID}")
        print(f"   餐廳名稱: {name}")
        print(f"   更新時間: {data.get('updated_at', 'N/A')}")
        
        # 刪除
        doc_ref.delete()
        print(f"\n✅ 已刪除快取")
    else:
        print(f"\n⚠️  快取不存在（可能已經刪除）")
        print(f"   Place ID: {PLACE_ID}")
    
    print("\n" + "=" * 80)
    print("✅ 完成！現在可以重新測試了")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
