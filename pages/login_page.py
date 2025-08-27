from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        
        self.page = page

        self.email_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.get_by_role('button', name='Entrar')     


    def navigate(self):

        self.page.goto("https://gestor.pigz.com.br/sign-in")


    def login(self, email, password): 

        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()