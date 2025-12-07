# OderWhat 組件實作範例

> 展示如何將設計系統應用到實際 React 組件

---

## 📋 目錄

1. [DishCard - 菜色卡片](#dishcard)
2. [MenuSummary - 菜單摘要](#menusummary)
3. [SwapAnimation - 換菜動畫](#swapanimation)
4. [PriceIndicator - 價格指示器](#priceindicator)
5. [ProgressBar - 進度條](#progressbar)

---

## 🍽️ DishCard - 菜色卡片 {#dishcard}

### 設計規範

- 大卡片設計，手機版佔據主要視覺焦點
- 上方：菜色照片佔位區（淡色背景 + 菜系圖示）
- 中間：菜名 + 價格（層次分明）
- 下方：手寫風格推薦理由
- 兩種狀態：`pending` (待選擇) / `selected` (已確認)

### 實作代碼

```tsx
// components/dish-card.tsx
'use client';

import { motion } from 'framer-motion';
import { CheckCircle2 } from 'lucide-react';
import { MenuItem } from '@/types';

interface DishCardProps {
  dish: MenuItem;
  status: 'pending' | 'selected';
  onConfirm: () => void;
  onSwap: () => void;
}

export function DishCard({ dish, status, onConfirm, onSwap }: DishCardProps) {
  const isSelected = status === 'selected';

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={`
        relative
        bg-white
        rounded-[var(--radius-card)]
        overflow-hidden
        transition-all duration-300
        ${isSelected
          ? 'shadow-[0_0_0_3px_var(--color-success)] opacity-75'
          : 'shadow-[var(--shadow-card)] hover:shadow-[var(--shadow-lg)]'
        }
      `}
    >
      {/* 已選擇標記 */}
      {isSelected && (
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          className="absolute top-4 right-4 z-10"
        >
          <CheckCircle2 className="w-8 h-8 text-[var(--color-success)]" />
        </motion.div>
      )}

      {/* 菜色照片佔位區 */}
      <div className="
        h-48
        bg-gradient-to-br from-cream-50 to-caramel-50
        flex items-center justify-center
      ">
        <div className="text-6xl opacity-30">
          {getCategoryEmoji(dish.category)}
        </div>
      </div>

      {/* 卡片內容 */}
      <div className="p-6 space-y-4">
        {/* 類別標籤 */}
        <div className="inline-block px-3 py-1 rounded-full bg-sage/10 text-sage-700 text-sm font-medium">
          {dish.category}
        </div>

        {/* 菜名與價格 */}
        <div className="space-y-2">
          <h3 className="text-2xl font-bold text-charcoal font-body">
            {dish.dish_name}
          </h3>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-terracotta">
              NT$ {dish.price}
            </span>
            {dish.price_estimated && (
              <span className="text-sm text-charcoal/60">
                (估算)
              </span>
            )}
          </div>
        </div>

        {/* 推薦理由 - 手寫風格 */}
        <div className="
          p-4
          bg-cream-100/50
          rounded-lg
          border-l-4 border-caramel
        ">
          <p className="
            font-handwriting
            text-xl
            text-caramel-700
            leading-relaxed
            -rotate-1
          ">
            "{dish.reason}"
          </p>
          {dish.review_count && (
            <p className="text-sm text-charcoal/60 mt-2 font-body">
              基於 {dish.review_count} 則評論
            </p>
          )}
        </div>

        {/* 操作按鈕 */}
        {!isSelected && (
          <div className="flex gap-3 pt-4">
            <button
              onClick={onConfirm}
              className="
                flex-1
                px-6 py-3
                rounded-[var(--radius-button)]
                bg-gradient-to-r from-caramel to-terracotta
                text-white font-medium
                shadow-md hover:shadow-lg
                transition-all duration-300
                hover:scale-105
                active:scale-95
              "
            >
              ✅ 我要點這道
            </button>
            <button
              onClick={onSwap}
              className="
                flex-1
                px-6 py-3
                rounded-[var(--radius-button)]
                border-2 border-charcoal/20
                text-charcoal
                hover:border-charcoal
                hover:bg-charcoal/5
                transition-all duration-300
              "
            >
              🔄 換一道
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
}

// 輔助函數：根據類別返回 emoji
function getCategoryEmoji(category: string): string {
  const emojiMap: Record<string, string> = {
    '冷菜': '🥗',
    '熱菜': '🍖',
    '主食': '🍚',
    '湯品': '🍲',
    '點心': '🥟',
    '刺身': '🍣',
    '壽司': '🍱',
    '麵類': '🍜',
    '前菜': '🥙',
    '主餐': '🥩',
    '甜點': '🍰',
    '飲料': '🥤',
  };
  return emojiMap[category] || '🍽️';
}
```

### CSS 變數定義（需加入 globals.css）

```css
/* globals.css */
.font-handwriting {
  font-family: var(--font-handwriting);
}

.text-caramel-700 {
  color: var(--color-caramel-700);
}

.bg-cream-100\/50 {
  background-color: rgba(255, 248, 240, 0.5);
}

.border-caramel {
  border-color: var(--color-caramel);
}
```

---

## 📊 MenuSummary - 菜單摘要 {#menusummary}

### 設計規範

根據 v3 規格展示：
- 本次菜單組成（類別 + 數量）
- 總價、人均價格
- 進度顯示（已決定 X/Y 道）

### 實作代碼

```tsx
// components/menu-summary.tsx
'use client';

import { motion } from 'framer-motion';

interface MenuSummaryProps {
  categorySummary: Record<string, number>;
  totalPrice: number;
  perPerson: number;
  peopleCount: number;
  decidedCount: number;
  totalCount: number;
}

export function MenuSummary({
  categorySummary,
  totalPrice,
  perPerson,
  peopleCount,
  decidedCount,
  totalCount,
}: MenuSummaryProps) {
  const progress = (decidedCount / totalCount) * 100;

  return (
    <div className="
      bg-white
      rounded-[var(--radius-card)]
      shadow-[var(--shadow-card)]
      p-6
      space-y-4
    ">
      {/* 標題 */}
      <h2 className="text-xl font-bold text-charcoal font-body">
        本次菜單組成
      </h2>

      {/* 類別網格 */}
      <div className="grid grid-cols-2 gap-3">
        {Object.entries(categorySummary).map(([category, count]) => (
          <div
            key={category}
            className="
              flex items-center gap-2
              px-4 py-2
              bg-cream-100
              rounded-lg
            "
          >
            <span className="text-2xl">
              {getCategoryEmoji(category)}
            </span>
            <span className="text-sm font-medium text-charcoal">
              {category}
            </span>
            <span className="ml-auto text-lg font-bold text-terracotta">
              ×{count}
            </span>
          </div>
        ))}
      </div>

      {/* 分隔線 */}
      <div className="border-t border-charcoal/10 pt-4 space-y-2">
        {/* 總計 */}
        <div className="flex justify-between items-baseline">
          <span className="text-base text-charcoal/80">
            共 {totalCount} 道
          </span>
          <div className="text-right">
            <span className="text-2xl font-bold text-charcoal">
              NT$ {totalPrice.toLocaleString()}
            </span>
          </div>
        </div>

        {/* 人均 */}
        <div className="flex justify-between items-baseline">
          <span className="text-sm text-charcoal/60">
            人均 ({peopleCount} 人)
          </span>
          <span className="text-lg font-medium text-sage-700">
            NT$ {perPerson.toLocaleString()}
          </span>
        </div>

        {/* 進度 */}
        <div className="pt-2">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-charcoal/80">
              已決定 {decidedCount}/{totalCount} 道
            </span>
            <span className="text-sm font-medium text-terracotta">
              {Math.round(progress)}%
            </span>
          </div>

          {/* 進度條 */}
          <div className="h-2 bg-charcoal/10 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-caramel to-terracotta rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.6, ease: 'easeOut' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

// 重用之前的 getCategoryEmoji 函數
function getCategoryEmoji(category: string): string {
  const emojiMap: Record<string, string> = {
    '冷菜': '🥗',
    '熱菜': '🍖',
    '主食': '🍚',
    '湯品': '🍲',
    '點心': '🥟',
  };
  return emojiMap[category] || '🍽️';
}
```

---

## 🔄 SwapAnimation - 換菜動畫 {#swapanimation}

### 設計規範

卡片翻出/滑入動畫，提供流暢的視覺反饋

### 實作代碼

```tsx
// components/swap-animation.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { DishCard } from './dish-card';
import { MenuItem } from '@/types';

interface SwapAnimationProps {
  currentDish: MenuItem;
  status: 'pending' | 'selected';
  onConfirm: () => void;
  onSwap: () => void;
}

export function SwapAnimation({
  currentDish,
  status,
  onConfirm,
  onSwap,
}: SwapAnimationProps) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={currentDish.dish_name}
        initial={{
          x: '100vw',
          rotate: 15,
          opacity: 0
        }}
        animate={{
          x: 0,
          rotate: 0,
          opacity: 1
        }}
        exit={{
          x: '-100vw',
          rotate: -15,
          opacity: 0
        }}
        transition={{
          type: 'spring',
          stiffness: 100,
          damping: 20,
        }}
      >
        <DishCard
          dish={currentDish}
          status={status}
          onConfirm={onConfirm}
          onSwap={onSwap}
        />
      </motion.div>
    </AnimatePresence>
  );
}
```

### 使用範例

```tsx
// app/recommendation/page.tsx
'use client';

import { useState } from 'react';
import { SwapAnimation } from '@/components/swap-animation';

export default function RecommendationPage() {
  const [slots, setSlots] = useState<DishSlot[]>([...]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleSwap = () => {
    // 換菜邏輯
    const newDish = getNextAlternative(currentIndex);
    updateSlot(currentIndex, newDish);
  };

  const handleConfirm = () => {
    // 確認邏輯
    markAsSelected(currentIndex);
    setCurrentIndex(currentIndex + 1);
  };

  return (
    <div className="p-4">
      <SwapAnimation
        currentDish={slots[currentIndex].display}
        status={slots[currentIndex].status}
        onConfirm={handleConfirm}
        onSwap={handleSwap}
      />
    </div>
  );
}
```

---

## 💰 PriceIndicator - 價格指示器 {#priceindicator}

### 設計規範

當換菜導致價格變化時，顯示浮動的價格差異動畫

### 實作代碼

```tsx
// components/price-indicator.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';

interface PriceIndicatorProps {
  priceDiff: number;
  onComplete?: () => void;
}

export function PriceIndicator({ priceDiff, onComplete }: PriceIndicatorProps) {
  const [show, setShow] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShow(false);
      onComplete?.();
    }, 2000);

    return () => clearTimeout(timer);
  }, [priceDiff, onComplete]);

  if (priceDiff === 0) return null;

  const isIncrease = priceDiff > 0;
  const color = isIncrease ? 'var(--color-warning)' : 'var(--color-success)';

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ y: 20, opacity: 0, scale: 0.8 }}
          animate={{ y: 0, opacity: 1, scale: 1 }}
          exit={{ y: -20, opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="
            fixed top-24 right-4 z-50
            px-6 py-3
            rounded-full
            shadow-lg
          "
          style={{
            backgroundColor: color,
            color: 'white',
          }}
        >
          <motion.span
            className="text-xl font-bold"
            animate={{ scale: [1, 1.2, 1] }}
            transition={{
              duration: 0.5,
              repeat: 2,
              ease: 'easeInOut'
            }}
          >
            {isIncrease ? '+' : ''}NT$ {Math.abs(priceDiff)}
          </motion.span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

### 使用範例

```tsx
// app/recommendation/page.tsx
const [priceDiff, setPriceDiff] = useState(0);

const handleSwap = () => {
  const oldPrice = currentDish.price;
  const newDish = getNextAlternative();
  const newPrice = newDish.price;

  setPriceDiff(newPrice - oldPrice);
  updateCurrentDish(newDish);
};

return (
  <>
    <PriceIndicator
      priceDiff={priceDiff}
      onComplete={() => setPriceDiff(0)}
    />
    {/* ... */}
  </>
);
```

---

## 📈 ProgressBar - 進度條 {#progressbar}

### 設計規範

顯示決策進度，完成時有慶祝動畫

### 實作代碼

```tsx
// components/progress-bar.tsx
'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import confetti from 'canvas-confetti';

interface ProgressBarProps {
  current: number;
  total: number;
  label?: string;
}

export function ProgressBar({ current, total, label }: ProgressBarProps) {
  const [wasCompleted, setWasCompleted] = useState(false);
  const progress = (current / total) * 100;
  const isComplete = current === total;

  useEffect(() => {
    if (isComplete && !wasCompleted) {
      setWasCompleted(true);

      // 觸發慶祝動畫
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#D4A574', '#C85A54', '#8B9D83'],
      });
    }
  }, [isComplete, wasCompleted]);

  return (
    <div className="space-y-2">
      {/* 標籤 */}
      {label && (
        <div className="flex justify-between items-center">
          <span className="text-sm text-charcoal/80">
            {label}
          </span>
          <span className="text-sm font-medium text-terracotta">
            {current}/{total}
          </span>
        </div>
      )}

      {/* 進度條容器 */}
      <div className="
        h-3
        bg-charcoal/10
        rounded-full
        overflow-hidden
        relative
      ">
        {/* 進度填充 */}
        <motion.div
          className="
            h-full
            bg-gradient-to-r from-caramel to-terracotta
            rounded-full
            relative
          "
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{
            duration: 0.6,
            ease: 'easeOut'
          }}
        >
          {/* 完成時的脈衝效果 */}
          {isComplete && (
            <motion.div
              className="absolute inset-0 bg-white/30 rounded-full"
              animate={{ opacity: [0.3, 0.6, 0.3] }}
              transition={{
                duration: 1,
                repeat: Infinity
              }}
            />
          )}
        </motion.div>
      </div>

      {/* 完成訊息 */}
      {isComplete && (
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-sm font-medium text-success text-center"
        >
          ✨ 所有菜品已決定！
        </motion.p>
      )}
    </div>
  );
}
```

---

## 🎨 全局樣式設定

### 安裝依賴

```bash
npm install framer-motion canvas-confetti lucide-react
npm install -D @types/canvas-confetti
```

### globals.css 完整配置

```css
/* app/globals.css */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* 字體 */
    --font-display: 'Cormorant Garamond', serif;
    --font-body: 'Noto Sans TC', -apple-system, sans-serif;
    --font-handwriting: 'Caveat', cursive;

    /* 色彩 - 主色調 */
    --color-cream-50: #FFFCF7;
    --color-cream-100: #FFF8F0;
    --color-caramel: #D4A574;
    --color-caramel-700: #B8915F;
    --color-terracotta: #C85A54;
    --color-sage: #8B9D83;
    --color-sage-700: #6F7D68;
    --color-charcoal: #2D2D2D;

    /* 功能色 */
    --color-success: #6B9D7F;
    --color-warning: #E89C5C;
    --color-error: #C85A54;

    /* 圓角 */
    --radius-button: 1rem;
    --radius-card: 1.5rem;
    --radius-input: 0.75rem;

    /* 陰影 */
    --shadow-card: 0 4px 20px rgba(212, 165, 116, 0.15);
    --shadow-lg: 0 8px 32px rgba(45, 45, 45, 0.16);
  }

  body {
    font-family: var(--font-body);
    background-color: var(--color-cream-100);
    color: var(--color-charcoal);
  }
}

@layer utilities {
  .font-display {
    font-family: var(--font-display);
  }

  .font-handwriting {
    font-family: var(--font-handwriting);
  }

  .text-charcoal {
    color: var(--color-charcoal);
  }

  .text-terracotta {
    color: var(--color-terracotta);
  }

  .text-caramel-700 {
    color: var(--color-caramel-700);
  }

  .text-sage-700 {
    color: var(--color-sage-700);
  }

  .bg-cream-100 {
    background-color: var(--color-cream-100);
  }

  .border-caramel {
    border-color: var(--color-caramel);
  }
}
```

---

## 📝 使用說明

### 1. 複製組件檔案到專案

```bash
# 在 frontend/ 目錄下
mkdir -p src/components
cp COMPONENT_EXAMPLES.md src/components/

# 然後根據範例創建對應的組件檔案
```

### 2. 確認類型定義

```typescript
// types/index.ts
export interface MenuItem {
  dish_name: string;
  price: number;
  category: string;
  reason: string;
  review_count?: number;
  price_estimated?: boolean;
}

export interface DishSlot {
  category: string;
  display: MenuItem;
  alternatives: MenuItem[];
  status: 'pending' | 'selected';
}
```

### 3. 整合到頁面

參考各組件的「使用範例」章節，整合到對應的頁面中。

---

**最後更新**: 2025-01-26
**維護者**: Frontend Team
