# pages/login_page.py
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = 'input[name="email"]'
    PASSWORD_INPUT = 'input[name="password"]'
    SUBMIT_BUTTON = 'button[type="submit"]'
    LOGIN_URL = "https://gestao.pigz.dev/"

    def navigate_to_login_page(self):
        self.navigate(self.LOGIN_URL)
        # Ajustar o zoom pode ser parte de uma fixture de setup do browser
        # ou chamado aqui se for específico desta página.
        self.page.evaluate("document.body.style.zoom='80%'")

    def login(self, email, password):
        print(f"Preenchendo email: {email}")
        self.fill(self.EMAIL_INPUT, email)
        print("Preenchendo senha")
        self.fill(self.PASSWORD_INPUT, password)
        print("Clicando no botão de submit")
        self.click(self.SUBMIT_BUTTON)
        # É uma boa prática esperar por um elemento da próxima página para confirmar o login
        # Por exemplo, esperar pelo dashboard ou menu principal.
        # self.wait_for_selector("SELETOR_DO_DASHBOARD_APOS_LOGIN")