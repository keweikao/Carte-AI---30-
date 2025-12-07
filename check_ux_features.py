#!/usr/bin/env python3
"""
檢查 UX 改進計劃 v2 的 8 個功能實作狀態
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# 專案根目錄
PROJECT_ROOT = Path(__file__).parent
FRONTEND_ROOT = PROJECT_ROOT / "frontend"

# 功能檢查規則
FEATURES = {
    "功能 1: 登入狀態顯示": {
        "files": [
            "src/components/header.tsx",
            "src/app/layout.tsx"
        ],
        "patterns": [
            r"useSession",
            r"Avatar",
            r"DropdownMenu",
            r"signOut"
        ],
        "description": "Header 組件顯示用戶頭像和登出選單"
    },
    "功能 2: 完成後返回搜尋頁": {
        "files": [
            "src/components/rating-modal.tsx"
        ],
        "patterns": [
            r"router\.push.*\/input",
            r"useRouter"
        ],
        "description": "提交回饋後導航回 /input"
    },
    "功能 3: 讚/倒讚評分系統": {
        "files": [
            "src/app/recommendation/page.tsx"
        ],
        "patterns": [
            r"ThumbsUp|thumbs-up|👍",
            r"ThumbsDown|thumbs-down|👎",
            r"itemRatings",
            r"like.*dislike"
        ],
        "description": "讚/倒讚按鈕取代綠勾勾"
    },
    "功能 5: 返回設定按鈕": {
        "files": [
            "src/app/recommendation/page.tsx",
            "src/app/input/page.tsx"
        ],
        "patterns": [
            r"返回設定|ArrowLeft",
            r"handleBackToSettings",
            r"searchParams\.get"
        ],
        "description": "推薦頁面加入返回設定按鈕並預填"
    },
    "功能 6: 菜品數量選項": {
        "files": [
            "src/app/input/page.tsx"
        ],
        "patterns": [
            r"dish_count|dishCount",
            r"想要幾道菜",
            r"validateDishCount",
            r"AlertDialog"
        ],
        "description": "可選填想要幾道菜並驗證"
    },
    "功能 7: 描述限制 2 行": {
        "files": [
            "src/app/recommendation/page.tsx"
        ],
        "patterns": [
            r"line-clamp-2"
        ],
        "description": "菜品說明濃縮為 2 行顯示"
    },
    "功能 8: 不同評價數": {
        "files": [
            "src/app/recommendation/page.tsx"
        ],
        "patterns": [
            r"review_count|reviewCount",
            r"generateReviewCount",
            r"則好評"
        ],
        "description": "每道菜顯示不同的評論數"
    }
}

def check_file_exists(filepath: Path) -> bool:
    """檢查檔案是否存在"""
    return filepath.exists()

def check_patterns_in_file(filepath: Path, patterns: List[str]) -> Tuple[int, List[str]]:
    """檢查檔案中是否包含特定 pattern"""
    if not filepath.exists():
        return 0, []

    try:
        content = filepath.read_text(encoding='utf-8')
        matched = []
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                matched.append(pattern)
        return len(matched), matched
    except Exception as e:
        print(f"⚠️  無法讀取檔案 {filepath}: {e}")
        return 0, []

def analyze_feature(feature_name: str, config: Dict) -> Dict:
    """分析單一功能的實作狀態"""
    result = {
        "feature": feature_name,
        "description": config["description"],
        "files_checked": [],
        "files_found": 0,
        "patterns_matched": 0,
        "total_patterns": len(config["patterns"]),
        "matched_patterns": [],
        "status": "未實作",
        "score": 0.0
    }

    for file_rel in config["files"]:
        filepath = FRONTEND_ROOT / file_rel
        exists = check_file_exists(filepath)

        file_result = {
            "path": file_rel,
            "exists": exists,
            "matched": 0,
            "patterns": []
        }

        if exists:
            result["files_found"] += 1
            matched_count, matched_patterns = check_patterns_in_file(filepath, config["patterns"])
            file_result["matched"] = matched_count
            file_result["patterns"] = matched_patterns
            result["patterns_matched"] += matched_count
            result["matched_patterns"].extend(matched_patterns)

        result["files_checked"].append(file_result)

    # 計算完成度
    file_score = result["files_found"] / len(config["files"]) if config["files"] else 0
    pattern_score = result["patterns_matched"] / result["total_patterns"] if result["total_patterns"] > 0 else 0
    result["score"] = (file_score * 0.4 + pattern_score * 0.6) * 100

    # 判斷狀態
    if result["score"] >= 80:
        result["status"] = "✅ 已完成"
    elif result["score"] >= 40:
        result["status"] = "🟡 部分實作"
    else:
        result["status"] = "❌ 未實作"

    return result

def print_report(results: List[Dict]):
    """輸出報告"""
    print("=" * 80)
    print("🔍 UX 改進計劃 v2.0 功能檢查報告")
    print("=" * 80)
    print()

    total_score = 0

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['feature']}")
        print(f"   描述: {result['description']}")
        print(f"   狀態: {result['status']} (完成度: {result['score']:.1f}%)")
        print(f"   檔案: {result['files_found']}/{len(result['files_checked'])} 存在")
        print(f"   Pattern: {result['patterns_matched']}/{result['total_patterns']} 符合")

        # 顯示檔案詳情
        for file_info in result['files_checked']:
            status_icon = "✓" if file_info['exists'] else "✗"
            print(f"      {status_icon} {file_info['path']}", end="")
            if file_info['exists'] and file_info['matched'] > 0:
                print(f" ({file_info['matched']} patterns matched)")
            elif file_info['exists']:
                print(" (no patterns matched)")
            else:
                print(" (file not found)")

        print()
        total_score += result['score']

    # 總體統計
    avg_score = total_score / len(results)
    print("=" * 80)
    print(f"📊 整體完成度: {avg_score:.1f}%")
    print()

    completed = sum(1 for r in results if r['score'] >= 80)
    partial = sum(1 for r in results if 40 <= r['score'] < 80)
    not_done = sum(1 for r in results if r['score'] < 40)

    print(f"   ✅ 已完成: {completed}/7")
    print(f"   🟡 部分實作: {partial}/7")
    print(f"   ❌ 未實作: {not_done}/7")
    print()
    print("=" * 80)

def main():
    """主函數"""
    if not FRONTEND_ROOT.exists():
        print(f"❌ 找不到 frontend 目錄: {FRONTEND_ROOT}")
        return

    results = []
    for feature_name, config in FEATURES.items():
        result = analyze_feature(feature_name, config)
        results.append(result)

    print_report(results)

    # 顯示需要實作的功能
    print("\n🎯 建議優先實作:")
    print()
    for result in sorted(results, key=lambda x: x['score']):
        if result['score'] < 80:
            print(f"   • {result['feature']} (完成度: {result['score']:.1f}%)")

if __name__ == "__main__":
    main()
