import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const runUI = !!process.env.E2E_RUN_UI;
const baseDir = __dirname;
const locators = JSON.parse(fs.readFileSync(path.join(baseDir, '__fixtures__', 'locators.json'), 'utf-8'));

test.describe('UI flow (mock login + recommendation)', () => {
  test.skip(!runUI, 'Set E2E_RUN_UI=1 to run UI flow tests.');

  test('user can reach input and see recommendations', async ({ page }) => {
    await page.goto('/');
    if (locators.landing?.heroTitle) {
      await expect(page.locator(locators.landing.heroTitle)).toBeVisible();
    }

    // 使用 error=mock_bypass 以略過未登入自動跳轉（前端判斷 unauth + !error 才會 redirect）
    await page.goto('/input?error=mock_bypass');

    // V2.3: Step 1 - Restaurant Search
    const restaurantField = page.locator(locators.input.restaurantField);
    await expect(restaurantField).toBeVisible();
    await restaurantField.fill('測試餐廳');

    // Wait a bit for restaurant selection to register
    await page.waitForTimeout(500);

    // V2.3: Step 2 - Mode Selection (auto-proceeds with default "sharing")
    // Click "Next" button to proceed to step 3
    const nextButton1 = page.locator('button:has-text("下一步")');
    await expect(nextButton1).toBeVisible({ timeout: 5000 });
    await nextButton1.click();

    // V2.3: Step 3 - People Count (auto-proceeds with default "2")
    // Click "Next" button to proceed to step 4
    await page.waitForTimeout(300);
    const nextButton2 = page.locator('button:has-text("下一步")');
    await expect(nextButton2).toBeVisible({ timeout: 5000 });
    await nextButton2.click();

    // V2.3: Step 4 - Occasion + Dietary (final step)
    // Now the submit button should appear
    await page.waitForTimeout(300);
    const submit = page.locator(locators.input.submitButton);
    await expect(submit).toBeVisible({ timeout: 10000 });
    await expect(submit).toBeEnabled();
  });
});
