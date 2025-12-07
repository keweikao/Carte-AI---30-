#!/usr/bin/env python3
"""
生成視覺化的測試摘要
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
REPORT_FILE = PROJECT_ROOT / "test_migration_report.json"

def generate_visual_summary():
    """生成視覺化測試摘要"""
    
    if not REPORT_FILE.exists():
        print("❌ 找不到測試報告,請先執行 test_migration_completeness.py")
        return
    
    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    passed = report['passed']
    failed = report['failed']
    warnings = report['warnings']
    total = passed + failed
    
    # 計算完成度
    if total > 0:
        completion = (passed / total) * 100
    else:
        completion = 0
    
    # 生成進度條
    bar_length = 50
    filled = int(bar_length * completion / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    # 輸出摘要
    print("\n" + "="*70)
    print("🎯 Carte AI 設計遷移測試摘要")
    print("="*70)
    print(f"\n完成度: {completion:.1f}%")
    print(f"[{bar}] {passed}/{total}\n")
    
    # 分類統計
    categories = {
        "設計系統": ["色彩變數", "字體變數", "陰影變數", "Google Fonts"],
        "頁面結構": ["頁面", "Landing Page", "Input Page", "Waiting Page", "Recommendation Page", "Final Menu Page"],
        "元件系統": ["元件", "Props"],
        "UI 樣式": ["Button", "卡片", "響應式"],
        "功能實作": ["導航", "React Hook"]
    }
    
    print("📊 分類統計:\n")
    
    for category, keywords in categories.items():
        category_passed = sum(1 for test, _ in report['details']['passed'] 
                            if any(kw in test for kw in keywords))
        category_failed = sum(1 for test, _ in report['details']['failed'] 
                            if any(kw in test for kw in keywords))
        category_total = category_passed + category_failed
        
        if category_total > 0:
            category_pct = (category_passed / category_total) * 100
            status = "✅" if category_pct == 100 else "⚠️"
            print(f"{status} {category:12} {category_passed:2}/{category_total:2} ({category_pct:5.1f}%)")
    
    # 失敗項目
    if failed > 0:
        print(f"\n❌ 失敗項目 ({failed}):\n")
        for test, detail in report['details']['failed']:
            print(f"  • {test}")
            if detail:
                print(f"    {detail}")
    
    # 警告項目
    if warnings > 0:
        print(f"\n⚠️  警告項目 ({warnings}):\n")
        for test, detail in report['details']['warnings']:
            print(f"  • {test}")
            if detail:
                print(f"    {detail}")
    
    # 結論
    print("\n" + "="*70)
    if completion == 100:
        print("🎉 恭喜!所有測試項目都已通過!")
    elif completion >= 90:
        print("👍 測試大部分通過,還有少數項目需要修復")
    elif completion >= 70:
        print("⚠️  測試通過率良好,但仍有改進空間")
    else:
        print("❌ 測試通過率較低,需要進行大量修復")
    print("="*70 + "\n")

if __name__ == "__main__":
    generate_visual_summary()
