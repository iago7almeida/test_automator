from time import sleep

from playwright.sync_api import Page, expect


class PaymentPage:
    """
    Representa a página de pagamento e finalização do pedido.

    Esta classe gerencia os elementos e as ações da etapa final de um pedido,
    incluindo a seleção do método de pagamento, a busca por um cliente
    e a submissão final do pedido.
    """

    def __init__(self, page: Page):
        self.page = page

        # --- Localizadores de Elementos ---

        self.submit_button = page.get_by_role("button", name="Lançar")
        self.send_order_button = page.get_by_role("button", name="Enviar Pedido")

    def select_payment_method(self, method: str):
        """
        Seleciona um método de pagamento na lista de opções.

        Args:
            method: O nome exato do método de pagamento (ex: "Dinheiro").
        """
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
        """
        Clica no botão 'Lançar' para registrar o pagamento.
        """
        sleep(1)
        self.submit_button.click()

        no_payment_message = self.page.get_by_text("Nenhum pagamento adicionado")
        expect(no_payment_message).to_be_hidden(timeout=15000)
        print("Botão 'lançar' clicado. Aguardando 'Enviar Pedido' ser habilitado...")
        expect(self.send_order_button).to_be_enabled(timeout=10000)
        print("'Eviar pedido' está habilidado. Prosseguindo...")

    def send_order(self):
        """
        Clica no botão final 'Enviar Pedido' para concluir o fluxo.
        """
        expect(self.send_order_button).to_be_enabled()
        self.send_order_button.click()

    def handle_fiscal_note_modal_if_appears(self):
        """
        Verifica se um modal sobre nota fiscal apareceu e o fecha.

        Esta função espera por um curto período de tempo por um modal que pode
        aparecer em ambientes de teste. Se o modal for encontrado, ela clica
        no botão 'Cancelar' para fechar. Se não, o teste continua sem erro.
        """
        close_modal_button = self.page.get_by_role("button", name="Cancelar")

        try:
            # Espera por até 5 segundos pelo botão do modal
            expect(close_modal_button).to_be_visible(timeout=5000)
            print("Modal de nota fiscal encontrado. Fechando...")
            close_modal_button.click()
        except Exception:
            # Se o botão não aparecer, o expect() lança um TimeoutError,
            # que é capturado aqui para que o teste prossiga normalmente.
            print("Modal de nota fiscal não apareceu. Continuando...")
