import asyncio
from playwright.async_api import async_playwright

# change the path if your chrome install is somewhere else 
# (like in appdata/local/google/chrome/application/chrome.exe)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


class Browser:
    def __init__(self, page):
        self.page = page

    async def open(self, url):
        await self.page.goto(url)
        print(f"Opened: {url}")

    async def get_title(self):
        return await self.page.title()

    async def get_url(self):
        return self.page.url

    async def click(self, selector):
        await self.page.locator(selector).click()
        print(f"Clicked: {selector}")

    async def type(self, selector, text):
        await self.page.locator(selector).fill(text)
        print(f"Typed: {text}")

    async def press(self, selector, key):
        await self.page.locator(selector).press(key)
        print(f"Pressed: {key}")

    async def get_text(self):
        return await self.page.locator("body").inner_text()


async def main():
    async with async_playwright() as p:

        # Launch installed Chrome
        browser = await p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=False,
            slow_mo=300
        )

        page = await browser.new_page()

        # Create our browser controller
        browser_controller = Browser(page)

        # -------------------------------------------------
        # TEST
        # -------------------------------------------------

        await browser_controller.open("https://www.google.com")

        print("Title:", await browser_controller.get_title())
        print("URL:", await browser_controller.get_url())

        # Google search
        search_box = "textarea[name='q']"

        await browser_controller.type(
            search_box,
            "Python Playwright tutorial"
        )

        await browser_controller.press(
            search_box,
            "Enter"
        )

        await page.wait_for_load_state("domcontentloaded")

        print("\nSearch completed!")
        print("Title:", await browser_controller.get_title())
        print("URL:", await browser_controller.get_url())

        print("\n--- PAGE TEXT ---")
        text = await browser_controller.get_text()
        print(text[:3000])

        input("\nPress Enter to close...")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())