from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click(self, selector: str, **kwargs):
        self.page.click(selector, **kwargs)

    def fill(self, selector: str, text: str, **kwargs):
        self.page.fill(selector, text, **kwargs)

    def navigate(self, url: str):
        self.page.goto(url)

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: int = 5000):
        try:
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            print(f"Timeout esperando pelo seletor: {selector} com estado: {state}")
            return False
