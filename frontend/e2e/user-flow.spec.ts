import { test, expect } from '@playwright/test';

test.describe('User Flow', () => {
  test.skip('complete user journey from input to menu', async ({ page }) => {
    // Note: This test is skipped because it requires authentication
    // To run this test, you need to set up authentication in Playwright
    
    await page.goto('/');
    
    // 1. Login (would need to be implemented with actual auth)
    // await page.click('text=登入');
    
    // 2. Navigate to input page
    await page.goto('/input');
    
    // 3. Fill in preferences
    await page.fill('input[name="restaurant"]', '鼎泰豐');
    await page.fill('input[name="partySize"]', '4');
    await page.fill('input[name="budget"]', '2000');
    
    // 4. Submit and go to recommendation page
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/recommendation/);
    
    // 5. Select dishes
    const selectButtons = page.locator('button:has-text("我要點")');
    const count = await selectButtons.count();
    for (let i = 0; i < Math.min(count, 3); i++) {
      await selectButtons.nth(i).click();
    }
    
    // 6. Complete and go to menu page
    await page.click('button:has-text("完成點餐")');
    await expect(page).toHaveURL(/\/menu/);
    
    // 7. Verify menu page shows selected dishes
    await expect(page.locator('text=推薦菜色')).toBeVisible();
  });

  test('navigation works correctly', async ({ page }) => {
    await page.goto('/');
    
    // Test navigation to different pages
    const pages = ['/input', '/recommendation', '/menu'];
    
    for (const path of pages) {
      await page.goto(path);
      await expect(page).toHaveURL(path);
    }
  });
});
