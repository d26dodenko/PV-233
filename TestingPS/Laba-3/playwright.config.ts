import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const repoRoot = fileURLToPath(new URL('../../', import.meta.url));

export default defineConfig({
  testDir: './e2e',
  outputDir: resolve(repoRoot, 'test-results'),
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: process.env.CI ? 2 : undefined,
  timeout: 30_000,
  expect: { timeout: 7_000 },
  reporter: [['list'], ['html', { outputFolder: resolve(repoRoot, 'artifacts/playwright/html'), open: 'never' }],
    ['junit', { outputFile: resolve(repoRoot, 'artifacts/playwright/junit.xml') }]],
  use: { baseURL: 'http://127.0.0.1:3000', browserName: 'chromium',
    screenshot: 'on', trace: 'retain-on-failure', video: 'retain-on-failure' },
  webServer: { command: process.env.SHOP_EXECUTABLE || 'cargo run --locked', cwd: repoRoot, url: 'http://127.0.0.1:3000/api/health',
    timeout: 120_000, reuseExistingServer: false },
});
