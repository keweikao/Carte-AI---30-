# Browser Compatibility Testing Checklist

## Test Plan for Page Transitions (FE-034)

### Target Browsers

| Browser | Version | Priority | Status |
|---------|---------|----------|--------|
| Chrome | 90+ | High | ⏳ |
| Safari | 14+ | High | ⏳ |
| Firefox | 88+ | Medium | ⏳ |
| Edge | 90+ | Medium | ⏳ |
| Mobile Safari | 14+ | High | ⏳ |
| Chrome Mobile | 90+ | High | ⏳ |

### Testing Scenarios

#### 1. Basic Page Transitions
- [ ] Navigate: Home → Input (should slide forward)
- [ ] Navigate: Input → Recommendation (should slide forward)
- [ ] Navigate: Recommendation → Menu (should slide forward)
- [ ] Back button: Menu → Recommendation (should slide backward)
- [ ] Back button: Recommendation → Input (should slide backward)
- [ ] Back button: Input → Home (should slide backward)

**Expected**: Smooth 300ms slide animation with fade

#### 2. Animation Performance
- [ ] Open DevTools Performance panel
- [ ] Record page navigation
- [ ] Verify animations run at 60fps
- [ ] Check no layout shifts occur
- [ ] Verify no janky frames

**Tools**: Chrome DevTools → Performance → Record

#### 3. Reduced Motion Support
- [ ] Enable system reduced motion setting
- [ ] Navigate between pages
- [ ] Verify simple fade animation (no slide)
- [ ] Duration should be ~100ms instead of 300ms

**How to enable**:
- macOS: System Settings → Accessibility → Display → Reduce motion
- Windows: Settings → Ease of Access → Display → Show animations (OFF)
- Linux: System Settings → Accessibility → Reduce animation

#### 4. Mobile Testing
- [ ] Test on iOS Safari (iPhone)
- [ ] Test on Chrome Mobile (Android)
- [ ] Test landscape and portrait orientations
- [ ] Verify swipe-back gesture works correctly
- [ ] Check touch interactions don't conflict with animations

#### 5. Network Conditions
- [ ] Test on Fast 3G network throttling
- [ ] Test on Slow 3G network throttling
- [ ] Verify animations don't feel stuttery on slow connections
- [ ] Check page doesn't flash white during transition

**Chrome DevTools**: Network tab → Throttling dropdown

#### 6. Animation Component Tests
Visit `/transition-demo` and verify:
- [ ] SlideInUp components animate correctly
- [ ] FadeIn components animate correctly
- [ ] ScaleIn components animate correctly
- [ ] Stagger animations work sequentially
- [ ] Conditional rendering shows enter/exit animations
- [ ] All animations respect reduced motion

#### 7. Edge Cases
- [ ] Rapid navigation (click links quickly)
- [ ] Navigation during ongoing animation
- [ ] Browser back/forward during animation
- [ ] Refresh page during animation
- [ ] Deep link directly to /menu page

#### 8. Accessibility
- [ ] Keyboard navigation works correctly
- [ ] Focus is maintained during transitions
- [ ] Screen reader announces page changes
- [ ] No flashing/strobing effects (WCAG 2.1)
- [ ] Animations can be disabled globally

### Performance Benchmarks

#### Target Metrics
- **Animation FPS**: 60fps (16.67ms per frame)
- **CPU Usage**: < 50% during animation
- **Memory**: No memory leaks after 20 page transitions
- **Bundle Size Impact**: ~20KB (Framer Motion)

#### Measuring Tools
```bash
# Build production bundle
npm run build

# Check bundle size
npm run build && ls -lh .next/static/chunks

# Lighthouse performance test
npx lighthouse http://localhost:3000 --view
```

### Browser-Specific Issues

#### Safari
- [ ] Check will-change property support
- [ ] Verify no flickering on transform animations
- [ ] Test backdrop-filter performance

#### Firefox
- [ ] Verify cubic-bezier easing works correctly
- [ ] Check transform-origin behavior
- [ ] Test composite layers

#### Mobile Safari
- [ ] Check momentum scrolling during animation
- [ ] Verify touch-action works correctly
- [ ] Test safe-area-inset-bottom

### Regression Testing

After any animation code changes, verify:
- [ ] No console errors
- [ ] No TypeScript errors
- [ ] Build completes successfully
- [ ] All existing animations still work
- [ ] Performance hasn't degraded

### Known Limitations

1. **View Transitions API**: Not used (Chrome 111+ only)
   - Fallback: Framer Motion animations

2. **Older Browsers**: Graceful degradation to instant navigation
   - IE11: Not supported
   - Chrome < 90: No animations
   - Safari < 14: No animations

3. **Animation Conflicts**:
   - Don't animate width/height (causes reflow)
   - Don't animate position properties
   - Stick to transform and opacity

### Debugging Tips

#### Check animation is running
```tsx
<motion.div
  onAnimationStart={() => console.log("Animation started")}
  onAnimationComplete={() => console.log("Animation completed")}
/>
```

#### Check reduced motion detection
```tsx
useEffect(() => {
  const matches = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  console.log("Reduced motion:", matches);
}, []);
```

#### Performance debugging
```tsx
// Add to component
useEffect(() => {
  let frameCount = 0;
  let lastTime = performance.now();

  const measureFPS = () => {
    frameCount++;
    const currentTime = performance.now();
    if (currentTime >= lastTime + 1000) {
      console.log(`FPS: ${frameCount}`);
      frameCount = 0;
      lastTime = currentTime;
    }
    requestAnimationFrame(measureFPS);
  };

  measureFPS();
}, []);
```

### Test Report Template

```
# Page Transition Test Report

**Date**: YYYY-MM-DD
**Tester**: [Name]
**Browser**: [Chrome 121.0 / Safari 17.2 / etc]
**Platform**: [macOS Sonoma / Windows 11 / iOS 17]

## Test Results

### Basic Transitions: ✅ PASS / ❌ FAIL
- Home → Input: [PASS/FAIL]
- Input → Recommendation: [PASS/FAIL]
- Recommendation → Menu: [PASS/FAIL]
- Back navigation: [PASS/FAIL]

### Performance: ✅ PASS / ❌ FAIL
- Average FPS: [60fps]
- Animation smoothness: [PASS/FAIL]
- No layout shifts: [PASS/FAIL]

### Accessibility: ✅ PASS / ❌ FAIL
- Reduced motion works: [PASS/FAIL]
- Keyboard navigation: [PASS/FAIL]
- Focus management: [PASS/FAIL]

### Issues Found
1. [Description of issue]
   - Steps to reproduce: [...]
   - Expected: [...]
   - Actual: [...]

### Screenshots/Videos
[Attach if applicable]

### Conclusion
[Overall assessment]
```

### Sign-off

When all tests pass:
- [ ] All browsers tested
- [ ] Performance metrics met
- [ ] Accessibility verified
- [ ] Documentation updated
- [ ] Ready for production ✅

---

**Testing completed by**: _____________
**Date**: _____________
**Approved by**: _____________
