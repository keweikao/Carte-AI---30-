#!/usr/bin/env python3
"""
驗證兩階段智能圖片處理邏輯
直接使用忠南飯館的 10 張圖片進行測試
"""

import asyncio
import os
from typing import List
from services.pipeline.intelligence import MenuParser

# 忠南飯館的 10 張圖片 (來自 Apify)
ZHONGNAN_IMAGES = [
    "https://lh3.googleusercontent.com/p/AF1QipPLDtX0c247k6RJTkEW0NVNEEXDV9GHZn4htr5-=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSxpFpCqDjX7hC587cqPVhosM4hWwfs0IttNjpQTEPUQUQQmVDje9WbaFCYhDZQO1si6L0mzhhYAzYz6NygdtgJwLLDE7MS96zzYAFAYYElf_DPKuT6PwYd_jF9t22pRB8vBVjUi=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSyeptYBFAy8z2QgRVbE3qC2T-JuB0hnclIkF-314pb0Cgdgat0Ufa5D6td46qpSAgKyhrCFp-xyJjJbRRQIlELZp410cAb_4JYa3r888E6QN_iUsRMHuRDArfv4Qcm8s6CF2eKVW9K_WAG8=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSycYPR12yioki04oV4tRza63cTCjJ358aRF-O02tiGs33JQmDF-JnXL7evkWJt31troZ53TpgBzNZ6AQG8EwdXaD5X0DwCzCZBaWGZHVdajcXI9vv3ocCwMkjZCl9qRz79OvLL8okRbBxw=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSycBWFAj8P5SUte-N9U-zd-S239ZdJHCajeZeN5PtttG6gH8PPP3i2pqpDWi7X3UQqeZGNydJy3OJ-3EoW9k26rAgBXEzR_KXlrEfPLh7j04JQIzE4qKmukgsenR7v7GkUArse6mnGWtqFG=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSx6k_5Eq5Sbkc-NQxN1DoCW7Ya_vfnJtmat80dHjrXqiPQ8poOZxqp9gAzMNNO3MCCbbyVEbwj5nylIZaNcMkNjthpYuJ-lXb3aJb-6Pn6k9fTFv2XRISwXH9UzaH0ErR54XIOH-yqd9yg=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSxKo3owmtXOYLJranCyJ8rrLTIkZFmqYYKM1Q-KR9IqjESJKRVAuLyELAPmzqn0zCC9lZUWOF1Sur98rCzZSwH3PKcz-qocd1PgKNd6BnruqkfsYVdo2m1VmIKr3U3lpI-Gf5WYGhfo-eM=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSy-NeS3cKxn8qjBJjl74GCH_LjaVPeh3iXMy8qsWiIjGuPzA6kVIXQ_q-Rp4JQcRNY8fM0ieGvFCSKImRuQooC3cpgq5kM883fo76_Ex6DG_3aNkbpe4PRrsFwjy1w7p_QLKqsT=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSxRFG0JpmQTlaJh0gto5DnM-ykseSMwHQj9j5zJUPpbfyZlA2PLmGwJTLtm02Pdj1hyAK3ad6m98ma5uMQI9RlIfrAQvwpZibYnMmnpyOGYi8KfZfTjcIQdlfbCkDERPks0z0XV5pZbjaw=w1920-h1080-k-no",
    "https://lh3.googleusercontent.com/gps-cs-s/AG0ilSxYQgx9pjw34cN_ibUFGXsxYRltHh9Ms-B0EIaGCEn-jRh3-nRT-s4kMBhMjOevAo9PtybSp5tsAvLBP1CcoGjeP1RoTFKMffQXBAwcy8sVNCcV_dDsIY-aY8HYux2IyS-QdOR1Pjbhs-MR=w1920-h1080-k-no"
]

async def verify_new_logic():
    print("=" * 80)
    print("🧪 驗證兩階段智能圖片處理邏輯")
    print("=" * 80)
    
    # 檢查 API Key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY 未設定")
        return

    parser = MenuParser()
    
    print(f"\n📸 輸入圖片: {len(ZHONGNAN_IMAGES)} 張")
    print("⏳ 開始處理...")
    
    # 執行兩階段處理
    menu_items = await parser.parse_from_images(ZHONGNAN_IMAGES)
    
    print("\n" + "=" * 80)
    print(f"📊 處理結果: 提取到 {len(menu_items)} 個菜品")
    print("=" * 80)
    
    if menu_items:
        print("\n📋 提取到的菜單:")
        for i, item in enumerate(menu_items, 1):
            print(f"{i}. {item.name} - ${item.price} ({item.category})")
            if item.description:
                print(f"   📝 {item.description}")
    else:
        print("\n⚠️  未提取到任何菜品")
        print("   可能原因: 圖片中確實沒有菜單，或 OCR 失敗")

if __name__ == "__main__":
    asyncio.run(verify_new_logic())
