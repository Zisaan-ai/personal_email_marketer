import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        artifacts_dir = os.path.dirname(os.path.abspath(__file__))

        # Test 1: Desktop Viewport Check (1920x1080)
        context_desktop = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page_desktop = await context_desktop.new_page()
        await page_desktop.goto("https://xcomic.xyz", wait_until="domcontentloaded")
        await asyncio.sleep(1)
        await page_desktop.screenshot(path=os.path.join(artifacts_dir, "desktop_final.png"))
        print("Captured desktop_final.png")

        # Test 2: Mobile Visual Builder & Dashboard Check (375x812)
        context_mobile = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'
        )
        page_mobile = await context_mobile.new_page()
        
        await page_mobile.route("**/api/user/me", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id":"1","email":"zmonemrahman@gmail.com","is_admin":true,"plan":"enterprise","is_approved":true,"free_emails_sent":0}'
        ))
        
        await page_mobile.goto("https://xcomic.xyz", wait_until="domcontentloaded")
        await page_mobile.evaluate('''() => {
            localStorage.setItem('xcomic_token', 'mock_admin_token');
            localStorage.setItem('token', 'mock_admin_token');
            localStorage.setItem('user', JSON.stringify({ id: '1', is_admin: true, email: 'zmonemrahman@gmail.com', plan: 'enterprise' }));
            localStorage.setItem('is_admin', 'true');
            localStorage.setItem('user_plan', 'enterprise');
            location.reload();
        }''')
        await page_mobile.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        await page_mobile.screenshot(path=os.path.join(artifacts_dir, "mobile_dashboard_final.png"))
        print("Captured mobile_dashboard_final.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
