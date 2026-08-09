import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        d = os.path.dirname(os.path.abspath(__file__))

        ctx = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'
        )
        page = await ctx.new_page()

        await page.route("**/api/user/me", lambda r: r.fulfill(status=200, content_type="application/json",
            body='{"id":"1","email":"zmonemrahman@gmail.com","is_admin":true,"plan":"enterprise","is_approved":true,"free_emails_sent":0}'))
        await page.route("**/api/stats", lambda r: r.fulfill(status=200, content_type="application/json",
            body='{"emails_sent_today":142,"deliverability":99.2,"replies":18,"bounces":1,"sending_accounts_count":5}'))
        await page.route("**/api/sending-accounts*", lambda r: r.fulfill(status=200, content_type="application/json",
            body='[{"id":"1","email":"outreach@xcomic.xyz","provider":"smtp","status":"active","daily_limit":1000,"sent_today":142}]'))
        await page.route("**/api/campaigns*", lambda r: r.fulfill(status=200, content_type="application/json",
            body='[{"id":"1","name":"Q3 SaaS Founders","status":"running","sent":540,"replies":32,"open_rate":68.4,"type":"cold_mail"}]'))

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
            if (app) { app.style.setProperty('display', 'flex', 'important'); app.classList.add('on'); }
        }''')
        await asyncio.sleep(2)

        # Capture each view
        views = ['dashboard', 'campaigns-builder', 'cold-mail-builder', 'cold-mail-list', 'campaigns-list', 'sending-accounts', 'settings', 'unsubscribes', 'ai-replies']
        for v in views:
            await page.evaluate(f'''(viewId) => {{
                document.querySelectorAll('#app-page .view').forEach(el => {{
                    el.classList.remove('active');
                    el.style.removeProperty('display');
                }});
                const target = document.getElementById(viewId);
                if (target) {{
                    target.classList.add('active');
                    target.style.setProperty('display', 'block', 'important');
                }}
            }}''', v)
            await asyncio.sleep(1)
            # Full page scroll screenshot
            await page.screenshot(path=os.path.join(d, f"audit_{v}.png"), full_page=True)
            print(f"Captured audit_{v}.png")

            # Also check for overflow issues
            overflows = await page.evaluate('''() => {
                const bw = document.documentElement.clientWidth;
                const items = [];
                document.querySelectorAll('*').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0 && r.right > bw + 5) {
                        const cs = el.className ? el.className.toString().substring(0, 60) : '';
                        items.push({ tag: el.tagName, id: el.id, cls: cs, right: Math.round(r.right), bw: bw });
                    }
                });
                return items.slice(0, 8);
            }''')
            if overflows:
                print(f"  OVERFLOW in {v}: {len(overflows)} elements")
                for o in overflows:
                    print(f"    {o}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
