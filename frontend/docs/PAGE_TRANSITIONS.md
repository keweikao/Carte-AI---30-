# Page Transition System

## Overview

The OderWhat application implements smooth page transitions using Framer Motion, following the design system specifications defined in `DESIGN_SYSTEM.md`.

## Architecture

### Core Components

1. **`page-transition.tsx`** - Main transition wrapper and utility components
2. **`template.tsx`** - Next.js App Router template for page-level transitions
3. **`globals.css`** - Global CSS with accessibility support

## Features

### ✅ Implemented

- **Direction-aware transitions**: Slides forward/backward based on route order
- **Design system compliance**: Uses specified timing (100-800ms) and easing curves
- **Accessibility**: Full `prefers-reduced-motion` support
- **Performance**: GPU-accelerated animations using transform properties
- **Browser compatibility**: Works on all modern browsers

### 🎨 Animation Variants

#### Page Transitions
- **Duration**: 300ms (design system `--duration-base`)
- **Easing**: `cubic-bezier(0.4, 0, 0.2, 1)` (design system `--ease-in-out`)
- **Effects**: Opacity + horizontal slide + subtle scale

#### Reduced Motion
- **Duration**: 100ms (design system `--duration-instant`)
- **Effects**: Opacity fade only (no movement or scale)

## Usage

### Automatic Page Transitions

All pages automatically get transitions via `template.tsx`. No additional setup needed.

```tsx
// Page components work automatically
export default function MyPage() {
  return <div>Content</div>;
}
```

### Route Order

The system determines transition direction based on this flow:

```
/ (Home) → /input → /recommendation → /menu
```

- Forward navigation: slides in from right
- Backward navigation: slides in from left

### Utility Components

#### SlideInUp
Animate content sliding up from below:

```tsx
import { SlideInUp } from "@/components/page-transition";

<SlideInUp delay={0.1}>
  <Card>Content</Card>
</SlideInUp>
```

#### FadeIn
Simple fade animation:

```tsx
import { FadeIn } from "@/components/page-transition";

<FadeIn delay={0.2} duration={0.5}>
  <p>Fades in smoothly</p>
</FadeIn>
```

#### ScaleIn
Scale animation for emphasis:

```tsx
import { ScaleIn } from "@/components/page-transition";

<ScaleIn delay={0.1}>
  <Button>Emphasized button</Button>
</ScaleIn>
```

#### Stagger Animations
Animate lists with staggered timing:

```tsx
import { StaggerContainer, StaggerItem } from "@/components/page-transition";

<StaggerContainer staggerDelay={0.1}>
  {items.map(item => (
    <StaggerItem key={item.id}>
      <Card>{item.content}</Card>
    </StaggerItem>
  ))}
</StaggerContainer>
```

## Design System Alignment

### Timing Values

| Animation | Duration | CSS Variable | Usage |
|-----------|----------|--------------|-------|
| Page transition | 300ms | `--duration-base` | Route changes |
| Instant feedback | 100ms | `--duration-instant` | Reduced motion |
| Fast animation | 200ms | `--duration-fast` | Hover effects |
| Slow animation | 500ms | `--duration-slow` | Special effects |

### Easing Curves

| Type | Bezier | CSS Variable | Usage |
|------|--------|--------------|-------|
| In-Out | `cubic-bezier(0.4, 0, 0.2, 1)` | `--ease-in-out` | Page transitions |
| Out | `cubic-bezier(0, 0, 0.2, 1)` | `--ease-out` | Entering elements |
| In | `cubic-bezier(0.4, 0, 1, 1)` | `--ease-in` | Exiting elements |

## Accessibility

### Reduced Motion Support

The system respects `prefers-reduced-motion` at multiple levels:

1. **CSS Global**: `globals.css` disables all animations globally
2. **Component Level**: Each component checks motion preference
3. **Fallback**: Simple fade instead of complex animations

### Testing Reduced Motion

**macOS:**
```
System Settings → Accessibility → Display → Reduce motion
```

**Windows:**
```
Settings → Ease of Access → Display → Show animations
```

**Browser DevTools:**
```css
/* Chrome/Edge DevTools */
Command Menu (Cmd+Shift+P) → "Emulate CSS prefers-reduced-motion"
```

## Browser Compatibility

### Supported Browsers

| Browser | Version | Support Level |
|---------|---------|---------------|
| Chrome | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 90+ | ✅ Full |
| Mobile Safari | 14+ | ✅ Full |
| Chrome Mobile | 90+ | ✅ Full |

### Fallback Behavior

Older browsers gracefully degrade to instant navigation (no animation).

## Performance

### Optimization Techniques

1. **GPU Acceleration**: Uses `transform` and `opacity` only
2. **Will-Change**: Automatically applied by Framer Motion
3. **Layout Shift Prevention**: Animations don't trigger reflow
4. **Concurrent Rendering**: Compatible with React 19's concurrent features

### Performance Metrics

- **FCP (First Contentful Paint)**: < 1.5s
- **LCP (Largest Contentful Paint)**: < 2.5s
- **Animation Frame Rate**: 60fps on modern devices
- **JS Bundle Impact**: ~20KB (Framer Motion is already included)

## Testing

### Manual Testing Checklist

- [ ] Navigate forward through all routes (/ → /input → /recommendation → /menu)
- [ ] Navigate backward through all routes
- [ ] Test with reduced motion enabled
- [ ] Test on mobile devices
- [ ] Test on slow 3G network
- [ ] Verify no layout shifts during transitions
- [ ] Check animation smoothness (60fps)

### Automated Testing

```bash
# Build the application
npm run build

# Test in production mode
npm run start
```

### Performance Testing

Use Chrome DevTools:
1. Open Performance panel
2. Record a navigation
3. Verify animations run at 60fps
4. Check for layout thrashing

## Troubleshooting

### Issue: Janky animations

**Solution**: Check for heavy renders during transition
```tsx
// Wrap heavy components in React.memo
const HeavyComponent = React.memo(({ data }) => {
  // expensive rendering
});
```

### Issue: Animations don't work

**Checklist**:
1. Verify Framer Motion is installed: `npm list framer-motion`
2. Check browser console for errors
3. Ensure `"use client"` directive is present in client components
4. Verify route order in `routeOrder` object

### Issue: Reduced motion not working

**Solution**: Test media query detection
```tsx
// Debug helper
useEffect(() => {
  const matches = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  console.log("Reduced motion:", matches);
}, []);
```

## Future Enhancements

### Potential Additions

- [ ] Shared element transitions (when browser support improves)
- [ ] Gesture-based navigation with swipe detection
- [ ] Custom transition per route
- [ ] Transition sound effects (optional)
- [ ] More complex animation orchestrations

### View Transitions API

The native [View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API) is not yet widely supported (Chrome 111+). When support improves, consider:

```tsx
// Future implementation
if (document.startViewTransition) {
  document.startViewTransition(() => {
    router.push('/next-page');
  });
}
```

## References

- [Framer Motion Documentation](https://www.framer.com/motion/)
- [Next.js App Router](https://nextjs.org/docs/app)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [WCAG 2.1 Animation Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)

---

**Last Updated**: 2025-01-26
**Maintainer**: Frontend Team
**Version**: 1.0.0
