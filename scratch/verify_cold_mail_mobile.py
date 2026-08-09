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

        await page.route("**/api/user/me", lambda r: r.fulfill(
            status=200, content_type="application/json",
            body='{"id":"1","email":"zmonemrahman@gmail.com","is_admin":true,"plan":"enterprise","is_approved":true,"free_emails_sent":0}'
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
            
            document.querySelectorAll('#app-page .view').forEach(el => el.style.setProperty('display', 'none', 'important'));
            const coldMail = document.getElementById('cold-mail-builder');
            if (coldMail) {
                coldMail.style.setProperty('display', 'block', 'important');
                coldMail.classList.add('active');
            }
        }''')
        await asyncio.sleep(2)

        await page.screenshot(path=os.path.join(artifacts_dir, "cold_mail_mobile_fixed.png"))
        print("Captured cold_mail_mobile_fixed.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
