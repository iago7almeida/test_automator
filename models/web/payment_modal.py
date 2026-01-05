from playwright.sync_api import Page, expect
from models.web.base_page import BasePage
import re 

class PaymentModal(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Definimos os dois possíveis pais
        self.modal_order_balcony = page.locator("div.ReactModal__Content")
        self.modal_mesa = page.locator("div").filter(has_text="Selecione a forma de pagamento").last 
        self.modal_content = self.modal_order_balcony.or_(self.modal_mesa)

        # Agora podemos encadear os botões sem erro, pois self.modal_content sempre existe
        self.btn_money = self.modal_content.locator("button", has_text="Dinheiro")
        self.btn_pix = self.modal_content.locator("button", has_text="Pix")
        self.btn_debit = self.modal_content.locator("button", has_text="Débito")
        self.btn_credit = self.modal_content.locator("button", has_text="Crédito")
        
        # Input de valor
        self.input_value = self.modal_content.locator("input").first
        
        # Botões de ação
        self.btn_launch = self.modal_content.locator("button", has_text="Lançar")
        self.btn_finalize = self.page.locator("button", has_text="Finalizar Comanda")
        self.btn_confirm = self.modal_content.locator("button", has_text="Confirmar")
        self.btn_cancel_modal = self.modal_content.locator("button", has_text="Cancelar").last
        self.missing_amount_text = self.modal_content.locator("div", has_text="Falta pagar").last


    def select_payment_method(self, method: str):
        print(f"💳 Selecionando Aba: {method}")
 
        try:
            expect(self.modal_content).to_be_visible(timeout=10000)
        except AssertionError:
            # Se falhar, tira um print para vermos o que está na tela
            print("ERRO: Modal não abriu a tempo.")
            self.page.screenshot(path="erro_modal_nao_abriu.png")
            raise

        if method.lower() == "dinheiro": self.btn_money.click()       
        elif method.lower() == "pix": self.btn_pix.click()       
        elif method.lower() == "débito" or method.lower() == "debito": self.btn_debit.click()       
        elif method.lower() == "crédito": self.btn_credit.click()
        
        else:
            raise ValueError(f"Método de pagamento não reconhecido: {method}")

    def fill_amount(self, amount: str):
        print(f"✍️ Digitando valor: {amount}")
        self.input_value.click()
        self.input_value.press("ControlOrMeta+a")
        self.page.wait_for_timeout(100)
        self.input_value.fill(amount) 

    def launch_payment(self):
        print("🚀 Clicando Lançar")
        expect(self.btn_launch).to_be_enabled()
        self.btn_launch.click()
        # Pequena espera para animação do lançamento
        self.page.wait_for_timeout(500)

    def get_remaining_amount(self) -> str:
        # Adicionei um wait aqui, pois às vezes o cálculo demora uns milissegundos
        self.missing_amount_text.wait_for()
        return self.missing_amount_text.inner_text().replace("Falta pagar", "").replace("\xa0", " ").strip()

    def finalize_order_sheet(self):
        print("Finalizando conta...")
        expect(self.btn_finalize).to_be_enabled(timeout=15000)
        print(self.btn_finalize.is_visible())
        self.btn_finalize.click()

    def confirm_payment(self):
        self.btn_confirm.click()
        expect(self.modal_content).to_be_hidden(timeout=10000)