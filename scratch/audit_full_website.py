import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        artifacts_dir = os.path.dirname(os.path.abspath(__file__))

        context = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'
        )
        page = await context.new_page()
        await page.goto("https://xcomic.xyz", wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # 1. Take screenshot of closed topbar (should show Logo + Sign In + Get Started + ☰ on same line)
        await page.screenshot(path=os.path.join(artifacts_dir, "topbar_single_line.png"))
        print("Captured topbar_single_line.png")

        # 2. Click ☰ hamburger toggle
        toggle_btn = page.locator("#landing-nav-toggle")
        if await toggle_btn.count() > 0:
            await toggle_btn.click()
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(artifacts_dir, "drawer_opened_by_click.png"))
            print("Captured drawer_opened_by_click.png")
        else:
            print("ERROR: #landing-nav-toggle not found!")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
