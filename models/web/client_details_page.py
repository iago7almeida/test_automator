import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BasePage


class ClientDetailsPage(BasePage):
    RECEIVE_PAYMENT_MODAL_BUTTON = ".sc-c146f40d-5"
    PAYMENT_AMOUNT_INPUT_XPATH = '//*[@id="__next"]/div/main/div[2]/div/div/div/form/div[2]/div[2]/form/div[1]/div[1]/div/div/div/input'

    PAYMENT_METHOD_OPTIONS_XPATH = {
        "Cash": '//*[@id="__next"]/div/main/div[2]/div/div/div/form/div[2]/div[2]/form/div[1]/div[2]/div/div/div/div[2]/ul/li[1]',
        "Pix": '//*[@id="__next"]/div/main/div[2]/div/div/div/form/div[2]/div[2]/form/div[1]/div[2]/div/div/div/div[2]/ul/li[2]',
        "Debit": '//*[@id="__next"]/div/main/div[2]/div/div/div/form/div[2]/div[2]/form/div[1]/div[2]/div/div/div/div[2]/ul/li[3]',
        "Credit": '//*[@id="__next"]/div/main/div[2]/div/div/div/form/div[2]/div[2]/form/div[1]/div[2]/div/div/div/div[2]/ul/li[4]',
    }
    CONFIRM_RECEIVE_PAYMENT_BUTTON = 'xpath=//*[@id="__next"]/div/main/div[2]/div/div/div/form/div[2]/div[2]/form/div[3]/button[2]'
    DO_NOT_PRINT_RECEIPT_BUTTON_NAME = "Não Imprimir"

    CLOSE_CLIENT_DETAILS_AREA_BUTTON_XPATH = '//*[@id="__next"]/div/main/div[2]/button'
    TRANSACTIONS_HISTORY_BUTTON = 'button[class="sc-37cb81a8-12 gyTnjz"]'
    TRANSACTION_ITEM_ROW_SELECTOR = "table tbody tr svg.StyledIconBase-sc-ea9ulj-0.hQYLxw"

    def open_receive_payment_modal(self):
        print("Abrindo modal de recebimento de pagamento.")
        self.click(self.RECEIVE_PAYMENT_MODAL_BUTTON)
        self.wait_for_selector(self.PAYMENT_AMOUNT_INPUT_XPATH, timeout=5000)
        print("Modal de pagamento aberto.")

    def fill_payment_amount(self, amount: str):
        print(f"Preenchendo valor do pagamento: {amount}")
        self.fill(self.PAYMENT_AMOUNT_INPUT_XPATH, amount)

    def select_payment_method_client(self, payment_type: str):
        print(f"Selecionando método de pagamento: {payment_type}")
        if payment_type in self.PAYMENT_METHOD_OPTIONS_XPATH:
            method_selector = self.PAYMENT_METHOD_OPTIONS_XPATH[payment_type]
            self.wait_for_selector(method_selector, timeout=5000, state="visible")
            self.click(method_selector)
            print(f"Método {payment_type} selecionado.")
            time.sleep(1)
        else:
            raise ValueError(f"Método de pagamento '{payment_type}' não mapeado nos seletores.")

    def confirm_receive_payment(self):
        print("Confirmando recebimento do pagamento.")
        time.sleep(2)
        self.click(self.CONFIRM_RECEIVE_PAYMENT_BUTTON)
        self.page.wait_for_selector("SELETOR_DO_MODAL_DE_COMPROVANTE", timeout=10000)
        time.sleep(1)

    def select_do_not_print_receipt(self):
        print("Selecionando 'Não Imprimir' o comprovante.")
        try:
            self.page.wait_for_selector(f"button:has-text('{self.DO_NOT_PRINT_RECEIPT_BUTTON_NAME}')", state="visible", timeout=5000)
            self.page.get_by_role("button", name=self.DO_NOT_PRINT_RECEIPT_BUTTON_NAME).click()
            print("'Não Imprimir' selecionado.")
            self.page.wait_for_selector("SELETOR_DO_MODAL_DE_COMPROVANTE", state="hidden", timeout=5000)
            time.sleep(1)
        except PlaywrightTimeoutError:
            print("Timeout: Botão 'Não Imprimir' não apareceu ou não foi clicável a tempo.")
        except Exception as e:
            print(f"Erro ao clicar em 'Não Imprimir': {e}")

    def close_client_area_or_modal(self):
        print("Fechando área/modal de detalhes do cliente.")
        try:
            if self.page.is_visible(self.CLOSE_CLIENT_DETAILS_AREA_BUTTON_XPATH):
                self.click(self.CLOSE_CLIENT_DETAILS_AREA_BUTTON_XPATH)
                print("Área de detalhes do cliente fechada.")
        except Exception as e:
            print(f"Erro ao tentar fechar a área do cliente: {e}")

    def open_transactions_history(self):
        print("Abrindo histórico de transações do cliente.")
        self.click(self.TRANSACTIONS_HISTORY_BUTTON)
        self.wait_for_selector(self.TRANSACTION_ITEM_ROW_SELECTOR, timeout=5000, state="attached")
        print("Histórico de transações aberto.")

    def delete_all_listed_payments(self) -> int:
        self.open_transactions_history()

        deleted_count = 0
        print("Iniciando exclusão de pagamentos listados.")

        time.sleep(1)

        while True:
            list_transactions = self.page.locator(self.TRANSACTION_ITEM_ROW_SELECTOR)
            num_elements = list_transactions.count()
            print(f"Transações encontradas: {num_elements}")

            if num_elements == 0:
                print("Nenhuma transação encontrada para deletar.")
                break

            print("Tentando excluir a primeira transação da lista...")
            self.page.locator("button:has(svg)").click()

            self.page.get_by_role("dialog").get_by_role("textbox").click()
            self.page.get_by_role("dialog").get_by_role("textbox").fill("Porque sim")
            self.page.get_by_role("button", name="Cancelar").click()

            deleted_count += 1
            print(f"Transação {deleted_count} clicada para exclusão.")

            self.page.locator('button:has-text("Confirmar Exclusão")').click()

            self.page.wait_for_timeout(1500)

            if self.page.locator(self.TRANSACTION_ITEM_ROW_SELECTOR).count() == 0:
                print("Todas as transações visíveis foram processadas para exclusão.")
                break
            if self.page.locator(self.TRANSACTION_ITEM_ROW_SELECTOR).count() == num_elements:
                print("Nenhuma transação foi removida após o clique. Interrompendo para evitar loop infinito.")
                break

        print(f"Total de {deleted_count} pagamentos processados para exclusão.")
        return deleted_count
