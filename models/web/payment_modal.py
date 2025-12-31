from playwright.sync_api import Page, expect
from models.web.base_page import BasePage

class PaymentModal(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.modal_content = page.locator("div.ReactModal__Content")
        
        # Botões de Método
        self.btn_money = self.modal_content.get_by_role("button", name="Dinheiro")
        self.btn_pix = self.modal_content.get_by_role("button", name="Pix")
        self.btn_debit = self.modal_content.get_by_role("button", name="Débito")
        self.btn_credit = self.modal_content.get_by_role("button", name="Crédito")
        
        # --- CORREÇÃO DE LOCATOR ---
        # Usamos .first porque dentro do modal, o input de Valor é SEMPRE o primeiro.
        # Funciona para Pix (que só tem 1) e Dinheiro (onde ele é o 1º de 2).
        self.input_value = self.modal_content.locator("input").first
        
        self.btn_launch = self.modal_content.get_by_role("button", name="Lançar")
        self.btn_confirm = self.modal_content.get_by_role("button", name="Confirmar")
        self.btn_cancel_modal = self.modal_content.get_by_role("button", name="Cancelar").last
        self.missing_amount_text = self.modal_content.locator("div", has_text="Falta pagar").last

    def select_payment_method(self, method: str):
        print(f"💳 Aba: {method}")
        if method.lower() == "dinheiro": self.btn_money.click()
        elif method.lower() == "pix": self.btn_pix.click()
        elif method.lower() == "débito": self.btn_debit.click()
        elif method.lower() == "crédito": self.btn_credit.click()

    def fill_amount(self, amount: str):
        """
        Estratégia do Codegen: Click -> Ctrl+A -> Fill
        """
        print(f"✍️ Digitando valor: {amount}")
        self.input_value.click()
        # Seleciona tudo para garantir que sobrescreve
        self.input_value.press("ControlOrMeta+a")
        # Pequena pausa para garantir que o evento de seleção ocorreu
        self.page.wait_for_timeout(100)
        self.input_value.fill(amount) 

    def launch_payment(self):
        print("🚀 Clicando Lançar")
        self.btn_launch.click()
        self.page.wait_for_timeout(500)

    def get_remaining_amount(self) -> str:
        return self.missing_amount_text.inner_text().replace("Falta pagar", "").replace("\xa0", " ").strip()

    def confirm_payment(self):
        self.btn_confirm.click()
        expect(self.modal_content).to_be_hidden(timeout=5000)