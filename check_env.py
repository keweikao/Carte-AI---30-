#!/usr/bin/env python3
"""
環境變數檢查腳本
用於驗證所有必要的環境變數是否已正確設定
"""

import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 定義必要的環境變數
REQUIRED_VARS = {
    "GEMINI_API_KEY": {
        "description": "Google Gemini API Key",
        "example": "AIzaSy...",
        "validation": lambda v: v and not v.startswith("your_") and v.startswith("AIza")
    },
    "GOOGLE_API_KEY": {
        "description": "Google Places/Search API Key",
        "example": "AIzaSy...",
        "validation": lambda v: v and not v.startswith("your_") and v.startswith("AIza")
    },
    "GOOGLE_CLIENT_ID": {
        "description": "Google OAuth Client ID",
        "example": "123456789-abcdefg.apps.googleusercontent.com",
        "validation": lambda v: v and not v.startswith("your_") and ".apps.googleusercontent.com" in v
    },
    "SEARCH_ENGINE_ID": {
        "description": "Google Custom Search Engine ID",
        "example": "a1b2c3d4e5f6g7h8i",
        "validation": lambda v: v and not v.startswith("your_") and len(v) > 5
    }
}

OPTIONAL_VARS = {
    "GOOGLE_CLIENT_SECRET": {
        "description": "Google OAuth Client Secret (前端需要)",
        "example": "GOCSPX-...",
        "validation": lambda v: v and not v.startswith("your_")
    }
}

def check_env():
    """檢查環境變數"""
    print("=" * 60)
    print("🔍 環境變數檢查報告")
    print("=" * 60)

    all_valid = True

    # 檢查必要變數
    print("\n【必要變數】")
    for var_name, config in REQUIRED_VARS.items():
        value = os.getenv(var_name)
        is_valid = config["validation"](value) if value else False

        status = "✓" if is_valid else "✗"
        color = "\033[92m" if is_valid else "\033[91m"
        reset = "\033[0m"

        print(f"{color}{status}{reset} {var_name}")
        print(f"  描述: {config['description']}")

        if is_valid:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"  當前值: {masked_value}")
        else:
            print(f"  當前值: {value or '(未設定)'}")
            print(f"  範例: {config['example']}")
            all_valid = False
        print()

    # 檢查選擇性變數
    print("\n【選擇性變數】")
    for var_name, config in OPTIONAL_VARS.items():
        value = os.getenv(var_name)
        is_valid = config["validation"](value) if value else False

        status = "✓" if is_valid else "⚠"
        color = "\033[92m" if is_valid else "\033[93m"
        reset = "\033[0m"

        print(f"{color}{status}{reset} {var_name}")
        print(f"  描述: {config['description']}")

        if is_valid:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"  當前值: {masked_value}")
        else:
            print(f"  當前值: {value or '(未設定)'}")
            print(f"  範例: {config['example']}")
        print()

    # 總結
    print("=" * 60)
    if all_valid:
        print("✅ 所有必要的環境變數都已正確設定！")
    else:
        print("❌ 有環境變數缺失或設定錯誤，請檢查 .env 檔案")
        print("\n💡 提示:")
        print("1. 複製 .env.example 為 .env (如果有)")
        print("2. 在 .env 中填入真實的 API Keys")
        print("3. 重新執行此腳本驗證")
    print("=" * 60)

    return all_valid

if __name__ == "__main__":
    check_env()
