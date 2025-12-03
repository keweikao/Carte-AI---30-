import { test, expect, request } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const runApi = !!process.env.E2E_RUN_API;
const apiBase = process.env.E2E_API_URL || process.env.E2E_BASE_URL || 'http://localhost:3000';
const authHeader = process.env.E2E_AUTH_HEADER || 'Bearer fake-token';
const fixtureOpenApi = path.join(process.cwd(), 'tests/e2e/__fixtures__/openapi.json');

test.describe('API smoke (mock-friendly)', () => {
  test.skip(!runApi, 'Set E2E_RUN_API=1 to run API smoke tests against a mock-enabled backend.');

  test('OpenAPI fixture contains recommendations paths', async () => {
    test.skip(!fs.existsSync(fixtureOpenApi), 'OpenAPI fixture not found; run python tests/e2e/export_openapi.py');
    const schema = JSON.parse(fs.readFileSync(fixtureOpenApi, 'utf-8'));
    expect(schema.paths['/api/v1/recommend/v2']).toBeTruthy();
    expect(schema.paths['/api/v1/recommend/v2/alternatives']).toBeTruthy();
  });

  test('POST /api/v1/recommend/v2 returns items', async () => {
    const ctx = await request.newContext({ baseURL: apiBase });
    const payload = {
      restaurant_name: '測試餐廳',
      dining_style: 'Shared',
      party_size: 2,
      budget: { type: 'Total', amount: 1200 },
      dish_count_target: 2,
      preferences: [],
    };

    const res = await ctx.post('/api/v1/recommend/v2', {
      data: payload,
      headers: {
        'Content-Type': 'application/json',
        Authorization: authHeader,
      },
      timeout: 30_000,
    });

    if (!res.ok()) {
      console.log('API Error Status:', res.status());
      console.log('API Error Body:', await res.text());
    }
    expect(res.ok()).toBeTruthy();
    const json = await res.json();
    expect(Array.isArray(json.items)).toBeTruthy();
    expect(json.items.length).toBeGreaterThan(0);
  });

  test('GET /api/v1/recommend/v2/alternatives returns list', async () => {
    const ctx = await request.newContext({ baseURL: apiBase });
    const res = await ctx.get('/api/v1/recommend/v2/alternatives', {
      params: {
        recommendation_id: 'test-rec-id',
        category: '熱菜',
        exclude: ['宮保雞丁'],
      },
      headers: {
        Authorization: authHeader,
      },
      timeout: 20_000,
    });

    expect(res.status()).toBe(200);
    const json = await res.json();
    expect(Array.isArray(json)).toBeTruthy();
  });
});
