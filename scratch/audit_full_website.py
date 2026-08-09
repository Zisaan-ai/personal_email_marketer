import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        artifacts_dir = os.path.dirname(os.path.abspath(__file__))

        # Desktop Viewport Audit (1920x1080)
        context_desktop = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page_desktop = await context_desktop.new_page()
        await page_desktop.goto("https://xcomic.xyz", wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # 1. Take desktop full topbar screenshot
        await page_desktop.screenshot(path=os.path.join(artifacts_dir, "desktop_topbar.png"))
        print("Captured desktop_topbar.png")

        # 2. Check hamburger button visibility on desktop
        toggle_visible = await page_desktop.evaluate('''() => {
            const el = document.getElementById('landing-nav-toggle');
            if (!el) return false;
            const style = window.getComputedStyle(el);
            return style.display !== 'none' && style.visibility !== 'hidden';
        }''')
        print(f"Desktop hamburger button visible: {toggle_visible} (Should be False)")

        # 3. Check desktop nav links visibility
        links_visible = await page_desktop.evaluate('''() => {
            const el = document.querySelector('.landing-nav-links');
            if (!el) return false;
            const style = window.getComputedStyle(el);
            return style.display !== 'none';
        }''')
        print(f"Desktop nav links visible: {links_visible} (Should be True)")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
