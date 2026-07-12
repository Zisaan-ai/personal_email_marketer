import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        with open('frontend/assets/app.js', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i in range(1, len(lines) + 1):
            code = "".join(lines[:i])
            err = await page.evaluate(f"""(code) => {{
                try {{
                    new Function(code);
                    return null;
                }} catch(e) {{
                    return e.name + ': ' + e.message;
                }}
            }}""", code)
            
            if err and "await is only valid" in err:
                print(f"FOUND ERROR AT LINE {i}:")
                print(lines[i-1].strip())
                break
                
        await browser.close()

asyncio.run(run())
