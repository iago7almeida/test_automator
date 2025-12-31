from time import sleep

from playwright.sync_api import Page, expect


class PaymentPage:
    def __init__(self, page: Page):
        self.page = page

        self.submit_button = page.get_by_role("button", name="Lançar")
        self.send_order_button = page.get_by_role("button", name="Enviar Pedido")

    def select_payment_method(self, method: str):
        payment_button = self.page.get_by_role("button", name=method, exact=True)
        expect(payment_button).to_be_visible()
        payment_button.click()

    def select_other_sub_method(self, sub_method):
        other_sub_method_button = self.page.locator("#paymentMethod")
        expect(other_sub_method_button).to_be_visible()
        other_sub_method_button.click()
        select_sub_method = self.page.locator(f"p[title='{sub_method}']")
        expect(select_sub_method).to_be_visible(timeout=3000)
        select_sub_method.click()
        sleep(2)

    def launch_order(self):
        sleep(1)
        self.submit_button.click()

        no_payment_message = self.page.get_by_text("Nenhum pagamento adicionado")
        expect(no_payment_message).to_be_hidden(timeout=15000)
        print("Botão 'lançar' clicado. Aguardando 'Enviar Pedido' ser habilitado...")
        expect(self.send_order_button).to_be_enabled(timeout=10000)
        print("'Eviar pedido' está habilidado. Prosseguindo...")

    def send_order(self):
        expect(self.send_order_button).to_be_enabled()
        self.send_order_button.click()

    def handle_delivery_fee(self):
        insertion_fee_button = self.page.get_by_role("button", name="Adicionar taxa")
        try:
            expect(insertion_fee_button).to_be_visible(timeout=5000)
            insertion_fee_button.click()
        
        except Exception:
            print("Modal não apareceu ou foi comprometido")

    def handle_fiscal_note_modal_if_appears(self):
        close_modal_button = self.page.get_by_role("button", name="Cancelar")

        try:
            expect(close_modal_button).to_be_visible(timeout=5000)
            print("Modal de nota fiscal encontrado. Fechando...")
            close_modal_button.click()
        except Exception:
            print("Modal de nota fiscal não apareceu. Continuando...")
