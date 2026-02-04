import logging
from playwright.sync_api import Page, expect
from models.web.base_page import BasePage
from models.web.payment_page import PaymentPage

class PaymentModal(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Definimos os dois possíveis pais
        self.modal_order_balcony = page.get_by_role("dialog", name="Confirmar pagamento")
        self.modal_mesa = page.locator("div").filter(has_text="Selecione o tipo de pagamento").last
        self.modal_content = self.modal_order_balcony.or_(self.modal_mesa)

        self.btn_money = self.modal_content.locator("button", has_text="Dinheiro")
        self.btn_pix = self.modal_content.locator("button", has_text="Pix")
        self.btn_debit = self.modal_content.locator("button", has_text="Débito")
        self.btn_credit = self.modal_content.locator("button", has_text="Crédito")

        # Input de valor
        self.input_value = self.modal_content.locator("input").first

        # Botões de ação
        self.btn_launch = self.modal_content.locator("button", has_text="Lançar")
        self.btn_finalize = self.page.locator("button", has_text="Finalizar Comanda")
        self.btn_confirm = page.locator("button", has_text="Confirmar")
        self.btn_cancel_modal = self.modal_content.locator("button", has_text="Cancelar").last
        self.missing_amount_text = page.locator("div", has_text="Falta pagar").last


    def select_payment_method(self, method: str):
        logging.info(f"💳 Selecionando Aba: {method}")

        try:
            expect(self.modal_content).to_be_visible(timeout=10000)
        except AssertionError:
            logging.info("ERRO: Modal não abriu a tempo.")
            raise
        if method.lower() == "dinheiro":
            self.btn_money.click()
        elif method.lower() == "pix":
            self.btn_pix.click()
        elif method.lower() == "débito":
            self.btn_debit.click()
        elif method.lower() == "crédito":
            self.btn_credit.click()

        else:
            raise ValueError(f"Método de pagamento não reconhecido: {method}")

    def fill_amount(self, amount: str):
        logging.info(f"✍️ Digitando valor: {amount}")
        self.input_value.click()
        self.input_value.press("ControlOrMeta+a")
        self.page.wait_for_timeout(100)
        self.input_value.fill(amount)

    def launch_payment(self):
        try:
            self.btn_launch.wait_for(state="visible", timeout=6000)
        except:
            logging.info("⚠️ Botão 'Lançar' não foi encontrado.")
            return
        if self.btn_launch.is_disabled():
            logging.info("✅ O valor já está pago (Botão Lançar inativo). Pulando etapa...")
            return
        logging.info("🚀 Clicando Lançar")
        self.btn_launch.click()
        self.page.wait_for_timeout(5000)

    def get_remaining_amount(self) -> str:
        self.missing_amount_text.wait_for(state="visible", timeout=2000)
        return self.missing_amount_text.inner_text().replace("Falta pagar", "").replace("\xa0", " ").strip()

    def finalize_order_sheet(self):
        logging.info("Finalizando conta...")
        expect(self.btn_finalize).to_be_enabled(timeout=15000)
        logging.info(self.btn_finalize.is_visible())
        self.btn_finalize.click()

    def confirm_payment(self):
        payment_page = PaymentPage(self.page)
        logging.info("Ciicando em confirmar/enviar...")
        self.btn_confirm.click()
        payment_page.handle_fiscal_note_modal_if_appears()
        self.modal_content.wait_for(state="hidden", timeout=10000)

    def remove_staged_payment(self):
        logging.info("Aqui na remoção")
