import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should display the landing page', async ({ page }) => {
    await page.goto('/');
    
    // Check for main heading
    await expect(page.getByRole('heading', { name: /Carte/i })).toBeVisible();
    
    // Check for login button
    await expect(page.getByRole('button', { name: /登入/i })).toBeVisible();
  });

  test('should have proper meta tags', async ({ page }) => {
    await page.goto('/');
    
    // Check title
    await expect(page).toHaveTitle(/Carte AI/);
    
    // Check meta description
    const metaDescription = page.locator('meta[name="description"]');
    await expect(metaDescription).toHaveAttribute('content', /Carte AI/);
  });
});
