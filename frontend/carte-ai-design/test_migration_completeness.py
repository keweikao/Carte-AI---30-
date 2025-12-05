#!/usr/bin/env python3
"""
Carte AI 設計遷移完整性測試腳本
根據 LLM_MIGRATION_PROMPT.md 檢查實際開發內容
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

# 專案根目錄
PROJECT_ROOT = Path(__file__).parent

# 測試結果
class TestResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
        
    def add_pass(self, test_name: str, detail: str = ""):
        self.passed.append((test_name, detail))
        
    def add_fail(self, test_name: str, detail: str = ""):
        self.failed.append((test_name, detail))
        
    def add_warning(self, test_name: str, detail: str = ""):
        self.warnings.append((test_name, detail))
        
    def print_summary(self):
        print("\n" + "="*80)
        print("📊 Carte AI 設計遷移完整性測試報告")
        print("="*80)
        
        print(f"\n✅ 通過: {len(self.passed)}")
        for name, detail in self.passed:
            print(f"  ✓ {name}")
            if detail:
                print(f"    {detail}")
        
        print(f"\n❌ 失敗: {len(self.failed)}")
        for name, detail in self.failed:
            print(f"  ✗ {name}")
            if detail:
                print(f"    {detail}")
        
        print(f"\n⚠️  警告: {len(self.warnings)}")
        for name, detail in self.warnings:
            print(f"  ⚠ {name}")
            if detail:
                print(f"    {detail}")
        
        print("\n" + "="*80)
        total = len(self.passed) + len(self.failed)
        if total > 0:
            score = (len(self.passed) / total) * 100
            print(f"總分: {score:.1f}% ({len(self.passed)}/{total})")
        print("="*80 + "\n")

result = TestResult()

# ============================================================================
# 1. 設計系統檢查
# ============================================================================

def test_design_tokens():
    """檢查 globals.css 中的設計 tokens"""
    print("\n🎨 檢查設計系統 tokens...")
    
    globals_css = PROJECT_ROOT / "app" / "globals.css"
    if not globals_css.exists():
        result.add_fail("globals.css 存在", "檔案不存在")
        return
    
    content = globals_css.read_text()
    
    # 檢查色彩變數
    required_colors = {
        "--charcoal": "#2C2C2C",
        "--caramel": "#D4A574",
        "--terracotta": "#C77B5F",
        "--cream": "#F9F6F0",
        "--cream-dark": "#EDE8E0"
    }
    
    for var_name, expected_value in required_colors.items():
        if var_name in content:
            result.add_pass(f"色彩變數 {var_name}", f"已定義")
        else:
            result.add_fail(f"色彩變數 {var_name}", f"未找到")
    
    # 檢查字體變數
    if "--font-serif" in content or "Cormorant Garamond" in content:
        result.add_pass("字體變數 --font-serif", "已定義")
    else:
        result.add_fail("字體變數 --font-serif", "未找到")
    
    if "--font-sans" in content or "Inter" in content:
        result.add_pass("字體變數 --font-sans", "已定義")
    else:
        result.add_fail("字體變數 --font-sans", "未找到")
    
    # 檢查陰影變數
    shadow_vars = ["--shadow-subtle", "--shadow-medium", "--shadow-floating"]
    for var in shadow_vars:
        if var in content:
            result.add_pass(f"陰影變數 {var}", "已定義")
        else:
            result.add_fail(f"陰影變數 {var}", "未找到")

def test_layout_fonts():
    """檢查 layout.tsx 中的 Google Fonts 引入"""
    print("\n📝 檢查 layout.tsx 字體引入...")
    
    layout_tsx = PROJECT_ROOT / "app" / "layout.tsx"
    if not layout_tsx.exists():
        result.add_fail("layout.tsx 存在", "檔案不存在")
        return
    
    content = layout_tsx.read_text()
    
    if "Cormorant Garamond" in content or "Cormorant_Garamond" in content:
        result.add_pass("Google Fonts - Cormorant Garamond", "已引入")
    else:
        result.add_fail("Google Fonts - Cormorant Garamond", "未引入")
    
    if "Inter" in content:
        result.add_pass("Google Fonts - Inter", "已引入")
    else:
        result.add_fail("Google Fonts - Inter", "未引入")

# ============================================================================
# 2. 頁面檢查
# ============================================================================

def test_pages():
    """檢查所有必要頁面是否存在"""
    print("\n📄 檢查頁面...")
    
    required_pages = {
        "/": ("app/page.tsx", "Landing Page"),
        "/input": ("app/input/page.tsx", "輸入表單頁"),
        "/waiting": ("app/waiting/page.tsx", "等待畫面"),
        "/recommendation": ("app/recommendation/page.tsx", "推薦結果頁"),
        "/final-menu": ("app/final-menu/page.tsx", "最終菜單頁")
    }
    
    for route, (file_path, description) in required_pages.items():
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            result.add_pass(f"頁面 {route}", f"{description} 已建立")
        else:
            result.add_fail(f"頁面 {route}", f"{description} 不存在: {file_path}")

def test_landing_page_structure():
    """檢查 Landing Page 結構"""
    print("\n🏠 檢查 Landing Page 結構...")
    
    page_tsx = PROJECT_ROOT / "app" / "page.tsx"
    if not page_tsx.exists():
        result.add_fail("Landing Page 結構", "page.tsx 不存在")
        return
    
    content = page_tsx.read_text()
    
    # 檢查關鍵區塊
    sections = {
        "Hero Section": ["讓 AI", "完美", "用餐", "開始探索"],
        "Features Section": ["智慧", "個人化", "推薦"],
        "How It Works": ["選擇", "輸入", "獲得"]
    }
    
    for section_name, keywords in sections.items():
        found = any(keyword in content for keyword in keywords)
        if found:
            result.add_pass(f"Landing Page - {section_name}", "已實作")
        else:
            result.add_warning(f"Landing Page - {section_name}", "可能缺少或內容不符")

def test_input_page_steps():
    """檢查 Input Page 的 4 步驟"""
    print("\n📝 檢查 Input Page 步驟...")
    
    input_page = PROJECT_ROOT / "app" / "input" / "page.tsx"
    if not input_page.exists():
        result.add_fail("Input Page 步驟", "input/page.tsx 不存在")
        return
    
    content = input_page.read_text()
    
    # 檢查步驟元件
    step_components = [
        "step-restaurant",
        "step-dining-mode",
        "step-party-size",
        "step-preferences"
    ]
    
    for step in step_components:
        if step in content.lower():
            result.add_pass(f"Input Page - {step}", "步驟已整合")
        else:
            result.add_warning(f"Input Page - {step}", "可能未整合")

def test_waiting_page_phases():
    """檢查 Waiting Page 的 3 階段動畫"""
    print("\n⏳ 檢查 Waiting Page 階段...")
    
    waiting_page = PROJECT_ROOT / "app" / "waiting" / "page.tsx"
    if not waiting_page.exists():
        result.add_fail("Waiting Page 階段", "waiting/page.tsx 不存在")
        return
    
    content = waiting_page.read_text()
    
    # 檢查階段關鍵字
    phases = {
        "探索階段": ["探索", "菜單"],
        "分析階段": ["分析", "偏好"],
        "生成階段": ["生成", "推薦"]
    }
    
    for phase_name, keywords in phases.items():
        found = any(keyword in content for keyword in keywords)
        if found:
            result.add_pass(f"Waiting Page - {phase_name}", "已實作")
        else:
            result.add_warning(f"Waiting Page - {phase_name}", "可能缺少")
    
    # 檢查 Transparency Stream
    if "transparency" in content.lower() or "stream" in content.lower():
        result.add_pass("Waiting Page - Transparency Stream", "已實作")
    else:
        result.add_warning("Waiting Page - Transparency Stream", "可能缺少")

def test_recommendation_page_layout():
    """檢查 Recommendation Page 佈局"""
    print("\n🍽️  檢查 Recommendation Page 佈局...")
    
    rec_page = PROJECT_ROOT / "app" / "recommendation" / "page.tsx"
    if not rec_page.exists():
        result.add_fail("Recommendation Page 佈局", "recommendation/page.tsx 不存在")
        return
    
    content = rec_page.read_text()
    
    # 檢查關鍵元件
    components = {
        "DishCard": "dish-card",
        "MenuSummary": "menu-summary"
    }
    
    for comp_name, comp_file in components.items():
        if comp_file in content.lower() or comp_name in content:
            result.add_pass(f"Recommendation Page - {comp_name}", "已使用")
        else:
            result.add_fail(f"Recommendation Page - {comp_name}", "未使用")
    
    # 檢查響應式佈局
    if "md:" in content or "lg:" in content:
        result.add_pass("Recommendation Page - 響應式佈局", "已實作")
    else:
        result.add_warning("Recommendation Page - 響應式佈局", "可能缺少")

def test_final_menu_page():
    """檢查 Final Menu Page"""
    print("\n✅ 檢查 Final Menu Page...")
    
    final_page = PROJECT_ROOT / "app" / "final-menu" / "page.tsx"
    if not final_page.exists():
        result.add_fail("Final Menu Page", "final-menu/page.tsx 不存在")
        return
    
    content = final_page.read_text()
    
    # 檢查關鍵功能
    features = {
        "Success Header": ["準備好", "完成"],
        "分享功能": ["分享", "LINE", "複製"],
        "地圖連結": ["Google Maps", "地圖", "Maps"]
    }
    
    for feature_name, keywords in features.items():
        found = any(keyword in content for keyword in keywords)
        if found:
            result.add_pass(f"Final Menu Page - {feature_name}", "已實作")
        else:
            result.add_warning(f"Final Menu Page - {feature_name}", "可能缺少")

# ============================================================================
# 3. 元件檢查
# ============================================================================

def test_components():
    """檢查所有必要元件是否存在"""
    print("\n🧩 檢查元件...")
    
    required_components = {
        "header.tsx": "頂部導覽",
        "footer.tsx": "頁尾",
        "progress-bar.tsx": "步驟進度指示器",
        "dish-card.tsx": "菜色卡片",
        "menu-summary.tsx": "已選菜色摘要",
        "empty-state.tsx": "空狀態",
        "error-state.tsx": "錯誤狀態"
    }
    
    components_dir = PROJECT_ROOT / "components" / "carte"
    
    for file_name, description in required_components.items():
        file_path = components_dir / file_name
        if file_path.exists():
            result.add_pass(f"元件 {file_name}", f"{description} 已建立")
        else:
            result.add_fail(f"元件 {file_name}", f"{description} 不存在")

def test_component_props():
    """檢查元件 Props 定義"""
    print("\n🔍 檢查元件 Props...")
    
    # 檢查 DishCard Props
    dish_card = PROJECT_ROOT / "components" / "carte" / "dish-card.tsx"
    if dish_card.exists():
        content = dish_card.read_text()
        required_props = ["name", "price", "image", "selected"]
        
        props_found = sum(1 for prop in required_props if prop in content)
        if props_found >= 3:
            result.add_pass("DishCard Props", f"找到 {props_found}/{len(required_props)} 個必要 props")
        else:
            result.add_warning("DishCard Props", f"只找到 {props_found}/{len(required_props)} 個必要 props")
    
    # 檢查 ProgressBar Props
    progress_bar = PROJECT_ROOT / "components" / "carte" / "progress-bar.tsx"
    if progress_bar.exists():
        content = progress_bar.read_text()
        if "currentStep" in content or "totalSteps" in content or "step" in content.lower():
            result.add_pass("ProgressBar Props", "步驟相關 props 已定義")
        else:
            result.add_warning("ProgressBar Props", "可能缺少步驟相關 props")

# ============================================================================
# 4. 樣式檢查
# ============================================================================

def test_button_styles():
    """檢查 Primary Button 樣式"""
    print("\n🎨 檢查按鈕樣式...")
    
    # 搜尋所有 tsx 檔案
    tsx_files = list(PROJECT_ROOT.glob("**/*.tsx"))
    
    # 更新 pattern 以包含 gradient-primary 類別
    gradient_pattern = r'(bg-gradient-to-br|from-\[#D4A574\]|to-\[#C77B5F\]|gradient-primary)'
    rounded_pattern = r'rounded-full'
    
    files_with_gradient = []
    files_with_rounded = []
    
    for tsx_file in tsx_files:
        if "node_modules" in str(tsx_file):
            continue
        
        content = tsx_file.read_text()
        
        if re.search(gradient_pattern, content):
            files_with_gradient.append(tsx_file.name)
        
        if re.search(rounded_pattern, content):
            files_with_rounded.append(tsx_file.name)
    
    if files_with_gradient:
        result.add_pass("Primary Button 漸層", f"在 {len(files_with_gradient)} 個檔案中使用")
    else:
        result.add_warning("Primary Button 漸層", "未找到漸層按鈕樣式")
    
    if files_with_rounded:
        result.add_pass("圓角按鈕樣式", f"在 {len(files_with_rounded)} 個檔案中使用")
    else:
        result.add_warning("圓角按鈕樣式", "未找到 rounded-full")

def test_card_styles():
    """檢查 Card 樣式"""
    print("\n🃏 檢查卡片樣式...")
    
    tsx_files = list(PROJECT_ROOT.glob("**/*.tsx"))
    
    rounded_2xl_pattern = r'rounded-2xl'
    shadow_pattern = r'shadow-(subtle|medium|lg|xl)'
    
    files_with_rounded = []
    files_with_shadow = []
    
    for tsx_file in tsx_files:
        if "node_modules" in str(tsx_file):
            continue
        
        content = tsx_file.read_text()
        
        if re.search(rounded_2xl_pattern, content):
            files_with_rounded.append(tsx_file.name)
        
        if re.search(shadow_pattern, content):
            files_with_shadow.append(tsx_file.name)
    
    if files_with_rounded:
        result.add_pass("卡片圓角 (rounded-2xl)", f"在 {len(files_with_rounded)} 個檔案中使用")
    else:
        result.add_warning("卡片圓角 (rounded-2xl)", "未找到")
    
    if files_with_shadow:
        result.add_pass("卡片陰影", f"在 {len(files_with_shadow)} 個檔案中使用")
    else:
        result.add_warning("卡片陰影", "未找到")

def test_responsive_design():
    """檢查響應式設計"""
    print("\n📱 檢查響應式設計...")
    
    tsx_files = list(PROJECT_ROOT.glob("**/*.tsx"))
    
    breakpoints = ["sm:", "md:", "lg:", "xl:"]
    breakpoint_usage = {bp: [] for bp in breakpoints}
    
    for tsx_file in tsx_files:
        if "node_modules" in str(tsx_file):
            continue
        
        content = tsx_file.read_text()
        
        for bp in breakpoints:
            if bp in content:
                breakpoint_usage[bp].append(tsx_file.name)
    
    for bp, files in breakpoint_usage.items():
        if files:
            result.add_pass(f"響應式斷點 {bp}", f"在 {len(files)} 個檔案中使用")
        else:
            result.add_warning(f"響應式斷點 {bp}", "未使用")

# ============================================================================
# 5. 功能檢查
# ============================================================================

def test_navigation():
    """檢查頁面導航"""
    print("\n🧭 檢查頁面導航...")
    
    tsx_files = list(PROJECT_ROOT.glob("app/**/*.tsx"))
    
    routes = ["/input", "/waiting", "/recommendation", "/final-menu"]
    route_usage = {route: [] for route in routes}
    
    for tsx_file in tsx_files:
        content = tsx_file.read_text()
        
        for route in routes:
            if route in content:
                route_usage[route].append(tsx_file.name)
    
    for route, files in route_usage.items():
        if files:
            result.add_pass(f"導航到 {route}", f"在 {len(files)} 個檔案中使用")
        else:
            result.add_warning(f"導航到 {route}", "未找到導航連結")

def test_state_management():
    """檢查狀態管理"""
    print("\n🔄 檢查狀態管理...")
    
    tsx_files = list(PROJECT_ROOT.glob("app/**/*.tsx"))
    
    state_patterns = {
        "useState": r'useState',
        "useEffect": r'useEffect',
        "useRouter": r'useRouter'
    }
    
    for pattern_name, pattern in state_patterns.items():
        files_with_pattern = []
        
        for tsx_file in tsx_files:
            content = tsx_file.read_text()
            if re.search(pattern, content):
                files_with_pattern.append(tsx_file.name)
        
        if files_with_pattern:
            result.add_pass(f"React Hook - {pattern_name}", f"在 {len(files_with_pattern)} 個檔案中使用")
        else:
            result.add_warning(f"React Hook - {pattern_name}", "未使用")

# ============================================================================
# 執行所有測試
# ============================================================================

def run_all_tests():
    """執行所有測試"""
    print("🚀 開始執行 Carte AI 設計遷移完整性測試...\n")
    
    # 1. 設計系統
    test_design_tokens()
    test_layout_fonts()
    
    # 2. 頁面
    test_pages()
    test_landing_page_structure()
    test_input_page_steps()
    test_waiting_page_phases()
    test_recommendation_page_layout()
    test_final_menu_page()
    
    # 3. 元件
    test_components()
    test_component_props()
    
    # 4. 樣式
    test_button_styles()
    test_card_styles()
    test_responsive_design()
    
    # 5. 功能
    test_navigation()
    test_state_management()
    
    # 輸出結果
    result.print_summary()
    
    # 儲存 JSON 報告
    report = {
        "passed": len(result.passed),
        "failed": len(result.failed),
        "warnings": len(result.warnings),
        "details": {
            "passed": [{"test": name, "detail": detail} for name, detail in result.passed],
            "failed": [{"test": name, "detail": detail} for name, detail in result.failed],
            "warnings": [{"test": name, "detail": detail} for name, detail in result.warnings]
        }
    }
    
    report_file = PROJECT_ROOT / "test_migration_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📝 詳細報告已儲存至: {report_file}\n")
    
    return len(result.failed) == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
