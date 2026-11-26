import { Page, expect } from '@playwright/test';

export class AuthPage {
  constructor(readonly page: Page) {}
  async register(email: string, password = 'StrongPass!123') {
    await this.page.goto('/signup');
    await this.page.getByRole('textbox', { name: 'Name', exact: true }).fill('Roman Moroz');
    await this.page.getByRole('textbox', { name: 'Email', exact: true }).fill(email);
    await this.page.getByLabel('Password', { exact: true }).fill(password);
    await this.page.getByRole('button', { name: 'Sign Up', exact: true }).click();
    await expect(this.page).toHaveURL(/\/login$/);
  }
  async login(email: string, password = 'StrongPass!123') {
    await this.page.goto('/login');
    await this.page.getByRole('textbox', { name: 'Email', exact: true }).fill(email);
    await this.page.getByLabel('Password', { exact: true }).fill(password);
    await this.page.getByRole('button', { name: 'Login', exact: true }).click();
  }
}

export class CatalogPage {
  constructor(readonly page: Page) {}
  async search(query: string) { await this.page.getByRole('textbox', { name: 'Search products' }).fill(query); }
  async addHoodie() {
    await this.page.goto('/products');
    const product = this.page.getByTestId('product-p1');
    await product.getByRole('combobox').selectOption('M');
    await product.getByRole('button', { name: 'Add Cart' }).click();
    await expect(this.page.getByText('Added to cart', { exact: true })).toBeVisible();
  }
}

export class CartPage {
  constructor(readonly page: Page) {}
  async open() { await this.page.goto('/cart'); }
  async checkout(email: string) {
    await this.page.getByRole('button', { name: 'Proceed to Checkout' }).click();
    for (const [field, value] of Object.entries({ firstName: 'Roman', lastName: 'Moroz', email,
      address: 'Test street 10', city: 'Moscow', pinCode: '101000' })) {
      await this.page.getByLabel(field, { exact: true }).fill(value);
    }
    await this.page.getByRole('button', { name: 'Place Order' }).click();
    await expect(this.page.getByRole('heading', { name: 'Order Placed Successfully!' })).toBeVisible();
    await expect(this.page.getByTestId('order-address')).toContainText('Test street 10, Moscow, 101000');
  }
}
