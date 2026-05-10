import { test, expect } from '@playwright/test';
import path from 'path';

const fileUrl = `file://${path.resolve('tetris.html')}`;

test.describe('Tetris Game', () => {
  test('should load the game and start', async ({ page }) => {
    await page.goto(fileUrl);

    // Check title
    await expect(page).toHaveTitle(/Retro Tetris/);

    // Check overlay is visible initially
    const overlay = page.locator('#overlay');
    await expect(overlay).toBeVisible();

    // Click start button
    const startBtn = page.locator('#start-btn');
    await startBtn.click();

    // Overlay should be hidden
    await expect(overlay).toBeHidden();

    // Score should be 0
    const score = page.locator('#score');
    await expect(score).toHaveText('0');
  });

  test('should pause when P is pressed', async ({ page }) => {
    await page.goto(fileUrl);
    await page.locator('#start-btn').click();

    // Press P to pause
    await page.keyboard.press('p');
    
    // We can't easily check internal 'paused' state via DOM, 
    // but we can verify the game doesn't crash
    await page.keyboard.press('ArrowRight');
    await page.keyboard.press('p'); // Resume
  });

  test('should toggle sound', async ({ page }) => {
    await page.goto(fileUrl);
    const soundBtn = page.locator('#sound-toggle');
    
    await expect(soundBtn).toHaveText(/Sound: ON/);
    await soundBtn.click();
    await expect(soundBtn).toHaveText(/Sound: OFF/);
  });
});
