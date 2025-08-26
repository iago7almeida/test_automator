# pages/order_sheet_page.py
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
import time
import random
from pages.modal_handler import multiple_commands, tax_note

class OrderSheetPage(BasePage):
    # --- Locators para a Tela Principal de Mesas ---
    TABLE_BUTTON_XPATH_TEMPLATE = '//*[@id="__next"]/div/main/div/section/button[{table_num}]' # Botão da mesa
    BACK_TO_TABLES_VIEW_BUTTON_XPATH = '//*[@id="__next"]/div/div/aside/header/button' # Botão Voltar (quando uma comanda não está aberta)

    # --- Locators para Comanda Aberta (Order Sheet) ---
    ORDER_SHEET_TITLE_SELECTOR = 'div[class="sc-fa3a0b24-2 bAbjMs"]' # Usado para verificar se a comanda está aberta
    
    # Adicionar Itens/Novo Pedido na Comanda
    ADD_CATEGORY_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div[2]/div/button[3]' # Exemplo, pode variar
    ADD_PRODUCT_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div[3]/button[1]'    # Exemplo, pode variar
    CONFIRM_ADD_ITEM_BUTTON_SELECTOR = 'button[buttontype="confirm"]' # Botão "Confirmar" (ao adicionar item)
    
    NEW_ORDER_IN_SHEET_BUTTON_SELECTOR = 'xpath=//*[@id="__next"]/div[2]/div/header[2]/div/button[1]' # Botão "Novo Pedido" dentro da comanda
    # XPath genérico para uma categoria após clicar em "Novo Pedido" na comanda, refine se possível
    CATEGORY_IN_NEW_ORDER_XPATH = '//*[@id="__next"]/div/main/div/div[1]/div/div/div/div[2]' 

    # Cancelar Comanda
    CANCEL_SHEET_BUTTON_XPATH = '//*[@id="__next"]/div[2]/div/header[2]/div/button[6]' # Botão "Cancelar Comanda"
    CANCEL_REASON_ID_8_BUTTON_SELECTOR = 'button[id="8"]' # Motivo de cancelamento (ex: "Desistência do cliente")
    CONFIRM_CANCEL_SHEET_BUTTON_SELECTOR = 'button.sc-22f52115-5.kNiIjX:has-text("Confirmar")' # Botão final "Confirmar" cancelamento
    
    # Modal de Pagamentos Registrados (ao cancelar)
    REGISTERED_PAYMENTS_MODAL_TITLE_SELECTOR = 'h1:has-text("Pagamentos registrados")'
    REGISTERED_PAYMENTS_MODAL_OK_BUTTON_SELECTOR = 'button:has-text("Ok, entendi")'

    # Transferir Comanda
    MULTIPLE_COMMANDS_LABEL_SELECTOR = 'label[class="sc-32e0be68-12 gTfRrT"]' # Indica múltiplas comandas na mesa
    SELECT_FIRST_COMMAND_FOR_TRANSFER_XPATH = '//*[@id="__next"]/div[2]/div/div[2]/div/button[1]' # Selecionar a primeira comanda (se houver múltiplas)
    TRANSFER_SHEET_BUTTON_XPATH = '//*[@id="__next"]/div[2]/div/header[2]/div/button[3]' # Botão "Transferir"
    SELECT_ALL_ITEMS_FOR_TRANSFER_SELECTOR = ".checkbox" # Checkbox para selecionar todos os itens
    CONFIRM_TRANSFER_ITEMS_BUTTON_ROLE = ("button", {"name": "Transferir"}) # Botão "Transferir" no diálogo de itens
    TARGET_TABLE_INPUT_PLACEHOLDER = "N° Mesa"
    TARGET_COMMAND_INPUT_PLACEHOLDER = 'input[placeholder="N° comanda"]'
    APPLY_TRANSFER_BUTTON_ROLE = ("button", {"name": "Aplicar"})
    
    # Pagamento na Mesa (Comanda)
    # O botão 'button[buttontype="confirm"]' é usado para abrir a comanda e ir para pagamento
    PAYMENT_CASH_BUTTON_SELECTOR = 'button[name="CASH"]'
    PAYMENT_PIX_BUTTON_SELECTOR = 'button[name="PIX"]'
    PAYMENT_DEBIT_BUTTON_SELECTOR = 'button[name="DEBIT"]'
    PAYMENT_CREDIT_BUTTON_SELECTOR = 'button[name="CREDIT"]'
    PAYMENT_ON_CUSTOMER_ACCOUNT_BUTTON_SELECTOR = 'button[name="ON_CUSTOMER_ACCOUNT"]'
    PAYMENT_OTHERS_BUTTON_SELECTOR = 'button[name="OTHERS"]' # Botão "Outros" (vales)

    EDIT_INFO_BUTTON_SELECTOR = 'xpath=//*[@id="__next"]/div/div/aside/div[1]/button' # "Editar informações" (para adicionar cliente)
    CLIENT_SEARCH_IN_SHEET_INPUT_XPATH = '//*[@id="__next"]/div/div/aside/div[1]/div/div[1]/div[1]/input'
    FIRST_CLIENT_IN_SHEET_SEARCH_RESULTS_XPATH = '//*[@id="__next"]/div/div/aside/div[1]/div/div[1]/div[1]/div/div/div[1]/div[1]'
    CONFIRM_SHEET_EDIT_BUTTON_SELECTOR = 'button[buttontype="confirm"]' # Confirmar edição da comanda (após add cliente)
    
    VOUCHER_TYPE_DROPDOWN_LABEL_SELECTOR = 'label[class="sc-c146f40d-5 dUiEeC"]' # Para abrir dropdown de vales
    VOUCHER_TYPE_LI_XPATH_TEMPLATE = '//*[@id="__next"]/div/main/div/div/main/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[{voucher_option}]'
    
    LAUNCH_PAYMENT_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div/main/div/div[1]/div[1]/div[2]/button' # "Lançar pagamento"
    FINALIZE_ORDER_SHEET_BUTTON_XPATH = '//*[@id="__next"]/div/div/aside/footer/button' # "Finalizar a comanda"
    CANCEL_PRINT_MODAL_BUTTON_XPATH = '/html/body/div[9]/div/div/div/div/form/div[3]/button[1]' # "Cancelar impressão" (XPath absoluto, muito frágil)
                                                                                                # Idealmente: self.page.get_by_role("button", name="Não Imprimir") ou similar


    def __init__(self, page: Page):
        super().__init__(page)
        # Ações comuns ao inicializar, se houver.
        # Por exemplo, verificar se estamos na tela de mesas.
        # self.wait_for_selector(self.TABLE_BUTTON_XPATH_TEMPLATE.format(table_num=1), timeout=10000)
        print("OrderSheetPage (ou TablesPage) inicializada.")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#####
    def _click_table(self, table_num: int):
        """Clica no botão da mesa especificada."""
        table_selector = self.TABLE_BUTTON_XPATH_TEMPLATE.format(table_num=table_num)
        self.click(table_selector)
        print(f"Mesa {table_num} clicada.")
        # Adicionar uma pequena espera ou verificação se a UI mudou
        time.sleep(0.5) # Substituir por espera explícita
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#####
    def _is_order_sheet_opened(self, timeout_ms: int = 2000) -> bool:
        """Verifica se a comanda (order sheet) está atualmente aberta."""
        # Esta lógica veio de modal_helper.orderSheet_opened
        return self.wait_for_selector(self.ORDER_SHEET_TITLE_SELECTOR, state="visible", timeout=timeout_ms)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#####
    def _handle_registered_payments_modal(self, timeout_sec: int = 2):
        """Lida com o modal 'Pagamentos registrados' se ele aparecer."""
        # Esta lógica veio de modal_helper.registered_payments
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
        """Lida com o modal 'Caixa Aberto Identificado!' se presente."""
        # Reutilizando a lógica que estaria na BasePage ou foi sugerida anteriormente
        modal_header_selector = 'header.sc-60baa1a1-0:has-text("Caixa Aberto Identificado!")'
        keep_open_button_selector = 'button.sc-60baa1a1-4:has-text("Manter aberto")'
        try:
            self.page.wait_for_selector(modal_header_selector, state="visible", timeout=timeout_sec * 1000)
            if self.page.is_visible(modal_header_selector):
                print("Modal 'Caixa Aberto Identificado!' detectado. Clicando em 'Manter aberto'.")
                self.click(keep_open_button_selector)
                return True
        except PlaywrightTimeoutError:
            pass # Normal se não aparecer
        return False
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#####
    def add_order_to_table(self, table_num: int, is_new_table: bool = False):
        """
        Abre uma mesa e adiciona um pedido. Se a mesa já estiver aberta, adiciona um novo pedido à comanda existente.
        Baseado em orderSheet.py > order_sheet() e new_order()
        """
        
        self._click_table(table_num)
        self._handle_keep_open_modal_if_present() # Lida com modal de caixa aberto

        if self._is_order_sheet_opened():
            print(f"Mesa {table_num} já aberta. Adicionando novo pedido à comanda.")
            time.sleep(1.5)
            self.click(self.NEW_ORDER_IN_SHEET_BUTTON_SELECTOR)
            time.sleep(0.5) # Espera
            # A sequência de cliques para categoria/produto pode precisar ser mais robusta/paramétrica
            self.click(self.CATEGORY_IN_NEW_ORDER_XPATH) # Exemplo de categoria
            time.sleep(0.3)
            self.click(self.ADD_CATEGORY_BUTTON_XPATH) # Exemplo, pode ser outro locator aqui
            time.sleep(0.3)
            self.click(self.ADD_PRODUCT_BUTTON_XPATH)
        else:
            print(f"Mesa {table_num} não estava aberta ou abrindo pela primeira vez. Adicionando itens.")
            # Clicar em categoria e produto para o primeiro pedido na comanda
            self.click(self.ADD_CATEGORY_BUTTON_XPATH)
            time.sleep(0.3)
            self.click(self.ADD_PRODUCT_BUTTON_XPATH)
        
        time.sleep(0.5) # Espera para os itens serem processados
        self.click(self.CONFIRM_ADD_ITEM_BUTTON_SELECTOR)
        print(f"Itens confirmados para a mesa {table_num}.")
        time.sleep(1) # Espera para visualização/estabilidade
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#####
    def cancel_order_sheet(self, table_num: int):
        """
        Cancela a comanda de uma mesa específica.
        Baseado em orderSheet.py > cancel_orderSheet()
        """
        #self._click_table(table_num)
        #self._handle_keep_open_modal_if_present()

        if self._is_order_sheet_opened():
            print(f"Cancelando comanda da mesa: {table_num}")
            self.click(self.CANCEL_SHEET_BUTTON_XPATH)
            self._handle_registered_payments_modal() # Lida com modal de pagamentos se houver
            self.click(self.CANCEL_REASON_ID_8_BUTTON_SELECTOR) # Seleciona motivo
            time.sleep(0.3)
            self.click(self.CONFIRM_CANCEL_SHEET_BUTTON_SELECTOR) # Confirma cancelamento
            print(f"Comanda da mesa {table_num} cancelada.")
            time.sleep(1)
        else:
            print(f"Mesa {table_num} não está com a comanda aberta. Nada a cancelar.")
            self.click(self.BACK_TO_TABLES_VIEW_BUTTON_XPATH)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#####
    def transfer_order_sheet(self, table_num:int):
        """
        Transfere itens de uma comanda para outra mesa/comanda.
        Baseado em orderSheet.py > transfer_orderSheet()
        """
        multiple_comand = multiple_commands(self.page)
        self._click_table(table_num)
        self._handle_keep_open_modal_if_present()
        if self._is_order_sheet_opened():
            
            if multiple_comand:
                self.click(self.SELECT_FIRST_COMMAND_FOR_TRANSFER_XPATH)
            
            target_table = table_num    
            target_table = target_table - 1 if table_num > 1 else table_num + 1 # Isso é para que não tranfira em caso de loop sempre para mesa 01
            
            self.click(self.TRANSFER_SHEET_BUTTON_XPATH) # botão transferir
            self.page.locator(self.SELECT_ALL_ITEMS_FOR_TRANSFER_SELECTOR).first.click() # Checkbox que seleciona todos os itens da comanda
            time.sleep(1)
            self.page.get_by_role("dialog").get_by_role("button", name="Transferir").click()
            self.page.get_by_placeholder("N° Mesas").click()
            self.page.get_by_text(f"Mesas 0{target_table}").click() # Clicando na primeira mesa da lista
            print("Tranferiu e selecionou a mesa")
            element = self.page.locator(self.TARGET_COMMAND_INPUT_PLACEHOLDER)
            if element.is_visible() and element.is_enabled():
                print("Transferindo para para uma mesa já aberta")
                self.page.get_by_placeholder("N° comanda").click() # 
                self.page.click('xpath=/html/body/div[9]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/div') # Seleciona a primeira comanda da lista
                self.page.get_by_role("button", name="Aplicar").click() # aplica a tranferência
            else:
                self.page.get_by_role(self.APPLY_TRANSFER_BUTTON_ROLE).click()
        else:
            print(f"Não há o que tranferir na mesa {table_num}")
            self.click(self.BACK_TO_TABLES_VIEW_BUTTON_XPATH)
                        

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#####
    def select_client_for_table_payment(self):
        """Seleciona um cliente durante o pagamento na mesa."""
        print("Selecionando cliente para pagamento na conta.")
        self.click(self.CLIENT_SEARCH_IN_SHEET_INPUT_XPATH)
        time.sleep(1.5)

        self.page.evaluate('''(xpath) => {
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) element.click();
            }''', self.FIRST_CLIENT_IN_SHEET_SEARCH_RESULTS_XPATH)
        print("Cliente selecionado.")
        time.sleep(0.5)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#####
    def receive_payment_for_table(self, table_num: int,  tax_emit: int, payment_type: str = None):
        """
        Realiza o pagamento para uma comanda de mesa.
        Baseado em receivePaymentTable.py > receive_payment
        """
        
        
        multiple_comand = multiple_commands(self.page)
        tax_note_modal = tax_note(self.page)
        self._click_table(table_num)
        self._handle_keep_open_modal_if_present()
        
        if self._is_order_sheet_opened():
            print(f"Mesa {table_num} não está com a comanda aberta. Tentando abrir/confirmar.")
            self.click(self.CONFIRM_ADD_ITEM_BUTTON_SELECTOR) # Botão de receber pagamento
            time.sleep(1) # Esperar a tela de pagamento carregar
             
            payment_methods = {
                "Cash": lambda: self.click('button[name="CASH"]'),
                "Pix": lambda: self.click('button[name="PIX"]'),
                "Debit": lambda: self.click('button[name="DEBIT"]'),
                "Credit": lambda: self.click('button[name="CREDIT"]'),
                "OnCustomerAccount": lambda: self.on_customer_account(),
                "MealVoucher": lambda: self.select_voucher_type(1),
                "MealGift": lambda: self.select_voucher_type(2),
                "Courtesy": lambda: self.select_voucher_type(3)
            }
            
            payment_type = random.choice(list(payment_methods.keys()))
            #payment_type = "MealVoucher"
            print(f'Tipo de pagamento: {payment_type}')
            
            payment_methods[payment_type]() # Executa a função correspondente ao tipo de pagamento
            time.sleep(1)
            self.click(self.LAUNCH_PAYMENT_BUTTON_XPATH)  # Lançar pagamneto
            time.sleep(1)
            self.click(self.FINALIZE_ORDER_SHEET_BUTTON_XPATH) # Finalizar Comanda
            tax_c = tax_emit
            if tax_note_modal:
                self.page.locator('xpath=/html/body/div[9]/div/div/div/div/div/div[2]/div[2]/button[{tax_c}]').click() # Cancelar ou enviar a emissão da nota fiscal
                print("Cancela a emissão de nota fiscal")
            else:
                try:
                    self.page.locator('xpath=/html/body/div[9]/div/div/div/div/form/div[3]/button[1]').click(timeout=3000)  # Cancelar impressão após finalizar comanda
                
                except Exception as e:
                    print(f"Erro: {e}")
        else:
            self.page.locator('xpath=//*[@id="__next"]/div/div/aside/header/button').click() #Clica em vltar caso o modal de mesa aberta não seja detectado
                
    def select_voucher_type(self, voucher_option):
        self.click(self.PAYMENT_OTHERS_BUTTON_SELECTOR) # Botão "Outros"
        time.sleep(0.5)
        self.click(self.VOUCHER_TYPE_DROPDOWN_LABEL_SELECTOR) # Abrir dropdown de vales
        self.click(f'//*[@id="__next"]/div/main/div/div/main/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[{voucher_option}]')
            
    def on_customer_account(self):
            self.click(self.EDIT_INFO_BUTTON_SELECTOR) # "Editar informações"
            time.sleep(2)
            self.select_client_for_table_payment()
            self.click(self.CONFIRM_SHEET_EDIT_BUTTON_SELECTOR) # Confirmar edição da comanda
            self.click(self.PAYMENT_ON_CUSTOMER_ACCOUNT_BUTTON_SELECTOR) # Seleciona método Fiado
            time.sleep(2)
        
         # 
                

        