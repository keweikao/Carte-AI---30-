import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const runUI = !!process.env.E2E_RUN_UI;
const baseDir = __dirname;
const locators = JSON.parse(fs.readFileSync(path.join(baseDir, '__fixtures__', 'locators.json'), 'utf-8'));

test.describe('UI flow (mock login + recommendation)', () => {
  test.skip(!runUI, 'Set E2E_RUN_UI=1 to run UI flow tests.');

  test('user can reach input and see recommendations', async ({ page }) => {
    // Mock the autocomplete API to ensure listbox appears in test environment
    await page.route('**/places/autocomplete*', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          suggestions: [{
            description: '測試餐廳 Mock',
            place_id: 'mock-place-1',
            main_text: '測試餐廳 Mock',
            secondary_text: 'Mock Address'
          }]
        })
      });
    });

    await page.goto('/');
    if (locators.landing?.heroTitle) {
      await expect(page.locator(locators.landing.heroTitle)).toBeVisible();
    }

    // 使用 error=mock_bypass 以略過未登入自動跳轉（前端判斷 unauth + !error 才會 redirect）
    await page.goto('/input?error=mock_bypass');

    // V2.3: Step 1 - Restaurant Search
    const restaurantField = page.locator(locators.input.restaurantField);
    await expect(restaurantField).toBeVisible();

    // Use type() instead of fill() to trigger onChange events properly
    await restaurantField.click();
    await restaurantField.type('測試餐廳');

    // Wait for autocomplete suggestions (listbox) and select the first option
    // This ensures place_id is set, which is required for the "Next" button to be enabled
    const suggestionList = page.getByRole('listbox');
    await expect(suggestionList).toBeVisible({ timeout: 10000 });

    const firstOption = page.getByRole('option').first();
    await firstOption.click();

    // Wait for state update
    await page.waitForTimeout(500);

    // Check if "下一步" button appears (it should if step 1 is valid)
    const nextButton1 = page.locator('button:has-text("下一步")').first();
    await expect(nextButton1).toBeVisible({ timeout: 5000 });
    await nextButton1.click();

    // V2.3: Step 2 - Mode Selection
    // Wait for step 2 to render
    await page.waitForTimeout(500);

    // Step 2 should show mode options, but "下一步" should be visible immediately (has default)
    const nextButton2 = page.locator('button:has-text("下一步")').first();
    await expect(nextButton2).toBeVisible({ timeout: 5000 });
    await nextButton2.click();

    // V2.3: Step 3 - People Count
    await page.waitForTimeout(500);

    // Step 3 should show people count, "下一步" should be visible (has default 2)
    const nextButton3 = page.locator('button:has-text("下一步")').first();
    await expect(nextButton3).toBeVisible({ timeout: 5000 });
    await nextButton3.click();

    // V2.3: Step 4 - Occasion + Dietary (final step)
    // Now the submit button should appear instead of "下一步"
    await page.waitForTimeout(500);
    const submit = page.locator(locators.input.submitButton);
    await expect(submit).toBeVisible({ timeout: 10000 });
    await expect(submit).toBeEnabled();
  });
});
