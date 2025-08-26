# pages/tables_page.py
from pages.base_page import BasePage
import time

class TablesPage(BasePage):
    # Locators
    CATEGORY_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div[2]/div/button[3]' # Genérico, idealmente refinar
    PRODUCT_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div[3]/button[1]'    # Genérico, idealmente refinar
    CONFIRM_ORDER_ITEM_BUTTON = 'button[buttontype="confirm"]'
    NEW_ORDER = '//*[@id="__next"]/div[2]/div/header[2]/div/button[1]'
    CANCEL_BUTTON = '//*[@id="__next"]/div[2]/div/header[2]/div/button[6]'
    # ... outros locators ...

    def _get_table_selector(self, table_num: int) -> str:
        return f'//*[@id="__next"]/div/main/div/section/button[{table_num}]'

    def _is_order_sheet_opened(self, timeout_ms: int = 2000) -> bool:
        # Refatorado de modal_helper.orderSheet_opened
        selector = 'div[class="sc-fa3a0b24-2 bAbjMs"]' # Título "Comanda da Mesa X"
        return self.wait_for_selector(selector, state="visible", timeout=timeout_ms)

    def _handle_registered_payments_modal(self, timeout_sec: int = 2):
        # Refatorado de modal_helper.registered_payments
        modal_title_selector = 'h1:has-text("Pagamentos registrados")'
        ok_button_selector = 'button:has-text("Ok, entendi")'
        
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            if self.page.is_visible(modal_title_selector):
                print("Modal 'Pagamentos registrados' detectado. Clicando em 'Ok, entendi'.")
                self.click(ok_button_selector)
                return True
            time.sleep(0.5)
        print("Modal 'Pagamentos registrados' não detectado dentro do timeout.")
        return False

    def open_or_add_to_table(self, table_num: int):
        print(f"Clicando na Mesa: {table_num}")
        self.click(self._get_table_selector(table_num))
        
        # Lidar com o modal de "Caixa Aberto Identificado" que pode aparecer aqui
        self.handle_keep_open_modal_if_present() # Chamada do método da BasePage

        time.sleep(1) # Pequena pausa para a UI atualizar, idealmente usar waits explícitos

        if self._is_order_sheet_opened():
            print(f"Mesa {table_num} já aberta. Adicionando novo pedido.")
            self._add_items_to_existing_order_sheet()
        else:
            print(f"Abrindo Mesa {table_num} e adicionando primeiro pedido.")
            self._add_first_items_to_new_order_sheet()
        
        self.click(self.CONFIRM_ORDER_ITEM_BUTTON) # Confirmar adição de itens
        print(f"Itens confirmados para a mesa {table_num}")
        time.sleep(1) # Pausa para visualização/estabilidade, pode ser refinado
        
    def _add_items_to_existing_order_sheet(self):
        # Lógica de new_order de orderSheet.py
        time.sleep(1)
        self.click(self.NEW_ORDER) # Botão "Novo Pedido" dentro da comanda
        time.sleep(1) # Aguardar interface
        # Supondo que clicar na categoria e produto seja similar
        self.click(self.CATEGORY_BUTTON_XPATH)
        self.click(self.PRODUCT_BUTTON_XPATH) # Adiciona o produto
        time.sleep(1)

    def _add_first_items_to_new_order_sheet(self):
        # Lógica original de order_sheet para mesa não aberta
        self.click(self.CATEGORY_BUTTON_XPATH) # Categoria
        self.click(self.PRODUCT_BUTTON_XPATH)  # Adiciona o produto
        time.sleep(1)

    def cancel_order_sheet_for_table(self, table_num: int):
        print(f"Tentando cancelar comanda da Mesa: {table_num}")
        self.click(self._get_table_selector(table_num))
        time.sleep(1)

        if self._is_order_sheet_opened():
            print(f"Comanda da Mesa {table_num} está aberta. Procedendo com cancelamento.")
            # Locator para o botão "Cancelar Comanda" - ajuste se necessário
            self.click(self.CANCEL_BUTTON) # Ou seu XPath: //*[@id="__next"]/div[2]/div/header[2]/div/button[6]
            
            self._handle_registered_payments_modal() # Lida com modal de pagamentos
            
            # Locator para o motivo do cancelamento - ajuste se necessário
            self.click('xpath=//*[@id="8"]') # Motivo "Desistência do cliente" (exemplo)
            # Locator para o botão de confirmação final do cancelamento
            time.sleep(1)
            self.click('xpath=/html/body/div[9]/div/div/footer/button[2]') # Botão "Confirmar"
            print(f"Comanda da Mesa {table_num} cancelada.")
        else:
            print(f"Comanda da Mesa {table_num} não está aberta ou não foi encontrada. Nada a cancelar.")
            # Adicionar lógica para voltar, se necessário, ex:
            self.click('xpath=//*[@id="__next"]/div/div/aside/header/button') # Voltar para as mesas

    # ... Implementar outros métodos como transfer_order_sheet, receive_payment_for_table ...