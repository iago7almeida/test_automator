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
        print("Concluí payment_method")

    def select_other_sub_method(self, sub_method):
        print(f"Tentando selecionar sub-método: {sub_method}")
    
        target_option = self.page.get_by_text(sub_method, exact=True)
        if target_option.is_visible():
            target_option.click()
        else:
            try:
                self.page.locator("input[placeholder*='Selecione']").click(timeout=2000)
            except:
                pass
            target_option.click(force=True)

    def launch_order(self):
        sleep(1)
        self.submit_button.click()

        no_payment_message = self.page.get_by_text("Nenhum pagamento adicionado")
        expect(no_payment_message).to_be_hidden(timeout=15000)
        expect(self.send_order_button).to_be_enabled(timeout=10000)

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
        close_modal_button = self.page.get_by_role("button", name="Não emitir")

        try:
            expect(close_modal_button).to_be_visible(timeout=5000)
            print("Modal de nota fiscal encontrado. Fechando...")
            close_modal_button.click()
        except Exception:
            print("Modal de nota fiscal não apareceu. Continuando...")
