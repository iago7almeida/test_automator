import random
import time

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BasePage
from .modal_handler import multiple_commands, tax_note


class OrderSheetPage(BasePage):
    TABLE_BUTTON_XPATH_TEMPLATE = '//*[@id="__next"]/div/main/div/section/button[{table_num}]'
    BACK_TO_TABLES_VIEW_BUTTON_XPATH = '//*[@id="__next"]/div/div/aside/header/button'

    ORDER_SHEET_TITLE_SELECTOR = 'div[class="sc-fa3a0b24-2 bAbjMs"]'

    ADD_CATEGORY_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div[2]/div/button[3]'
    ADD_PRODUCT_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div[3]/button[1]'
    CONFIRM_ADD_ITEM_BUTTON_SELECTOR = 'button[buttontype="confirm"]'

    NEW_ORDER_IN_SHEET_BUTTON_SELECTOR = 'xpath=//*[@id="__next"]/div[2]/div/header[2]/div/button[1]'
    CATEGORY_IN_NEW_ORDER_XPATH = '//*[@id="__next"]/div/main/div/div[1]/div/div/div/div[2]'

    CANCEL_SHEET_BUTTON_XPATH = '//*[@id="__next"]/div[2]/div/header[2]/div/button[6]'
    CANCEL_REASON_ID_8_BUTTON_SELECTOR = 'button[id="8"]'
    CONFIRM_CANCEL_SHEET_BUTTON_SELECTOR = 'button.sc-22f52115-5.kNiIjX:has-text("Confirmar")'

    REGISTERED_PAYMENTS_MODAL_TITLE_SELECTOR = 'h1:has-text("Pagamentos registrados")'
    REGISTERED_PAYMENTS_MODAL_OK_BUTTON_SELECTOR = 'button:has-text("Ok, entendi")'

    MULTIPLE_COMMANDS_LABEL_SELECTOR = 'label[class="sc-32e0be68-12 gTfRrT"]'
    SELECT_FIRST_COMMAND_FOR_TRANSFER_XPATH = '//*[@id="__next"]/div[2]/div/div[2]/div/button[1]'
    TRANSFER_SHEET_BUTTON_XPATH = '//*[@id="__next"]/div[2]/div/header[2]/div/button[3]'
    SELECT_ALL_ITEMS_FOR_TRANSFER_SELECTOR = ".checkbox"
    CONFIRM_TRANSFER_ITEMS_BUTTON_ROLE = (
        "button",
        {"name": "Transferir"},
    )
    TARGET_TABLE_INPUT_PLACEHOLDER = "N° Mesa"
    TARGET_COMMAND_INPUT_PLACEHOLDER = 'input[placeholder="N° comanda"]'
    APPLY_TRANSFER_BUTTON_ROLE = ("button", {"name": "Aplicar"})

    PAYMENT_CASH_BUTTON_SELECTOR = 'button[name="CASH"]'
    PAYMENT_PIX_BUTTON_SELECTOR = 'button[name="PIX"]'
    PAYMENT_DEBIT_BUTTON_SELECTOR = 'button[name="DEBIT"]'
    PAYMENT_CREDIT_BUTTON_SELECTOR = 'button[name="CREDIT"]'
    PAYMENT_ON_CUSTOMER_ACCOUNT_BUTTON_SELECTOR = 'button[name="ON_CUSTOMER_ACCOUNT"]'
    PAYMENT_OTHERS_BUTTON_SELECTOR = 'button[name="OTHERS"]'

    EDIT_INFO_BUTTON_SELECTOR = 'xpath=//*[@id="__next"]/div/div/aside/div[1]/button'
    CLIENT_SEARCH_IN_SHEET_INPUT_XPATH = '//*[@id="__next"]/div/div/aside/div[1]/div/div[1]/div[1]/input'
    FIRST_CLIENT_IN_SHEET_SEARCH_RESULTS_XPATH = '//*[@id="__next"]/div/div/aside/div[1]/div/div[1]/div[1]/div/div/div[1]/div[1]'
    CONFIRM_SHEET_EDIT_BUTTON_SELECTOR = 'button[buttontype="confirm"]'

    VOUCHER_TYPE_DROPDOWN_LABEL_SELECTOR = 'label[class="sc-c146f40d-5 dUiEeC"]'
    VOUCHER_TYPE_LI_XPATH_TEMPLATE = '//*[@id="__next"]/div/main/div/div/main/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[{voucher_option}]'

    LAUNCH_PAYMENT_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div/main/div/div[1]/div[1]/div[2]/button'
    FINALIZE_ORDER_SHEET_BUTTON_XPATH = '//*[@id="__next"]/div/div/aside/footer/button'
    CANCEL_PRINT_MODAL_BUTTON_XPATH = "/html/body/div[9]/div/div/div/div/form/div[3]/button[1]"

    def __init__(self, page: Page):
        super().__init__(page)
        print("OrderSheetPage (ou TablesPage) inicializada.")

    def _click_table(self, table_num: int):
        table_selector = self.TABLE_BUTTON_XPATH_TEMPLATE.format(table_num=table_num)
        self.click(table_selector)
        print(f"Mesa {table_num} clicada.")
        time.sleep(0.5)

    def _is_order_sheet_opened(self, timeout_ms: int = 2000) -> bool:
        return self.wait_for_selector(self.ORDER_SHEET_TITLE_SELECTOR, state="visible", timeout=timeout_ms)

    def _handle_registered_payments_modal(self, timeout_sec: int = 2):
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            if self.page.is_visible(self.REGISTERED_PAYMENTS_MODAL_TITLE_SELECTOR):
                print("Modal 'Pagamentos registrados' detectado. Clicando em 'Ok, entendi'.")
                self.click(self.REGISTERED_PAYMENTS_MODAL_OK_BUTTON_SELECTOR)
                return True
            time.sleep(0.2)
        print("Modal 'Pagamentos registrados' não detectado ou não tratado a tempo.")
        return False

    def _handle_keep_open_modal_if_present(self, timeout_sec=1):
        modal_header_selector = 'header.sc-60baa1a1-0:has-text("Caixa Aberto Identificado!")'
        keep_open_button_selector = 'button.sc-60baa1a1-4:has-text("Manter aberto")'
        try:
            self.page.wait_for_selector(modal_header_selector, state="visible", timeout=timeout_sec * 1000)
            if self.page.is_visible(modal_header_selector):
                print("Modal 'Caixa Aberto Identificado!' detectado. Clicando em 'Manter aberto'.")
                self.click(keep_open_button_selector)
                return True
        except PlaywrightTimeoutError:
            pass
        return False

    def add_order_to_table(self, table_num: int):
        self._click_table(table_num)
        self._handle_keep_open_modal_if_present()

        if self._is_order_sheet_opened():
            print(f"Mesa {table_num} já aberta. Adicionando novo pedido à comanda.")
            time.sleep(1.5)
            self.click(self.NEW_ORDER_IN_SHEET_BUTTON_SELECTOR)
            time.sleep(0.5)
            self.click(self.CATEGORY_IN_NEW_ORDER_XPATH)
            time.sleep(0.3)
            self.click(self.ADD_CATEGORY_BUTTON_XPATH)
            time.sleep(0.3)
            self.click(self.ADD_PRODUCT_BUTTON_XPATH)
        else:
            print(f"Mesa {table_num} não estava aberta ou abrindo pela primeira vez. Adicionando itens.")
            self.click(self.ADD_CATEGORY_BUTTON_XPATH)
            time.sleep(0.3)
            self.click(self.ADD_PRODUCT_BUTTON_XPATH)

        time.sleep(0.5)
        self.click(self.CONFIRM_ADD_ITEM_BUTTON_SELECTOR)
        print(f"Itens confirmados para a mesa {table_num}.")
        time.sleep(1)

    def cancel_order_sheet(self, table_num: int):
        if self._is_order_sheet_opened():
            print(f"Cancelando comanda da mesa: {table_num}")
            self.click(self.CANCEL_SHEET_BUTTON_XPATH)
            self._handle_registered_payments_modal()
            self.click(self.CANCEL_REASON_ID_8_BUTTON_SELECTOR)
            time.sleep(0.3)
            self.click(self.CONFIRM_CANCEL_SHEET_BUTTON_SELECTOR)
            print(f"Comanda da mesa {table_num} cancelada.")
            time.sleep(1)
        else:
            print(f"Mesa {table_num} não está com a comanda aberta. Nada a cancelar.")
            self.click(self.BACK_TO_TABLES_VIEW_BUTTON_XPATH)

    def transfer_order_sheet(self, table_num: int):
        has_multiple_comand = multiple_commands(self.page)
        self._click_table(table_num)
        self._handle_keep_open_modal_if_present()
        if self._is_order_sheet_opened():
            if has_multiple_comand:
                self.click(self.SELECT_FIRST_COMMAND_FOR_TRANSFER_XPATH)

            target_table = table_num
            target_table = target_table - 1 if table_num > 1 else table_num + 1

            self.click(self.TRANSFER_SHEET_BUTTON_XPATH)
            self.page.locator(self.SELECT_ALL_ITEMS_FOR_TRANSFER_SELECTOR).first.click()
            time.sleep(1)
            self.page.get_by_role("dialog").get_by_role("button", name="Transferir").click()
            self.page.get_by_placeholder("N° Mesas").click()
            self.page.get_by_text(f"Mesas 0{target_table}").click()
            print("Tranferiu e selecionou a mesa")
            element = self.page.locator(self.TARGET_COMMAND_INPUT_PLACEHOLDER)
            if element.is_visible() and element.is_enabled():
                print("Transferindo para para uma mesa já aberta")
                self.page.get_by_placeholder("N° comanda").click()
                self.page.click("xpath=/html/body/div[9]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div")
                self.page.get_by_role("button", name="Aplicar").click()
            else:
                self.page.get_by_role(self.APPLY_TRANSFER_BUTTON_ROLE).click()
        else:
            print(f"Não há o que tranferir na mesa {table_num}")
            self.click(self.BACK_TO_TABLES_VIEW_BUTTON_XPATH)

    def select_client_for_table_payment(self):
        print("Selecionando cliente para pagamento na conta.")
        self.click(self.CLIENT_SEARCH_IN_SHEET_INPUT_XPATH)
        time.sleep(1.5)

        self.page.evaluate(
            """(xpath) => {
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) element.click();
            }""",
            self.FIRST_CLIENT_IN_SHEET_SEARCH_RESULTS_XPATH,
        )
        print("Cliente selecionado.")
        time.sleep(0.5)

    def receive_payment_for_table(self, table_num: int, tax_emit: int, payment_type: str = None):
        tax_note_modal = tax_note(self.page)
        self._click_table(table_num)
        self._handle_keep_open_modal_if_present()

        if self._is_order_sheet_opened():
            print(f"Mesa {table_num} não está com a comanda aberta. Tentando abrir/confirmar.")
            self.click(self.CONFIRM_ADD_ITEM_BUTTON_SELECTOR)
            time.sleep(1)

            # Map simple payment methods to selectors; special cases call methods
            selector_map = {
                "Cash": self.PAYMENT_CASH_BUTTON_SELECTOR,
                "Pix": self.PAYMENT_PIX_BUTTON_SELECTOR,
                "Debit": self.PAYMENT_DEBIT_BUTTON_SELECTOR,
                "Credit": self.PAYMENT_CREDIT_BUTTON_SELECTOR,
            }

            payment_type = random.choice(["Cash", "Pix", "Debit", "Credit", "OnCustomerAccount", "MealVoucher", "MealGift", "Courtesy"])
            print(f"Tipo de pagamento: {payment_type}")

            if payment_type in selector_map:
                self.click(selector_map[payment_type])
            elif payment_type == "OnCustomerAccount":
                self.on_customer_account()
            elif payment_type == "MealVoucher":
                self.select_voucher_type(1)
            elif payment_type == "MealGift":
                self.select_voucher_type(2)
            elif payment_type == "Courtesy":
                self.select_voucher_type(3)
            time.sleep(1)
            self.click(self.LAUNCH_PAYMENT_BUTTON_XPATH)
            time.sleep(1)
            self.click(self.FINALIZE_ORDER_SHEET_BUTTON_XPATH)
            if tax_note_modal:
                self.page.locator(f"xpath=/html/body/div[9]/div/div/div/div/div/div[2]/div[2]/button[{tax_emit}]").click()
                print("Cancela a emissão de nota fiscal")
            else:
                try:
                    self.page.locator("xpath=/html/body/div[9]/div/div/div/div/form/div[3]/button[1]").click(timeout=3000)
                except Exception as e:
                    print(f"Erro: {e}")
        else:
            self.page.locator('xpath=//*[@id="__next"]/div/div/aside/header/button').click()

    def select_voucher_type(self, voucher_option):
        self.click(self.PAYMENT_OTHERS_BUTTON_SELECTOR)
        time.sleep(0.5)
        self.click(self.VOUCHER_TYPE_DROPDOWN_LABEL_SELECTOR)
        self.click(f'//*[@id="__next"]/div/main/div/div/main/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[{voucher_option}]')

    def on_customer_account(self):
        self.click(self.EDIT_INFO_BUTTON_SELECTOR)
        time.sleep(2)
        self.select_client_for_table_payment()
        self.click(self.CONFIRM_SHEET_EDIT_BUTTON_SELECTOR)
        self.click(self.PAYMENT_ON_CUSTOMER_ACCOUNT_BUTTON_SELECTOR)
        time.sleep(2)

    # Backwards-compatible aliases used by some tests
    def open_order(self, table_num: int):
        """Alias for opening a table/order sheet."""
        self._click_table(table_num)

    def transfer_order(self, table_num: int):
        """Alias for transfer operation used in older tests."""
        return self.transfer_order_sheet(table_num)
