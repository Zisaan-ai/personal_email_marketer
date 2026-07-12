import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to login...")
        await page.goto("https://xcomic.xyz")
        await page.wait_for_selector("#login-email")
        await page.fill("#login-email", "zmonemrahman@gmail.com")
        await page.fill("#login-pass", "76008972")
        await page.click("#login-btn")
        print("Logged in, waiting...")
        await page.wait_for_timeout(3000)
        
        # Take a screenshot to see where we are
        await page.screenshot(path="after_login.png")
        print("Taking screenshot after login...")
        
        # In case there's an issue with clicking the tab directly, let's force JS execution
        print("Navigating to Cold Mail Builder via JS...")
        await page.evaluate("window.navTo('cold-mail-builder')")
        await page.wait_for_timeout(1000)
        
        await page.screenshot(path="builder.png")
        print("Filling out cold mail form using robust JS evaluation...")
        await page.evaluate("document.getElementById('inst-subject').value = 'Test Subject UI Playwright';")
        await page.evaluate("document.getElementById('inst-body').value = 'Test Body UI Playwright';")
        await page.evaluate("document.getElementById('campaign-delay-min').value = '0';")
        await page.evaluate("document.getElementById('campaign-delay-max').value = '0';")
        await page.evaluate("document.getElementById('seq-leads').value = 'test@test.com, Test Name, Test Co';")
        await page.evaluate("if(window.saveLeads) window.saveLeads('seq-leads');")
        
        print("Clicking Launch Campaign...")
        await page.click("#inst-send-seq-btn")
        
        print("Waiting for 5 seconds for redirection...")
        await page.wait_for_timeout(5000)
        
        await page.screenshot(path="after_launch.png")
        
        text = await page.content()
        if "Test Subject UI Playwright" in text:
            print("SUCCESS: Campaign appeared in the list without refresh!")
        else:
            print("FAILED: Campaign did NOT appear in the list.")
        
        await browser.close()

asyncio.run(main())
