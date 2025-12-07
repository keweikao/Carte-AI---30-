import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.E2E_BASE_URL || 'http://localhost:3000';
const webCommand = process.env.E2E_WEB_COMMAND;

export default defineConfig({
  testDir: './',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['list'], ['html', { outputFolder: 'tests/e2e/results/html' }], ['junit', { outputFile: 'tests/e2e/results/junit/results.xml' }]],
  use: {
    baseURL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: webCommand
    ? {
        command: webCommand,
        url: baseURL,
        reuseExistingServer: true,
        stdout: 'ignore',
        stderr: 'pipe',
      }
    : undefined,
});
