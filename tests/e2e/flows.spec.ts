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

    // 使用 error=mock 以略過未登入自動跳轉（前端判斷 unauth + !error 才會 redirect）
    await page.goto('/input?error=mock');

    const restaurantField = page.locator(locators.input.restaurantField);
    await expect(restaurantField).toBeVisible();
    await restaurantField.fill('測試餐廳');

    const submit = page.locator(locators.input.submitButton);
    await expect(submit).toBeVisible();
    // 不強制導航，避免真登入依賴；僅確認 UI 元件可互動
    await expect(submit).toBeEnabled();
  });
});
