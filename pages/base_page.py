# pages/base_page.py
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

    # def handle_keep_open_modal_if_present(self, timeout_sec=1):
    #     """
    #     Verifica e clica em 'Manter aberto' se o modal de 'Caixa Aberto Identificado!' aparecer.
    #     """
    #     modal_header_selector = 'header.sc-60baa1a1-0:has-text("Caixa Aberto Identificado!")'
    #     keep_open_button_selector = 'button.sc-60baa1a1-4:has-text("Manter aberto")'

    #     # Espera um curto período para o modal aparecer
    #     try:
    #         self.page.wait_for_selector(modal_header_selector, state="visible", timeout=timeout_sec * 1000)
    #         if self.page.is_visible(modal_header_selector):
    #             print("Modal 'Caixa Aberto Identificado!' detectado. Clicando em 'Manter aberto'.")
    #             self.click(keep_open_button_selector)
    #             return True
    #     except PlaywrightTimeoutError:
    #         # Modal não apareceu, o que é normal na maioria das vezes
    #         pass
    #     except Exception as e:
    #         print(f"Erro ao tentar lidar com o modal 'Manter aberto': {e}")
    #     return False
