import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        artifacts_dir = os.path.dirname(os.path.abspath(__file__))

        context_mobile = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'
        )
        page = await context_mobile.new_page()

        # Mock API calls
        await page.route("**/api/user/me", lambda r: r.fulfill(
            status=200, content_type="application/json",
            body='{"id":"1","email":"zmonemrahman@gmail.com","is_admin":true,"plan":"enterprise","is_approved":true,"free_emails_sent":0}'
        ))
        await page.route("**/api/stats", lambda r: r.fulfill(
            status=200, content_type="application/json",
            body='{"emails_sent_today":142,"deliverability":99.2,"replies":18,"bounces":1,"sending_accounts_count":5}'
        ))
        await page.route("**/api/sending-accounts*", lambda r: r.fulfill(
            status=200, content_type="application/json",
            body='[{"id":"1","email":"outreach@xcomic.xyz","provider":"smtp","status":"active","daily_limit":1000,"sent_today":142}]'
        ))
        await page.route("**/api/campaigns*", lambda r: r.fulfill(
            status=200, content_type="application/json",
            body='[{"id":"1","name":"Q3 SaaS Founders Prospecting","status":"running","sent":540,"replies":32,"open_rate":68.4}]'
        ))

        await page.goto("https://xcomic.xyz", wait_until="domcontentloaded")
        await page.evaluate('''() => {
            localStorage.setItem('xcomic_token', 'mock_admin_token');
            localStorage.setItem('token', 'mock_admin_token');
            localStorage.setItem('user', JSON.stringify({ id: '1', is_admin: true, email: 'zmonemrahman@gmail.com', plan: 'enterprise' }));
            localStorage.setItem('is_admin', 'true');
            localStorage.setItem('user_plan', 'enterprise');
            
            const landing = document.getElementById('landing-page');
            const authPage = document.getElementById('auth-page');
            const app = document.getElementById('app-page');
            
            if (landing) landing.style.setProperty('display', 'none', 'important');
            if (authPage) authPage.style.setProperty('display', 'none', 'important');
            if (app) {
                app.style.setProperty('display', 'flex', 'important');
                app.classList.add('on');
            }
            if (typeof window.APP_INIT === 'function') window.APP_INIT();
        }''')
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        # Inspect all views
        views_to_test = [
            'overview', 'campaigns', 'cold-mail-builder', 'campaigns-builder',
            'leads', 'inbox', 'accounts', 'analytics', 'settings'
        ]

        for v in views_to_test:
            await page.evaluate(f'''(viewId) => {{
                document.querySelectorAll('#app-page .view').forEach(el => {{
                    el.style.setProperty('display', 'none', 'important');
                    el.classList.remove('active');
                }});
                const target = document.getElementById(viewId) || document.getElementById('view-' + viewId);
                if (target) {{
                    target.style.setProperty('display', 'block', 'important');
                    target.classList.add('active');
                }}
            }}''', v)
            await asyncio.sleep(1)

            # Check overflow elements
            overflows = await page.evaluate('''() => {
                const bodyWidth = document.documentElement.clientWidth;
                const items = [];
                document.querySelectorAll('#app-page *').forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > bodyWidth + 2 || rect.left < -2) {
                        items.push({
                            tagName: el.tagName,
                            id: el.id,
                            className: el.className.toString(),
                            right: Math.round(rect.right),
                            bodyWidth: bodyWidth
                        });
                    }
                });
                return items.slice(0, 5);
            }''')

            print(f"VIEW '{v}': Overflows = {len(overflows)}")
            for item in overflows:
                print(f"   Overflow item in {v}: {item}")

            await page.screenshot(path=os.path.join(artifacts_dir, f"bug_mobile_{v}.png"))

        # Test Sidebar open state
        await page.evaluate('''() => {
            const btn = document.querySelector('.mobile-menu-btn') || document.getElementById('mobile-menu-btn');
            if (btn) btn.click();
            else {
                document.querySelector('.sidebar').classList.add('open');
                document.querySelector('.sidebar-overlay').classList.add('show');
            }
        }''')
        await asyncio.sleep(1)
        await page.screenshot(path=os.path.join(artifacts_dir, "bug_mobile_sidebar.png"))
        print("Captured bug_mobile_sidebar.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
