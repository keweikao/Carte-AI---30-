# D-005: 動畫規範設計

> **完整的動畫系統與互動規格**

**任務狀態**: ✅ 規格已建立
**建立日期**: 2025-01-26

---

## 🎬 動畫設計哲學

### 三層次動畫策略

```
情感層 (Emotional) - 慶祝、驚喜時刻
    ↑
回饋層 (Feedback) - 即時操作反饋
    ↑
功能層 (Functional) - 頁面轉場、狀態變化
```

### 核心原則

1. **有目的的動畫**: 每個動畫都服務於用戶理解或情感連結
2. **性能優先**: 使用 GPU 加速屬性（transform, opacity）
3. **尊重用戶偏好**: 支援 `prefers-reduced-motion`
4. **統一時序**: 使用標準化的 duration 和 easing

---

## ⏱️ 時序系統 (Timing System)

### Duration (持續時間)

```javascript
export const duration = {
  instant: 100,    // 按鈕 hover
  fast: 200,       // Tooltip 顯示
  base: 300,       // 預設動畫
  moderate: 400,   // 卡片翻轉
  slow: 600,       // 頁面轉場
  slower: 800,     // 慶祝動畫
}
```

### Easing (緩動函數)

```javascript
export const easing = {
  // 標準緩動
  linear: 'linear',
  easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
  easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
  easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',

  // 自訂緩動（Framer Motion）
  spring: { type: 'spring', stiffness: 100, damping: 20 },
  bouncy: { type: 'spring', stiffness: 300, damping: 15 },
  smooth: { type: 'tween', ease: [0.25, 0.1, 0.25, 1] },
}
```

---

## 🎯 功能層動畫 (Functional Animations)

### 1. 頁面轉場 (Page Transitions)

使用 View Transitions API + Framer Motion fallback

#### 規格

```typescript
// 頁面進入
PageEnter: {
  initial: { opacity: 0, y: 24 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: easing.easeOut }
}

// 頁面離開
PageExit: {
  exit: { opacity: 0, y: -24 },
  transition: { duration: 0.3, ease: easing.easeIn }
}

// 支援 View Transitions API
if (document.startViewTransition) {
  document.startViewTransition(() => navigate('/next-page'))
}
```

#### 頁面特定動畫

**Landing → Input Page**
```
方向: 向上推出 (y: 0 → -100vh)
Duration: 600ms
Easing: easeInOut
```

**Input → Recommendation**
```
方向: 淡入 + 輕微放大 (scale: 0.95 → 1)
Duration: 400ms
Easing: easeOut
```

**Recommendation → Menu**
```
方向: 側滑進入 (x: 100vw → 0)
Duration: 400ms
Easing: spring
```

---

### 2. 卡片翻轉動畫 (Card Swap Animation)

這是核心動畫，需要精心調校

#### Swap Out (舊卡片離開)

```javascript
{
  initial: { x: 0, rotate: 0, opacity: 1, scale: 1 },
  animate: {
    x: '-100vw',
    rotate: -15,
    opacity: 0,
    scale: 0.8
  },
  transition: {
    duration: 0.4,
    ease: [0.4, 0, 0.2, 1]
  }
}
```

**關鍵幀分解**:
```
0ms    → x: 0,       rotate: 0deg,   opacity: 1,   scale: 1
100ms  → x: -25vw,   rotate: -4deg,  opacity: 0.9, scale: 0.95
200ms  → x: -50vw,   rotate: -8deg,  opacity: 0.6, scale: 0.9
300ms  → x: -75vw,   rotate: -12deg, opacity: 0.3, scale: 0.85
400ms  → x: -100vw,  rotate: -15deg, opacity: 0,   scale: 0.8
```

#### Swap In (新卡片進入)

```javascript
{
  initial: { x: '100vw', rotate: 15, opacity: 0, scale: 0.8 },
  animate: {
    x: 0,
    rotate: 0,
    opacity: 1,
    scale: 1
  },
  transition: {
    type: 'spring',
    stiffness: 100,
    damping: 20,
    mass: 1
  }
}
```

**Spring 動畫特性**:
- 會有輕微彈跳效果
- 總時長約 600-700ms
- 自然的減速曲線

#### Confirm Animation (確認動畫)

當用戶點擊「我要點這道」:

```javascript
// Stage 1: 輕微放大 + 降低透明度
{
  animate: {
    scale: 1.02,
    opacity: 0.75
  },
  transition: { duration: 0.2, ease: easeOut }
}

// Stage 2: 加入邊框 + CheckCircle icon
{
  border: '3px solid #6B9D7F', // success color
  // 加入 CheckCircle icon (右上角)
  transition: { duration: 0.3, ease: easeOut }
}

// Stage 3: 縮回原大小
{
  animate: { scale: 1 },
  transition: { duration: 0.2, ease: easeInOut }
}
```

---

### 3. 價格變化動畫 (Price Change Animation)

當換菜導致價格變化時的浮動提示

#### 進場動畫

```javascript
{
  initial: {
    x: 400,           // 從右側外飛入
    opacity: 0,
    scale: 0.8
  },
  animate: {
    x: 0,
    opacity: 1,
    scale: 1
  },
  transition: {
    type: 'spring',
    stiffness: 200,
    damping: 25
  }
}
```

#### Pulse 動畫 (重複 2 次)

```javascript
{
  animate: {
    scale: [1, 1.15, 1, 1.15, 1]
  },
  transition: {
    duration: 0.8,
    times: [0, 0.2, 0.4, 0.6, 0.8],
    ease: easing.easeInOut
  }
}
```

#### 離場動畫 (2 秒後)

```javascript
{
  animate: {
    opacity: 0,
    y: -20
  },
  transition: {
    duration: 0.3,
    delay: 2.0,
    ease: easing.easeIn
  }
}
```

---

### 4. 步驟指示器動畫 (Step Indicator)

#### Dot 狀態轉換

**Upcoming → Current**
```javascript
{
  animate: {
    scale: [1, 1.3, 1],
    backgroundColor: gradient-accent
  },
  transition: { duration: 0.4 }
}
```

**Current → Completed**
```javascript
{
  animate: {
    backgroundColor: success,
    // CheckMark icon fade in
  },
  transition: { duration: 0.3 }
}

// CheckMark icon
{
  initial: { scale: 0, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  transition: {
    type: 'spring',
    stiffness: 300,
    damping: 20
  }
}
```

#### Connector Line 填充

```javascript
{
  initial: { scaleX: 0 },
  animate: { scaleX: 1 },
  transition: {
    duration: 0.5,
    ease: easing.easeInOut
  },
  style: { transformOrigin: 'left' }
}
```

---

### 5. Progress Bar 動畫

#### 填充動畫

```javascript
{
  initial: { width: '0%' },
  animate: { width: `${percentage}%` },
  transition: {
    duration: 0.8,
    ease: easing.easeOut,
    delay: 0.2  // 稍微延遲，讓用戶注意到變化
  }
}
```

#### 100% 完成時的脈衝

```javascript
// 當 percentage === 100
{
  animate: {
    boxShadow: [
      '0 0 0 0 rgba(212, 165, 116, 0.7)',
      '0 0 0 10px rgba(212, 165, 116, 0)',
      '0 0 0 0 rgba(212, 165, 116, 0)'
    ]
  },
  transition: {
    duration: 1.5,
    repeat: Infinity,
    repeatDelay: 0.5
  }
}
```

---

## 🎨 回饋層動畫 (Feedback Animations)

### 1. Button Hover/Active

#### Hover 狀態

```javascript
// Primary Button
{
  scale: 1.05,
  boxShadow: '0 8px 32px rgba(45, 45, 45, 0.16)',
  transition: { duration: 0.2, ease: easeOut }
}

// Outline Button
{
  borderColor: charcoal,
  backgroundColor: 'rgba(45, 45, 45, 0.05)',
  transition: { duration: 0.15 }
}
```

#### Active 狀態

```javascript
{
  scale: 0.95,
  transition: { duration: 0.1 }
}
```

#### Disabled 狀態

```javascript
{
  opacity: 0.5,
  cursor: 'not-allowed',
  // 無 hover 效果
}
```

---

### 2. Input Focus

#### Focus Ring 動畫

```javascript
{
  initial: {
    boxShadow: '0 0 0 0 rgba(212, 165, 116, 0)'
  },
  animate: {
    boxShadow: '0 0 0 4px rgba(212, 165, 116, 0.2)',
    borderColor: caramel
  },
  transition: { duration: 0.2 }
}
```

#### Label 浮動 (如果使用 Floating Label)

```javascript
{
  initial: { y: 12, fontSize: '16px', color: charcoal/60 },
  animate: { y: -8, fontSize: '13px', color: caramel },
  transition: { duration: 0.2, ease: easeOut }
}
```

---

### 3. Tooltip / Popover

#### 進場

```javascript
{
  initial: { opacity: 0, y: 8, scale: 0.95 },
  animate: { opacity: 1, y: 0, scale: 1 },
  transition: { duration: 0.15, ease: easeOut }
}
```

#### 離場

```javascript
{
  exit: { opacity: 0, scale: 0.95 },
  transition: { duration: 0.1, ease: easeIn }
}
```

---

### 4. Slider Thumb 拖曳

#### Hover

```javascript
{
  scale: 1.2,
  boxShadow: '0 2px 8px rgba(212, 165, 116, 0.3)',
  transition: { duration: 0.15 }
}
```

#### Dragging

```javascript
{
  scale: 1.3,
  cursor: 'grabbing',
  boxShadow: '0 4px 16px rgba(212, 165, 116, 0.4)',
  transition: { duration: 0.1 }
}
```

---

## 🎉 情感層動畫 (Emotional Animations)

### 1. 慶祝動畫 (菜單完成時)

使用 `canvas-confetti` 或 `react-confetti`

#### 規格

```javascript
import confetti from 'canvas-confetti'

confetti({
  particleCount: 150,
  spread: 70,
  origin: { y: 0.6 },
  colors: ['#D4A574', '#C85A54', '#8B9D83', '#FFF8F0'],
  shapes: ['circle', 'square'],
  gravity: 1.2,
  scalar: 1.2,
  drift: 0,
  ticks: 300,
  startVelocity: 45,
  decay: 0.9
})
```

#### 觸發時機

```
當 Progress Bar 達到 100% 時
延遲 500ms 觸發
持續 3 秒
```

---

### 2. 成功提示動畫

#### CheckCircle Icon 動畫

```javascript
{
  initial: { scale: 0, rotate: -180, opacity: 0 },
  animate: { scale: 1, rotate: 0, opacity: 1 },
  transition: {
    type: 'spring',
    stiffness: 200,
    damping: 15,
    delay: 0.1
  }
}

// 外圈擴散效果
{
  animate: {
    boxShadow: [
      '0 0 0 0 rgba(107, 157, 127, 0.7)',
      '0 0 0 20px rgba(107, 157, 127, 0)',
    ]
  },
  transition: { duration: 0.6 }
}
```

---

### 3. Loading Skeleton 動畫

#### 骨架屏閃爍

```javascript
{
  animate: {
    opacity: [0.5, 1, 0.5]
  },
  transition: {
    duration: 1.5,
    repeat: Infinity,
    ease: easing.easeInOut
  }
}
```

#### Shimmer 效果（進階）

```css
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #FFF8F0 0%,
    #FFFFFF 20%,
    #FFF8F0 40%,
    #FFF8F0 100%
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite linear;
}
```

---

## 🧩 組件專屬動畫

### MenuSummary 卡片

#### 類別方塊依序顯示

```javascript
// 使用 stagger 效果
{
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: {
    duration: 0.3,
    delay: index * 0.1,  // 每個方塊延遲 100ms
    ease: easeOut
  }
}
```

### RestaurantSearch 下拉選單

#### 結果列表展開

```javascript
{
  initial: { height: 0, opacity: 0 },
  animate: { height: 'auto', opacity: 1 },
  exit: { height: 0, opacity: 0 },
  transition: { duration: 0.25, ease: easeInOut }
}

// 每個結果項目
{
  initial: { x: -8, opacity: 0 },
  animate: { x: 0, opacity: 1 },
  transition: {
    duration: 0.2,
    delay: index * 0.05
  }
}
```

### TagInput 標籤

#### 新增標籤

```javascript
{
  initial: { scale: 0, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  transition: {
    type: 'spring',
    stiffness: 300,
    damping: 20
  }
}
```

#### 移除標籤

```javascript
{
  exit: { scale: 0, opacity: 0, x: -20 },
  transition: { duration: 0.2, ease: easeIn }
}
```

---

## ♿ 無障礙處理

### prefers-reduced-motion 支援

```javascript
import { useReducedMotion } from 'framer-motion'

function Component() {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      animate={{ x: 100 }}
      transition={{
        duration: shouldReduceMotion ? 0 : 0.4
      }}
    />
  )
}
```

### CSS 替代方案

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 🎬 動畫最佳實踐

### 1. 性能優化

✅ **只動畫化這些屬性** (GPU 加速):
- `transform` (translate, scale, rotate)
- `opacity`

❌ **避免動畫化**:
- `width`, `height`, `top`, `left`
- `margin`, `padding`
- `background-color` (可使用，但性能較差)

### 2. will-change 使用

```css
.card-swapping {
  will-change: transform, opacity;
}

/* 動畫結束後移除 */
.card-swapping.animation-complete {
  will-change: auto;
}
```

### 3. Framer Motion 最佳化

```javascript
// 使用 layout animation 避免手動計算
<motion.div layout layoutId="unique-id">
  {content}
</motion.div>

// 使用 AnimatePresence 處理元件卸載
<AnimatePresence mode="wait">
  {showCard && <DishCard key={dish.id} />}
</AnimatePresence>
```

---

## 📝 D-005 任務完成報告

### 完成項目
✅ 定義三層次動畫策略
✅ 建立時序系統（duration + easing）
✅ 設計 5 個功能層動畫
✅ 設計 4 個回饋層動畫
✅ 設計 3 個情感層動畫
✅ 組件專屬動畫規範
✅ 無障礙處理方案

### 交付物
- `D-005-ANIMATION-SPECIFICATIONS.md` - 完整動畫規範

### 核心動畫設計

#### 最重要的動畫（需精心調校）:
1. **卡片翻轉**: 使用 spring 動畫 + rotate，400ms + spring bounce
2. **價格變化提示**: 飛入 + pulse × 2 + 2 秒後消失
3. **慶祝動畫**: canvas-confetti，150 顆粒子，暖色系

#### 技術要點:
- 使用 Framer Motion 處理複雜動畫
- 所有動畫支援 `prefers-reduced-motion`
- 只動畫化 `transform` 和 `opacity` 以保證 60fps
- 使用 `will-change` 提示瀏覽器優化

### 實際執行事項（前端工程師需完成）

**Week 2 執行** (8 小時):
1. 安裝 Framer Motion 與 canvas-confetti
2. 建立動畫 utility functions (src/lib/animations.ts)
3. 實作卡片翻轉動畫
4. 實作價格變化動畫
5. 實作 prefers-reduced-motion 支援

**Week 3 優化** (4 小時):
6. 調校動畫時序（實際測試後微調）
7. 加入慶祝動畫
8. 性能測試與優化

### 設計師檢查點

在 Figma 中建立動畫原型（D-014 任務）:
1. 使用 Prototype 模式連接 Frame
2. 設定 Smart Animate
3. 調整 Easing 曲線
4. 導出原型連結給工程師參考

### 下一步
D-006: 首頁設計（Landing Page）

---

**任務狀態**: ✅ 規格完成
**建立時間**: 2025-01-26
**預估時間**: 4 小時（規格建立） + 12 小時（實際實作）
