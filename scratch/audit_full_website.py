import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        artifacts_dir = os.path.dirname(os.path.abspath(__file__))

        context_app = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'
        )
        page_app = await context_app.new_page()

        # Mock API calls so dashboard loads fully without 401 redirect
        await page_app.route("**/api/user/me", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id":"1","email":"zmonemrahman@gmail.com","is_admin":true,"plan":"enterprise","is_approved":true,"free_emails_sent":0}'
        ))
        await page_app.route("**/api/stats", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"emails_sent_today":142,"deliverability":99.2,"replies":18,"bounces":1,"sending_accounts_count":5}'
        ))
        await page_app.route("**/api/sending-accounts*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='[{"id":"1","email":"outreach@xcomic.xyz","provider":"smtp","status":"active","daily_limit":1000,"sent_today":142}]'
        ))
        await page_app.route("**/api/campaigns*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='[{"id":"1","name":"Q3 SaaS Founders Prospecting","status":"running","sent":540,"replies":32,"open_rate":68.4}]'
        ))

        # Set auth storage
        await page_app.goto("https://xcomic.xyz", wait_until="domcontentloaded")
        await page_app.evaluate('''() => {
            localStorage.setItem('xcomic_token', 'mock_admin_token');
            localStorage.setItem('token', 'mock_admin_token');
            localStorage.setItem('user', JSON.stringify({ id: '1', is_admin: true, email: 'zmonemrahman@gmail.com', plan: 'enterprise' }));
            localStorage.setItem('is_admin', 'true');
            localStorage.setItem('user_plan', 'enterprise');
            location.reload();
        }''')
        await page_app.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        # Audit app tabs
        views = ['overview', 'campaigns', 'leads', 'inbox', 'accounts', 'analytics', 'settings']
        for v in views:
            try:
                await page_app.evaluate(f'''(tName) => {{
                    const btn = document.querySelector('[data-view="' + tName + '"]') || document.querySelector('#nav-' + tName);
                    if (btn) btn.click();
                    else if (typeof window.switchNavTab === 'function') window.switchNavTab(tName);
                }}''', v)
                await asyncio.sleep(1)
                await page_app.screenshot(path=os.path.join(artifacts_dir, f"app_mocked_{v}.png"))
                print(f"Captured app_mocked_{v}.png")
            except Exception as e:
                print(f"Error capturing view {v}: {e}")

        # Also open mobile sidebar inside dashboard
        await page_app.evaluate('''() => {
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            if (sidebar) sidebar.classList.add('open');
            if (overlay) overlay.classList.add('show');
        }''')
        await asyncio.sleep(1)
        await page_app.screenshot(path=os.path.join(artifacts_dir, "app_mocked_sidebar.png"))
        print("Captured app_mocked_sidebar.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
