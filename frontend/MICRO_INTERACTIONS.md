# FE-036: 微互動優化實作文件

## 概覽

本文件說明了在 OderWhat 前端專案中實作的微互動優化，包括按鈕波紋效果、輸入框聚焦動畫、卡片懸停陰影變化，以及觸覺回饋功能。

## 實作內容

### 1. Button 組件優化 (`/src/components/ui/button.tsx`)

#### 新增功能
- **點擊波紋效果**：點擊時從點擊位置擴散的白色半透明波紋
- **懸停縮放**：滑鼠懸停時輕微放大（1.02x）
- **按壓縮放**：點擊時輕微縮小（0.97x）
- **觸覺回饋**：手機端點擊時提供 10ms 的輕微振動

#### 技術細節
```typescript
// 波紋動畫參數
duration: 500ms (DURATION.slow)
easing: EASING.out
expansion: 0 → 200px diameter

// 懸停動畫
scale: 1 → 1.02
duration: 200ms (DURATION.fast)

// 按壓動畫
scale: 1 → 0.97
duration: 100ms (DURATION.instant)
```

#### 使用範例
```tsx
import { Button } from "@/components/ui/button"

// 基本使用（自動包含所有微互動）
<Button variant="primary">點擊我</Button>
<Button variant="secondary">次要按鈕</Button>
<Button variant="outline">外框按鈕</Button>

// 使用 asChild 時會自動停用動畫效果
<Button asChild>
  <Link href="/page">連結按鈕</Link>
</Button>
```

### 2. Input 組件優化 (`/src/components/ui/input.tsx`)

#### 新增功能
- **聚焦縮放**：獲得焦點時輕微放大（1.01x）並上移（-1px）
- **光暈效果**：聚焦時顯示徑向漸層背景光暈
- **彈簧動畫**：使用彈簧物理曲線提供自然感受

#### 技術細節
```typescript
// 聚焦動畫
scale: 1 → 1.01
y: 0 → -1px
duration: 200ms (DURATION.fast)
spring: SPRING_CONFIGS.gentle

// 光暈效果
background: radial-gradient(circle, rgba(200,90,84,0.05) 0%, transparent 70%)
opacity: 0 → 1
scale: 0.95 → 1
```

#### 使用範例
```tsx
import { Input } from "@/components/ui/input"

// 基本使用
<Input type="text" placeholder="請輸入..." />
<Input type="email" placeholder="email@example.com" />
<Input type="password" placeholder="密碼" />

// 帶有狀態管理
const [value, setValue] = useState("")
<Input
  value={value}
  onChange={(e) => setValue(e.target.value)}
  placeholder="受控輸入框"
/>
```

### 3. Card 組件優化 (`/src/components/ui/card.tsx`)

#### 新增功能
- **懸停上浮**：滑鼠懸停時向上移動（-4px）
- **輕微縮放**：懸停時放大（1.01x）
- **陰影變化**：從 shadow-card 過渡到 shadow-floating
- **彈簧動畫**：流暢的彈簧物理效果

#### 技術細節
```typescript
// 懸停動畫
y: 0 → -4px
scale: 1 → 1.01
duration: 200ms (DURATION.fast)
spring: SPRING_CONFIGS.gentle

// 陰影過渡
default: 0 4px 20px rgba(212,165,116,0.15)
hover: 0 12px 40px rgba(45,45,45,0.25)
transition: 200ms ease-out
```

#### 使用範例
```tsx
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter
} from "@/components/ui/card"

// 基本卡片（自動包含懸停效果）
<Card>
  <CardHeader>
    <CardTitle>卡片標題</CardTitle>
    <CardDescription>卡片描述</CardDescription>
  </CardHeader>
  <CardContent>
    <p>卡片內容</p>
  </CardContent>
  <CardFooter>
    <Button>動作按鈕</Button>
  </CardFooter>
</Card>

// 選中狀態的卡片
<Card variant="selected">
  <CardHeader>
    <CardTitle>已選擇</CardTitle>
  </CardHeader>
  <CardContent>
    這張卡片有特殊的邊框樣式
  </CardContent>
</Card>
```

### 4. 觸覺回饋工具 (`/src/lib/haptic-utils.ts`)

#### 新增功能
提供統一的觸覺回饋 API，支援多種振動模式：

- `hapticLight()` - 輕微振動（10ms）：用於按鈕點擊
- `hapticMedium()` - 中度振動（20ms）：用於標準互動
- `hapticHeavy()` - 強烈振動（30ms）：用於重要動作
- `hapticSuccess()` - 成功模式（雙振）：用於成功提示
- `hapticError()` - 錯誤模式（三振）：用於錯誤提示
- `hapticWarning()` - 警告模式（40ms）：用於警告提示
- `hapticCustom(pattern)` - 自訂模式：自訂振動序列

#### 使用範例
```tsx
import {
  hapticLight,
  hapticSuccess,
  hapticError,
  isHapticSupported
} from "@/lib/haptic-utils"

// 檢查是否支援
if (isHapticSupported()) {
  // 按鈕點擊
  hapticLight()

  // 成功提示
  hapticSuccess()

  // 錯誤提示
  hapticError()

  // 自訂模式
  hapticCustom([50, 100, 50, 100, 50])
}
```

## 動畫規範遵循

所有動畫都遵循設計系統規範（`/src/lib/animation-utils.ts`）：

### 時長標準
- `DURATION.instant` - 100ms：即時回饋
- `DURATION.fast` - 200ms：快速過渡
- `DURATION.base` - 300ms：標準動畫
- `DURATION.slow` - 500ms：慢速動畫
- `DURATION.slower` - 800ms：最慢動畫

### 緩動曲線
- `EASING.in` - [0.4, 0, 1, 1]：加速進入
- `EASING.out` - [0, 0, 0.2, 1]：減速退出
- `EASING.inOut` - [0.4, 0, 0.2, 1]：平滑進出
- `EASING.spring` - [0.34, 1.56, 0.64, 1]：彈簧效果
- `EASING.smooth` - [0.65, 0, 0.35, 1]：柔和過渡

### 彈簧配置
- `SPRING_CONFIGS.bouncy` - 彈跳感強
- `SPRING_CONFIGS.gentle` - 柔和彈性
- `SPRING_CONFIGS.snappy` - 快速回彈
- `SPRING_CONFIGS.smooth` - 平滑彈性

## 無障礙支援

所有微互動都完整支援 `prefers-reduced-motion` 設定：

```typescript
// 自動檢測使用者偏好
const reducedMotion = prefersReducedMotion()

// 根據偏好調整動畫
if (reducedMotion) {
  // 停用複雜動畫
  // 僅保留簡單的透明度過渡
  // 時長縮短至 100ms
} else {
  // 完整動畫效果
}
```

### 降級策略
- **減少動畫模式下**：
  - 停用波紋效果
  - 停用縮放和位移動畫
  - 僅保留透明度淡入淡出
  - 動畫時長縮短至 100ms
  - 所有功能保持完整

## 效能優化

### GPU 加速
所有動畫都使用 GPU 加速的 CSS 屬性：
- `transform` - 位移、縮放、旋轉
- `opacity` - 透明度變化
- 避免使用觸發重排的屬性（width、height、top、left 等）

### 記憶體管理
- 波紋動畫完成後自動清理
- 使用 `AnimatePresence` 管理退出動畫
- 事件監聽器正確清理

### 效能指標
- 目標：60fps（16.67ms per frame）
- 所有動畫使用 requestAnimationFrame
- 避免 JavaScript 密集計算

## 測試與展示

### 展示頁面
訪問 `/micro-interactions-demo` 查看所有微互動效果的即時展示。

### 測試清單
- [ ] 按鈕點擊波紋效果正常
- [ ] 按鈕懸停縮放流暢
- [ ] 輸入框聚焦動畫自然
- [ ] 卡片懸停陰影過渡平滑
- [ ] 手機端觸覺回饋正常
- [ ] prefers-reduced-motion 正確降級
- [ ] 效能達到 60fps
- [ ] 無記憶體洩漏

## 瀏覽器支援

### 動畫支援
- Chrome 51+
- Firefox 52+
- Safari 13+
- Edge 79+

### 觸覺回饋支援
- Android Chrome 32+
- Samsung Internet 2.0+
- iOS Safari **不支援**（API 存在但不作用）

## 未來改進

1. **進階波紋效果**
   - 多色彩波紋
   - 波紋速度可調
   - 波紋形狀變化

2. **更多輸入框效果**
   - 輸入時的字符動畫
   - 錯誤狀態的抖動效果
   - 成功狀態的勾選動畫

3. **卡片進階互動**
   - 傾斜效果（3D transform）
   - 滑動手勢支援
   - 翻轉動畫

4. **更豐富的觸覺回饋**
   - 根據動作類型自動選擇振動模式
   - 可配置的振動強度
   - 振動模式預設集

## 相關文件

- [動畫工具文件](/src/lib/animation-utils.ts)
- [頁面過渡文件](/src/components/page-transition.tsx)
- [設計系統規範](/tailwind.config.ts)
- [Framer Motion 文件](https://www.framer.com/motion/)

## 維護者

- 實作日期：2025-11-26
- 版本：1.0.0
- 狀態：已完成 ✓
