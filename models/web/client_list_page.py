from playwright.sync_api import Page, expect

from .base_page import BasePage


class ClientListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.current_balance_text = self.page.locator('span[color="#E0453E"]')
        self.payment_modal_input = self.page.get_by_label("Informe o valor")
        self.confirm_payment_button = self.page.get_by_role("button", name="Receber pagamento")
        self.firt_client_row_path = page.locator('//*[@id="__next"]/div/main/table/tbody/tr[1]')
        self.search_client_input = page.locator('//*[@id="__next"]/div/main/div/div[2]/div/div/div/div/input')

    def select_first_client(self):
        print("Primeiro cliente selecionado.")

    def select_client_by_name(self, client_name: str):
        self.search_client_input.fill(client_name)
        client_result = self.page.locator('//*[@id="__next"]/div/main/table/tbody/tr/td[3]')
        expect(client_result).to_be_visible()
        client_result.click()
