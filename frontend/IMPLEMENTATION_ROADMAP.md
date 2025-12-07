# OderWhat 前端實作路徑圖

> 從零到完整產品的分階段實作指南

**狀態**: 📋 規劃中
**預估時程**: 3-4 週（1 位全職前端工程師）
**技術棧**: Next.js 14, TypeScript, Tailwind CSS, Framer Motion

---

## 🎯 實作策略

### 核心原則

1. **Mobile First**: 優先實作手機版體驗（80% 使用者來自手機）
2. **漸進增強**: 先完成核心流程，再添加進階動畫
3. **元件驅動**: 建立可重用的設計系統組件庫
4. **即測即改**: 每個階段完成後立即進行可用性測試

---

## 📅 Phase 1: 基礎設施與設計系統 (Week 1)

**目標**: 建立開發基礎，定義設計語言

### 1.1 專案設置 ⏱️ 1 天

```bash
# 檢查現有專案
cd frontend/
npm install

# 安裝設計系統依賴
npm install framer-motion canvas-confetti lucide-react
npm install -D @types/canvas-confetti

# 安裝 UI 組件庫（無頭組件）
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
npm install @radix-ui/react-toast

# 字體優化
npm install next/font
```

**驗收標準**:
- ✅ 所有依賴安裝成功
- ✅ 開發伺服器運行正常
- ✅ TypeScript 配置無錯誤

---

### 1.2 CSS 變數與全局樣式 ⏱️ 0.5 天

**任務清單**:
- [ ] 將 `DESIGN_SYSTEM.md` 中的 CSS 變數加入 `globals.css`
- [ ] 設定字體載入（Google Fonts 或本地字體）
- [ ] 定義 Tailwind 自訂配置

**實作步驟**:

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['var(--font-display)'],
        body: ['var(--font-body)'],
        handwriting: ['var(--font-handwriting)'],
      },
      colors: {
        cream: {
          50: '#FFFCF7',
          100: '#FFF8F0',
          200: '#FFF0E0',
        },
        caramel: {
          50: '#F5E6D3',
          100: '#E8D4B8',
          DEFAULT: '#D4A574',
          700: '#B8915F',
          900: '#8A6B47',
        },
        terracotta: {
          50: '#F5E1E0',
          100: '#E8C5C2',
          DEFAULT: '#C85A54',
          700: '#B04E48',
          900: '#8A3D39',
        },
        sage: {
          50: '#F0F2EF',
          100: '#D8DDD5',
          DEFAULT: '#8B9D83',
          700: '#6F7D68',
          900: '#4A5145',
        },
        charcoal: {
          50: '#F5F5F5',
          100: '#E0E0E0',
          DEFAULT: '#2D2D2D',
          700: '#1F1F1F',
          900: '#0A0A0A',
        },
      },
      borderRadius: {
        button: 'var(--radius-button)',
        card: 'var(--radius-card)',
        input: 'var(--radius-input)',
      },
      boxShadow: {
        card: '0 4px 20px rgba(212, 165, 116, 0.15)',
        floating: '0 12px 40px rgba(45, 45, 45, 0.25)',
      },
    },
  },
  plugins: [],
};

export default config;
```

```typescript
// app/layout.tsx
import { Cormorant_Garamond, Noto_Sans_TC, Caveat } from 'next/font/google';
import './globals.css';

const cormorant = Cormorant_Garamond({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-display',
});

const notoSansTC = Noto_Sans_TC({
  subsets: ['latin'],
  weight: ['300', '400', '500', '700', '900'],
  variable: '--font-body',
});

const caveat = Caveat({
  subsets: ['latin'],
  weight: ['400', '500', '700'],
  variable: '--font-handwriting',
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-TW">
      <body
        className={`${cormorant.variable} ${notoSansTC.variable} ${caveat.variable} font-body`}
      >
        {children}
      </body>
    </html>
  );
}
```

**驗收標準**:
- ✅ 字體正確載入顯示
- ✅ CSS 變數在開發工具中可見
- ✅ Tailwind 自訂類別生效

---

### 1.3 基礎組件庫 ⏱️ 2 天

**優先級排序**:

| 組件 | 優先級 | 時間 | 依賴 |
|------|--------|------|------|
| Button | P0 | 2h | 無 |
| Card | P0 | 1h | 無 |
| Input | P0 | 1.5h | 無 |
| Badge | P1 | 0.5h | 無 |
| Progress | P1 | 1h | 無 |
| Toast | P1 | 1.5h | Radix UI |
| Dialog | P2 | 1h | Radix UI |

**實作範例 - Button**:

```tsx
// components/ui/button.tsx
import { forwardRef, ButtonHTMLAttributes } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-button font-medium transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed',
  {
    variants: {
      variant: {
        primary: 'bg-gradient-to-r from-caramel to-terracotta text-white shadow-md hover:shadow-lg hover:scale-105 active:scale-95',
        secondary: 'bg-sage text-white hover:bg-sage-700',
        outline: 'border-2 border-charcoal/20 text-charcoal hover:border-charcoal hover:bg-charcoal/5',
        ghost: 'text-charcoal hover:bg-charcoal/10',
      },
      size: {
        sm: 'px-4 py-2 text-sm',
        md: 'px-6 py-3 text-base',
        lg: 'px-8 py-4 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={buttonVariants({ variant, size, className })}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';
```

**驗收標準**:
- ✅ 所有 P0 組件完成並測試
- ✅ Storybook 文檔完善（選用）
- ✅ 在隔離環境中正常運作

---

### 1.4 類型定義 ⏱️ 0.5 天

```typescript
// types/index.ts

// ==================== API 回應類型 ====================

export interface MenuItem {
  dish_name: string;
  price: number;
  category: string;
  reason: string;
  review_count?: number;
  price_estimated?: boolean;
}

export interface DishSlotResponse {
  category: string;
  display: MenuItem;
  alternatives: MenuItem[];
}

export interface RecommendationResponse {
  recommendation_id: string;
  restaurant_name: string;
  cuisine_type: string;
  total_price: number;
  per_person: number;
  items: DishSlotResponse[];
  category_summary: Record<string, number>;
}

// ==================== 前端狀態類型 ====================

export type DishStatus = 'pending' | 'selected';

export interface DishSlot {
  category: string;
  display: MenuItem;
  alternatives: MenuItem[];
  replacedDishes: string[];  // 已換掉的菜名
  status: DishStatus;
}

export interface UserInput {
  restaurant_name: string;
  people_count: number;
  budget_per_person: number;
  dining_mode: 'sharing' | 'individual';
  dietary_restrictions: string[];
  preferences: string;
}

// ==================== UI 狀態類型 ====================

export interface PriceDiff {
  amount: number;
  timestamp: number;
}

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}
```

**驗收標準**:
- ✅ 與後端 API schema 對齊
- ✅ 所有必要類型定義完成
- ✅ 無 TypeScript 錯誤

---

## 📅 Phase 2: 核心頁面實作 (Week 2)

**目標**: 完成主要用戶流程（輸入 → 推薦 → 菜單）

### 2.1 首頁 (Landing Page) ⏱️ 1 天

**設計重點**:
- Hero 區域（大標題 + 插圖佔位圖）
- 價值主張說明
- 主要 CTA（開始推薦）
- 特色展示（3 個圖示區塊）

**實作清單**:
- [ ] Hero 組件
- [ ] 特色展示網格
- [ ] CTA 按鈕動畫
- [ ] 頁面載入動畫（stagger effect）

**驗收標準**:
- ✅ 響應式布局正常
- ✅ CTA 按鈕導航至輸入頁
- ✅ 動畫流暢無卡頓

---

### 2.2 輸入頁面 ⏱️ 2 天

**設計重點**:
- 步驟式導覽（4 步驟）
- Google Places 餐廳搜尋
- 表單驗證
- 進度指示器

**實作清單**:
- [ ] StepIndicator 組件
- [ ] RestaurantSearch 組件（Google Places API）
- [ ] 表單狀態管理（React Hook Form 或 Zustand）
- [ ] 客戶端驗證

**技術細節**:

```tsx
// app/input/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { StepIndicator } from '@/components/step-indicator';
import { RestaurantSearch } from '@/components/restaurant-search';
import { Button } from '@/components/ui/button';

export default function InputPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<Partial<UserInput>>({});

  const handleNext = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    } else {
      submitForm();
    }
  };

  const submitForm = async () => {
    // 呼叫 API
    const response = await fetch('/api/recommendations', {
      method: 'POST',
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    router.push(`/recommendation?id=${data.recommendation_id}`);
  };

  return (
    <div className="min-h-screen bg-cream-100 p-4">
      <StepIndicator
        currentStep={currentStep}
        totalSteps={4}
        labels={['餐廳', '人數', '模式', '偏好']}
      />

      {currentStep === 1 && (
        <RestaurantSearch
          onSelect={(restaurant) => {
            setFormData({ ...formData, restaurant_name: restaurant });
          }}
        />
      )}

      {/* 其他步驟... */}

      <Button onClick={handleNext}>
        {currentStep === 4 ? '開始推薦' : '下一步'}
      </Button>
    </div>
  );
}
```

**驗收標準**:
- ✅ 所有步驟流程正常
- ✅ Google Places 搜尋功能正常
- ✅ 表單驗證完整
- ✅ 提交後正確導航

---

### 2.3 推薦頁面 ⏱️ 3 天

**設計重點** (根據 v3 規格):
- 菜單摘要卡片（類別統計 + 總價）
- 菜色卡片（大卡片設計）
- 換菜動畫
- 價格變化指示器
- 進度追蹤

**實作清單**:
- [ ] MenuSummary 組件
- [ ] DishCard 組件
- [ ] SwapAnimation 組件
- [ ] PriceIndicator 組件
- [ ] ProgressBar 組件
- [ ] 狀態管理（已選擇、候選池）

**關鍵邏輯 - 換菜**:

```tsx
// app/recommendation/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';

export default function RecommendationPage() {
  const searchParams = useSearchParams();
  const recommendationId = searchParams.get('id');

  const [slots, setSlots] = useState<DishSlot[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [priceDiff, setPriceDiff] = useState(0);

  // 載入推薦資料
  useEffect(() => {
    fetchRecommendation(recommendationId);
  }, [recommendationId]);

  const handleSwap = async () => {
    const currentSlot = slots[currentIndex];
    const nextAlternative = currentSlot.alternatives[0];

    if (!nextAlternative) {
      // 候選池用完，呼叫 API 取得更多
      const moreAlternatives = await fetchMoreAlternatives(
        recommendationId,
        currentSlot.category,
        currentSlot.replacedDishes
      );

      if (moreAlternatives.length === 0) {
        toast.error('該類別暫無更多推薦');
        return;
      }

      currentSlot.alternatives = moreAlternatives;
    }

    // 計算價格差異
    const oldPrice = currentSlot.display.price;
    const newPrice = nextAlternative.price;
    setPriceDiff(newPrice - oldPrice);

    // 更新槽位
    const newSlots = [...slots];
    newSlots[currentIndex] = {
      ...currentSlot,
      display: nextAlternative,
      alternatives: currentSlot.alternatives.slice(1),
      replacedDishes: [...currentSlot.replacedDishes, currentSlot.display.dish_name],
    };

    setSlots(newSlots);

    // 記錄換菜行為（追蹤 API）
    await recordSwap(recommendationId, currentSlot.display, nextAlternative);
  };

  const handleConfirm = () => {
    // 標記為已選擇
    const newSlots = [...slots];
    newSlots[currentIndex].status = 'selected';
    setSlots(newSlots);

    // 移至下一道
    if (currentIndex < slots.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const allDecided = slots.every(slot => slot.status === 'selected');

  return (
    <div className="min-h-screen bg-cream-100 p-4 space-y-6">
      <MenuSummary
        categorySummary={getCategorySummary(slots)}
        totalPrice={calculateTotalPrice(slots)}
        perPerson={calculatePerPerson(slots)}
        peopleCount={peopleCount}
        decidedCount={slots.filter(s => s.status === 'selected').length}
        totalCount={slots.length}
      />

      <SwapAnimation
        currentDish={slots[currentIndex]?.display}
        status={slots[currentIndex]?.status}
        onConfirm={handleConfirm}
        onSwap={handleSwap}
      />

      <PriceIndicator
        priceDiff={priceDiff}
        onComplete={() => setPriceDiff(0)}
      />

      <Button
        disabled={!allDecided}
        onClick={() => router.push('/menu')}
        className="w-full"
      >
        產出點餐菜單
      </Button>
    </div>
  );
}
```

**驗收標準**:
- ✅ 所有菜色卡片正確顯示
- ✅ 換菜動畫流暢
- ✅ 價格即時更新
- ✅ 進度正確追蹤
- ✅ 候選池邏輯正確

---

### 2.4 菜單頁面 ⏱️ 1 天

**設計重點**:
- 最終菜單展示
- 分享功能
- 滿意度評分

**實作清單**:
- [ ] 菜單清單組件
- [ ] 分享卡片生成（Canvas API）
- [ ] 評分組件
- [ ] 列印樣式優化

**驗收標準**:
- ✅ 菜單正確顯示
- ✅ 分享功能正常
- ✅ 評分可提交
- ✅ 列印樣式美觀

---

## 📅 Phase 3: 進階功能與優化 (Week 3)

### 3.1 動畫精緻化 ⏱️ 2 天

**任務清單**:
- [ ] 頁面轉場動畫（View Transitions API）
- [ ] 慶祝動畫（完成所有決策時）
- [ ] 微互動（按鈕 hover、點擊回饋）
- [ ] 載入骨架屏（Skeleton）

---

### 3.2 錯誤處理與邊界情況 ⏱️ 1 天

**任務清單**:
- [ ] API 錯誤處理
- [ ] 候選池用完提示
- [ ] 網路斷線提示
- [ ] 超預算警告對話框

---

### 3.3 效能優化 ⏱️ 1 天

**任務清單**:
- [ ] 圖片懶加載
- [ ] 路由預載（prefetch）
- [ ] 組件動態導入
- [ ] 字體優化載入

---

### 3.4 無障礙改進 ⏱️ 1 天

**任務清單**:
- [ ] 鍵盤導航支援
- [ ] ARIA 標籤完善
- [ ] 顏色對比檢查
- [ ] 螢幕閱讀器測試

---

## 📅 Phase 4: 測試與部署 (Week 4)

### 4.1 測試 ⏱️ 2 天

**測試清單**:
- [ ] 單元測試（關鍵邏輯）
- [ ] 組件測試（React Testing Library）
- [ ] E2E 測試（Playwright）
- [ ] 跨瀏覽器測試

---

### 4.2 部署準備 ⏱️ 1 天

**任務清單**:
- [ ] 環境變數設定
- [ ] Build 優化
- [ ] SEO 設定（metadata）
- [ ] Analytics 整合

---

### 4.3 上線與監控 ⏱️ 1 天

**任務清單**:
- [ ] 部署至 Cloud Run
- [ ] 錯誤監控（Sentry）
- [ ] 效能監控（Web Vitals）
- [ ] A/B 測試準備

---

## 🎯 驗收標準總覽

### 功能完整性

- ✅ 所有核心流程可完整走通
- ✅ API 整合無錯誤
- ✅ 所有邊界情況處理妥當

### 效能指標

- ✅ Lighthouse Score > 90
- ✅ LCP < 2.5s
- ✅ FID < 100ms
- ✅ CLS < 0.1

### 無障礙標準

- ✅ WCAG 2.1 AA 合規
- ✅ 鍵盤完全可操作
- ✅ 螢幕閱讀器友善

### 設計還原度

- ✅ 視覺與設計稿一致 (95%+)
- ✅ 動畫流暢自然
- ✅ 響應式正常

---

## 🚀 快速啟動指南

### 立即開始開發

```bash
# 1. 安裝依賴
cd frontend/
npm install

# 2. 設定環境變數
cp .env.example .env.local
# 編輯 .env.local，填入 API URLs

# 3. 啟動開發伺服器
npm run dev

# 4. 開始實作 Phase 1
# 按照本文檔順序逐步實作
```

### 開發工作流

```bash
# 建立功能分支
git checkout -b feature/dish-card

# 實作組件
# ...

# 測試
npm run test

# 提交
git add .
git commit -m "feat: add DishCard component"

# 推送
git push origin feature/dish-card
```

---

## 📊 進度追蹤

使用 GitHub Projects 或 Notion 追蹤進度：

| Phase | 任務數 | 已完成 | 進度 |
|-------|--------|--------|------|
| Phase 1 | 4 | 0 | 0% |
| Phase 2 | 4 | 0 | 0% |
| Phase 3 | 4 | 0 | 0% |
| Phase 4 | 3 | 0 | 0% |

---

## 🆘 常見問題

### Q: 動畫在某些裝置上卡頓？
A: 使用 `will-change` CSS 屬性，並考慮降級方案

### Q: Google Places API 配額不夠？
A: 實作本地快取，減少重複請求

### Q: 字體載入閃爍？
A: 使用 `font-display: swap` 並設定 fallback 字體

---

**最後更新**: 2025-01-26
**維護者**: Frontend Team
