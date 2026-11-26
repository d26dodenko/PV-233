import { test, expect } from '@playwright/test';
import { randomUUID } from 'node:crypto';
import { AuthPage, CatalogPage, CartPage } from './pages.js';

test('UI-01 регистрация → вход → поиск → корзина → заказ → выход', async ({ page }) => {
  const email = `qa-${randomUUID()}@example.test`;
  const auth = new AuthPage(page);
  await auth.register(email);
  await auth.login(email);
  await expect(page).toHaveURL('http://127.0.0.1:3000/');
  const catalog = new CatalogPage(page);
  await catalog.search('rust');
  await expect(page.getByTestId('product-p1')).toBeVisible();
  await expect(page.getByTestId('product-p2')).toHaveCount(0);
  await catalog.addHoodie();
  const cart = new CartPage(page); await cart.open();
  await expect(page.getByText('Rust Hoodie', { exact: true })).toBeVisible();
  await expect(page.getByText('Total:', { exact: false })).toContainText('80');
  await cart.checkout(email);
  await page.screenshot({ path: 'artifacts/playwright/order-success.png', fullPage: true });
  await cart.open();
  await expect(page.getByText('Your cart is empty', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Logout', exact: true }).click();
  await expect(page).toHaveURL(/\/login$/);
  await page.goto('/cart'); await expect(page).toHaveURL(/\/login$/);
});

test('UI-02 неверный пароль не создаёт сессию', async ({ page }) => {
  const email = `qa-${randomUUID()}@example.test`; const auth = new AuthPage(page);
  await auth.register(email); await auth.login(email, 'WrongPass!123');
  await expect(page.getByText('Invalid credentials', { exact: true })).toBeVisible();
  await expect(page).toHaveURL(/\/login$/);
  expect(await page.evaluate(() => localStorage.getItem('token'))).toBeNull();
});

test('UI-03 поиск без результатов и очистка фильтра', async ({ page }) => {
  const response = await page.goto('/products');
  expect(response?.status()).toBe(200);
  const catalog = new CatalogPage(page);
  await catalog.search('nonexistent-product');
  await expect(page.getByRole('status')).toHaveText('No products found');
  await catalog.search(''); await expect(page.locator('[data-testid^="product-"]')).toHaveCount(3);
});

test('UI-04 гость не добавляет товар в корзину', async ({ page }) => {
  await page.goto('/products');
  await page.getByTestId('product-p1').getByRole('button', { name: 'Add Cart' }).click();
  await expect(page.getByText('Please log in to add items to cart.', { exact: true })).toBeVisible();
  await page.goto('/checkout'); await expect(page).toHaveURL(/\/login$/);
});

test('UI-05 повторная регистрация показывает ошибку', async ({ page }) => {
  const email = `qa-${randomUUID()}@example.test`; await new AuthPage(page).register(email);
  await page.goto('/signup');
  await page.getByRole('textbox', { name: 'Name', exact: true }).fill('Another user');
  await page.getByRole('textbox', { name: 'Email', exact: true }).fill(email);
  await page.getByLabel('Password', { exact: true }).fill('StrongPass!123');
  await page.getByRole('button', { name: 'Sign Up', exact: true }).click();
  await expect(page.getByText('Email already registered', { exact: true })).toBeVisible();
  await expect(page).toHaveURL(/\/signup$/);
});

test('UI-06 удаление последней позиции очищает корзину', async ({ page }) => {
  const email = `qa-${randomUUID()}@example.test`; const auth = new AuthPage(page);
  await auth.register(email); await auth.login(email); await expect(page).toHaveURL('http://127.0.0.1:3000/');
  await new CatalogPage(page).addHoodie(); await new CartPage(page).open();
  await page.getByRole('button', { name: 'Remove Rust Hoodie' }).click();
  await expect(page.getByText('Your cart is empty', { exact: true })).toBeVisible();
});
