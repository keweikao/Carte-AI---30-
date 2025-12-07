# 響應式設計修正說明

## 已完成的修正

### 1. 首頁 (src/app/page.tsx)
- ✅ 減少小螢幕上的 padding 和 gap
- ✅ 調整卡片內邊距為響應式
- ✅ 優化標題文字大小

### 2. BrandHeader 組件 (src/components/brand-header.tsx)
- ✅ 添加響應式文字大小
- ✅ 條件性換行（小螢幕不換行，大螢幕換行）

## 待應用的修正

### 3. 輸入頁 (src/app/input/page.tsx)

需要手動應用以下修改：

**第 320 行：** 將預算標籤和切換器改為響應式佈局
```tsx
// 原始碼
<div className="flex justify-between items-center">

// 修改為
<div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
```

**第 325-336 行：** 調整按鈕內邊距
```tsx
// 將兩個 button 的 className 中的 px-3 改為 px-2 sm:px-3
className={`px-2 sm:px-3 py-1 text-xs rounded-md transition-all ${budgetType === "person" ? "bg-white shadow-sm text-foreground font-medium" : "text-muted-foreground"}`}
```

**第 349-355 行：** 優化價格顯示區域
```tsx
// 原始碼
<div className="flex justify-between text-xs text-muted-foreground px-1">
    <span>NT$ 0</span>
    <div className="font-mono text-sm font-semibold text-primary rounded-full bg-primary/10 px-3 py-1">
        NT$ {Number(formData.budget).toLocaleString() || "0"}
    </div>
    <span>NT$ {budgetType === 'person' ? "3,000+" : "10,000+"}</span>
</div>

// 修改為
<div className="flex justify-between items-center text-xs text-muted-foreground px-1 gap-2">
    <span className="text-[10px] sm:text-xs">NT$ 0</span>
    <div className="font-mono text-xs sm:text-sm font-semibold text-primary rounded-full bg-primary/10 px-2 sm:px-3 py-1">
        NT$ {Number(formData.budget).toLocaleString() || "0"}
    </div>
    <span className="text-[10px] sm:text-xs whitespace-nowrap">NT$ {budgetType === 'person' ? "3,000+" : "10,000+"}</span>
</div>
```

### 4. 推薦頁 (src/app/recommendation/page.tsx)

**第 511-516 行：** 優化頂部導航按鈕
```tsx
// 原始碼
<div className="container flex h-14 items-center justify-between px-4">
    <Button variant="ghost" onClick={handleBackToSettings} className="gap-2"><ArrowLeft className="w-4 h-4" />返回設定</Button>
    <Button onClick={() => allDecided && alert("導航到最終菜單頁")} disabled={!allDecided} className="gap-2 bg-primary hover:bg-primary/90">
        <Check className="w-4 h-4" />產出點餐菜單
    </Button>
</div>

// 修改為
<div className="container flex h-14 items-center justify-between px-2 sm:px-4 gap-2">
    <Button variant="ghost" onClick={handleBackToSettings} className="gap-1 sm:gap-2 text-sm sm:text-base px-2 sm:px-4">
        <ArrowLeft className="w-4 h-4" />
        <span className="hidden xs:inline">返回設定</span>
        <span className="xs:hidden">返回</span>
    </Button>
    <Button onClick={() => allDecided && alert("導航到最終菜單頁")} disabled={!allDecided} className="gap-1 sm:gap-2 bg-primary hover:bg-primary/90 text-sm sm:text-base px-2 sm:px-4">
        <Check className="w-4 h-4" />
        <span className="hidden xs:inline">產出點餐菜單</span>
        <span className="xs:hidden">產出</span>
    </Button>
</div>
```

**第 519-530 行：** 優化價格摘要區域
```tsx
// 在 <div className="bg-background/95 backdrop-blur-sm sticky top-14 z-10 px-6 py-4 shadow-sm border-b"> 中
// 將 px-6 改為 px-4 sm:px-6

<div className="bg-background/95 backdrop-blur-sm sticky top-14 z-10 px-4 sm:px-6 py-4 shadow-sm border-b">
    <div className="flex justify-between items-end mb-2">
        <div>
            <p className="text-xs text-muted-foreground mb-1 uppercase tracking-wider">菜單總價</p>
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground font-mono transition-colors duration-300">NT$ {totalPrice.toLocaleString()}</h1>
        </div>
        <div className="text-right">
            <p className="text-xs text-muted-foreground mb-1">人均約</p>
            <p className="text-lg sm:text-xl font-bold text-orange-600 font-mono">NT$ {perPerson.toLocaleString()}</p>
        </div>
    </div>
</div>
```

### 5. 菜單頁 (src/app/menu/page.tsx)

**第 291-310 行：** 優化頂部工具列
```tsx
// 原始碼
<div className="container flex h-14 items-center justify-between px-4">
    <Button variant="ghost" onClick={handleBack} className="gap-2">
        <ArrowLeft className="w-4 h-4" />
        返回修改
    </Button>
    <div className="flex gap-2">
        <Button variant="outline" onClick={handlePrint} className="gap-2">
            <Printer className="w-4 h-4" />
            列印
        </Button>
        <Button variant="outline" onClick={handleShare} className="gap-2">
            <Share2 className="w-4 h-4" />
            分享
        </Button>
        <Button onClick={handleRating} className="gap-2 bg-primary">
            <Star className="w-4 h-4" />
            評分
        </Button>
    </div>
</div>

// 修改為
<div className="container flex h-14 items-center justify-between px-2 sm:px-4 gap-2">
    <Button variant="ghost" onClick={handleBack} className="gap-1 sm:gap-2 px-2 sm:px-4">
        <ArrowLeft className="w-4 h-4" />
        <span className="hidden sm:inline">返回修改</span>
        <span className="sm:hidden">返回</span>
    </Button>
    <div className="flex gap-1 sm:gap-2">
        <Button variant="outline" onClick={handlePrint} className="gap-1 sm:gap-2 px-2 sm:px-4">
            <Printer className="w-4 h-4" />
            <span className="hidden md:inline">列印</span>
        </Button>
        <Button variant="outline" onClick={handleShare} className="gap-1 sm:gap-2 px-2 sm:px-4">
            <Share2 className="w-4 h-4" />
            <span className="hidden md:inline">分享</span>
        </Button>
        <Button onClick={handleRating} className="gap-1 sm:gap-2 bg-primary px-2 sm:px-4">
            <Star className="w-4 h-4" />
            <span className="hidden md:inline">評分</span>
        </Button>
    </div>
</div>
```

**第 324-330 行：** 優化標題
```tsx
// 將標題改為響應式
<h1 className="text-3xl sm:text-4xl font-bold text-foreground mb-2 font-display">
    {menu.restaurant_name}
</h1>
```

**第 342-344 行：** 優化價格顯示
```tsx
<h2 className="text-2xl sm:text-3xl font-bold text-foreground font-mono">
    NT$ {menu.total_price.toLocaleString()}
</h2>
```

## 測試檢查清單

### iPhone SE (375px)
- [ ] 首頁：登入卡片不溢出，文字大小適中
- [ ] 輸入頁：預算切換器正常顯示，價格範圍不重疊
- [ ] 推薦頁：導航按鈕不重疊，價格摘要清晰
- [ ] 菜單頁：工具列按鈕正常顯示

### iPhone 14 Pro (393px)
- [ ] 所有頁面：佈局正常，無橫向滾動
- [ ] 文字大小適中，可讀性良好

### iPad (768px)
- [ ] 首頁：兩欄佈局開始顯示
- [ ] 所有按鈕和文字恢復正常大小

### Desktop (1280px, 1920px)
- [ ] 首頁：完整的兩欄佈局
- [ ] 所有元素充分利用空間
- [ ] 文字和按鈕大小最佳化
