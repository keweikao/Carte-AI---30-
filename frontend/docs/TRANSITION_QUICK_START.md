# Page Transitions - Quick Start Guide

## ✅ Already Implemented

Page transitions are **automatically enabled** for all pages. No additional setup required!

## How It Works

1. **`template.tsx`** in `/src/app/` wraps all pages with `PageTransition`
2. Transitions activate on route navigation (/, /input, /recommendation, /menu)
3. Direction-aware animations (slides forward/backward based on route order)
4. Automatically respects `prefers-reduced-motion` for accessibility

## Test the Transitions

### Quick Test
1. Start the dev server: `npm run dev`
2. Navigate: Home → Input → Recommendation → Menu
3. Use browser back button to see reverse animations

### Test Reduced Motion
**Enable system setting:**
- macOS: System Settings → Accessibility → Display → Reduce motion
- Windows: Settings → Ease of Access → Display → Show animations (OFF)

You should see simple fade animations instead of sliding animations.

## Using Animation Components

### SlideInUp (for cards, sections)
```tsx
import { SlideInUp } from "@/components/page-transition";

<SlideInUp delay={0.2}>
  <Card>Your content</Card>
</SlideInUp>
```

### FadeIn (for text, subtle animations)
```tsx
import { FadeIn } from "@/components/page-transition";

<FadeIn delay={0.1} duration={0.5}>
  <p>Fades in smoothly</p>
</FadeIn>
```

### StaggerContainer + StaggerItem (for lists)
```tsx
import { StaggerContainer, StaggerItem } from "@/components/page-transition";

<StaggerContainer staggerDelay={0.1}>
  {items.map(item => (
    <StaggerItem key={item.id}>
      <DishCard dish={item} />
    </StaggerItem>
  ))}
</StaggerContainer>
```

### ScaleIn (for emphasis)
```tsx
import { ScaleIn } from "@/components/page-transition";

<ScaleIn delay={0.1}>
  <Button>Important Action</Button>
</ScaleIn>
```

## Demo Page

Visit `/transition-demo` to see all animations in action.

## Performance Tips

✅ **Good**: Using transform and opacity (GPU accelerated)
```tsx
<motion.div animate={{ x: 100, opacity: 0.5 }} />
```

❌ **Bad**: Animating layout properties (causes reflow)
```tsx
<motion.div animate={{ width: 100, height: 100 }} />
```

## Animation Presets

Import from `@/lib/animation-utils`:

```tsx
import { DURATION, EASING, fadeInVariants } from "@/lib/animation-utils";

<motion.div
  variants={fadeInVariants}
  transition={{ duration: DURATION.base, ease: EASING.inOut }}
/>
```

## Troubleshooting

### Animations feel janky?
- Check for heavy re-renders during transition
- Wrap heavy components in `React.memo()`
- Use browser DevTools Performance panel to identify bottlenecks

### Transitions not working?
- Verify Framer Motion is installed: `npm list framer-motion`
- Check browser console for errors
- Ensure `"use client"` is at top of client components

### Want different animation for a specific page?
Create a custom template in that page's folder:
```tsx
// app/special-page/template.tsx
"use client";
export default function Template({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      {children}
    </motion.div>
  );
}
```

## Browser Support

✅ Chrome 90+ | ✅ Firefox 88+ | ✅ Safari 14+ | ✅ Edge 90+

Older browsers get instant navigation (graceful degradation).

## More Info

- Full documentation: `docs/PAGE_TRANSITIONS.md`
- Design system: `DESIGN_SYSTEM.md`
- Demo page: `/transition-demo`
