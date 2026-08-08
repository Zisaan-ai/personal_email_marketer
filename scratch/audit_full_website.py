import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        artifacts_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Test 1: Mobile Landing Page Drawer
        context_landing = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'
        )
        page_landing = await context_landing.new_page()
        await page_landing.goto("https://xcomic.xyz", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        # Click landing nav toggle
        toggle = page_landing.locator("#landing-nav-toggle")
        if await toggle.count() > 0:
            await toggle.click()
            await asyncio.sleep(1)
            await page_landing.screenshot(path=os.path.join(artifacts_dir, "landing_drawer_open.png"))
            print("Captured landing_drawer_open.png")

        # Test 2: Logged-In App Page Sub-Views Audit
        context_app = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'
        )
        page_app = await context_app.new_page()
        await page_app.goto("https://xcomic.xyz", wait_until="domcontentloaded")
        
        # Inject token
        await page_app.evaluate('''() => {
            localStorage.setItem("xcomic_token", "dummy_test_token");
            localStorage.setItem("token", "dummy_test_token");
            location.reload();
        }''')
        await page_app.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(2)

        # Audit app views
        views = ['overview', 'campaigns', 'leads', 'inbox', 'accounts', 'analytics', 'settings']
        for v in views:
            try:
                # Click nav link or switch tab via JS
                await page_app.evaluate(f'''(viewId) => {{
                    if (typeof window.switchNavTab === 'function') window.switchNavTab(viewId);
                }}''', v)
                await asyncio.sleep(1)
                await page_app.screenshot(path=os.path.join(artifacts_dir, f"app_view_{v}.png"), full_page=False)
                
                # Check for overflows in this view
                overflow_info = await page_app.evaluate('''() => {
                    const bodyWidth = document.documentElement.clientWidth;
                    const overflowing = [];
                    document.querySelectorAll('#app-page *').forEach(el => {
                        const rect = el.getBoundingClientRect();
                        if (rect.right > bodyWidth + 5 || rect.left < -5) {
                            overflowing.push({
                                tagName: el.tagName,
                                className: (el.className || '').toString(),
                                width: Math.round(rect.width),
                                left: Math.round(rect.left),
                                right: Math.round(rect.right)
                            });
                        }
                    });
                    return overflowing.slice(0, 10);
                }''')
                print(f"View '{v}' - Overflow items: {len(overflow_info)}")
                for item in overflow_info:
                    print(f"  [{v} overflow]:", item)

            except Exception as e:
                print(f"Error auditing view {v}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
