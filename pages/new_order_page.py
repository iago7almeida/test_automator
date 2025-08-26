# pages/new_order_page.py
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
import time

class NewOrderPage(BasePage):
    # Locators (baseados nos seus scripts originais - refine-os para maior robustez)
    
    # Seleção de Cliente
    CLIENT_SEARCH_INPUT_XPATH = '//*[@id="__next"]/div/div/aside/div[1]/div/input'
    FIRST_CLIENT_IN_SEARCH_RESULTS_XPATH = '//*[@id="__next"]/div/div/aside/div[1]/div/div/div/div[1]/div[1]' # Primeiro cliente na lista após busca

    # Tipos de Pedido
    ORDER_TYPE_RETIRADA_XPATH = '//*[@id="__next"]/div/div/aside/header/div/span[2]' # "Retirada"
    ORDER_TYPE_DELIVERY_XPATH = '//*[@id="__next"]/div/div/aside/header/div/span[3]' # "Delivery"

    # Adicionar Produtos (exemplos, idealmente seriam mais específicos ou parametrizáveis)
    # Categoria 1 (usado em single_order normal)
    CATEGORY_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div[2]/div/button[3]'
    # Produto 1 (usado em single_order normal)
    PRODUCT_BUTTON_XPATH = '//*[@id="__next"]/div/main/div/div[3]/button[1]'


    # Botões de Ação
    PROCEED_TO_PAYMENT_BUTTON_SELECTOR = 'button.sc-768b5d18-0.erbEJR:has-text("Pagamento")' # Botão "Pagamento"
    # O botão "Enviar Pedido" parece ter o mesmo seletor em alguns fluxos,
    # mas o contexto ou o nome podem mudar. Usaremos get_by_role quando possível.
    SEND_ORDER = '//*[@id="__next"]/div/div/aside/footer/div[2]/button[2]'
    LAUNCH_PAYMENT_BUTTON_ROLE_NAME = "Lançar"

    # Pagamento
    PAYMENT_OTHERS_BUTTON_NAME = "OTHERS" # Botão "Outros" para acessar vales
    PAYMENT_OTHERS_DROPDOWN_LABEL_SELECTOR = 'label.sc-c146f40d-5.dUiEeC' # Label para abrir dropdown de vales

    # Dicionário de seletores para métodos de pagamento (baseado em singleOrder.py)
    PAYMENT_METHOD_SELECTORS = {
        "Cash": 'button[name="CASH"]',
        "Pix": 'button[name="PIX"]',
        "Debit": 'button[name="DEBIT"]',
        "Credit": 'button[name="CREDIT"]',
        "OnCustomerAccount": 'button[name="ON_CUSTOMER_ACCOUNT"]',
        # Para os Vales, o fluxo é: clicar em OTHERS, clicar no label do dropdown, depois no item do li
        "MealVoucher": '//*[@id="__next"]/div/main/div/form/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[1]',
        "MealGift": '//*[@id="__next"]/div/main/div/form/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[2]',
        "Courtesy": '//*[@id="__next"]/div/main/div/form/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/ul/li[3]'
    }


    def __init__(self, page: Page):
        super().__init__(page)
        # É uma boa prática esperar por um elemento chave da página de Novo Pedido
        # para garantir que ela carregou antes de qualquer interação.
        # Ex: self.wait_for_selector(self.CATEGORY_1_BUTTON_XPATH, timeout=10000)
        print("Página de Novo Pedido inicializada.")


    def select_client_for_order(self):
        """Seleciona o primeiro cliente disponível após clicar no campo de busca."""
        print("Selecionando cliente para o pedido.")
        try:
        # Clica no campo de busca
            self.page.locator(self.CLIENT_SEARCH_INPUT_XPATH).click()
            time.sleep(1.3)  # Pequena espera para dropdown carregar (ideal: usar wait)

            # Espera até que o primeiro cliente esteja visível
            self.page.locator(self.FIRST_CLIENT_IN_SEARCH_RESULTS_XPATH).wait_for(state="visible", timeout=5000)

            # Força o clique no primeiro cliente
            self.page.evaluate('''(xpath) => {
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) element.click();
            }''', self.FIRST_CLIENT_IN_SEARCH_RESULTS_XPATH)
                
            print("Cliente selecionado com sucesso.")
            time.sleep(0.5)

        except PlaywrightTimeoutError:
            print("Timeout: Nenhum cliente encontrado nos resultados da busca.")
        except Exception as e:
            print(f"Erro ao selecionar cliente: {e}")


    def set_order_type_retirada(self):
        """Define o tipo de pedido como 'Retirada'."""
        print("Definindo tipo de pedido para RETIRADA.")
        self.click(self.ORDER_TYPE_RETIRADA_XPATH)
        # Adicionar espera para confirmação da mudança de tipo, se houver indicador visual
        time.sleep(1.5)

    def set_order_type_delivery(self):
        """Define o tipo de pedido como 'Delivery'."""
        print("Definindo tipo de pedido para DELIVERY.")
        self.click(self.ORDER_TYPE_DELIVERY_XPATH)
        # Adicionar espera
        time.sleep(1.5)

    def add_default_product_to_order(self, order_context: str = "standard"):
        """
        Adiciona um produto padrão ao pedido.
        order_context pode ser "standard" ou "retirada_delivery" para diferenciar seletores se necessário.
        """
        print(f"Adicionando produto padrão ao pedido (contexto: {order_context}).")
        if order_context == "retirada_delivery":
            self.click(self.CATEGORY_BUTTON_XPATH)
            time.sleep(1.2) # Curta espera entre cliques
            self.click(self.PRODUCT_BUTTON_XPATH)
        else: # standard
            self.click(self.CATEGORY_BUTTON_XPATH)
            time.sleep(1.2)
            self.click(self.PRODUCT_BUTTON_XPATH)
        print("Produto padrão adicionado.")
        time.sleep(0.5) # Espera para o item ser adicionado ao carrinho/resumo

    def go_to_payment_screen_single_order(self):
        """Clica no botão para prosseguir para a tela de pagamento do pedido avulso."""
        print("Prosseguindo para a tela de pagamento.")
        self.click(self.PROCEED_TO_PAYMENT_BUTTON_SELECTOR)
        # Adicionar espera para a tela de pagamento carregar
        # Ex: self.wait_for_selector(self.PAYMENT_METHOD_SELECTORS["Cash"], timeout=5000)
        time.sleep(1) # Do script original
        
    def proceed_to_payment_or_send_order(self):
        """Clica no botão para prosseguir para a tela de pagamento do pedido avulso."""
        print("Prosseguindo para a tela de pagamento.")
        self.click(self.PROCEED_TO_PAYMENT_BUTTON_SELECTOR)
        time.sleep(1)

    def select_payment_method_single_order(self, payment_type: str):
        """Seleciona o método de pagamento na tela de pagamento do pedido avulso."""
        print(f"Selecionando método de pagamento: {payment_type}")

        if payment_type in ["MealVoucher", "MealGift", "Courtesy"]:
            self.page.click(f'button[name="{self.PAYMENT_OTHERS_BUTTON_NAME}"]')
            time.sleep(1.3) # Espera para o dropdown de tipo de vale aparecer
            self.click(self.PAYMENT_OTHERS_DROPDOWN_LABEL_SELECTOR) # Clica no label para abrir as opções
            time.sleep(1.3) # Espera para as opções carregarem
            method_selector = self.PAYMENT_METHOD_SELECTORS[payment_type]
            self.click(method_selector)
        elif payment_type in self.PAYMENT_METHOD_SELECTORS:
            method_selector = self.PAYMENT_METHOD_SELECTORS[payment_type]
            self.click(method_selector)
        else:
            raise ValueError(f"Método de pagamento '{payment_type}' desconhecido ou não mapeado.")
        
        print(f"Método {payment_type} selecionado.")
        time.sleep(1.5) # Pausa para UI atualizar

    def click_launch_payment_button(self):
        """Clica no botão 'Lançar' pagamento."""
        print("Clicando no botão 'Lançar' pagamento.")
        self.page.get_by_role("button", name=self.LAUNCH_PAYMENT_BUTTON_ROLE_NAME).click()
        # Adicionar espera para o lançamento ser processado, se necessário
        time.sleep(1.5)

    def confirm_send_order(self):
        """Clica no botão 'Enviar Pedido' para finalizar."""
        print("Confirmando e enviando o pedido.")
        try:
            # Esperar o botão "Enviar Pedido" estar habilitado e visível
            time.sleep(2)
            self.click(self.SEND_ORDER)
            print("Pedido enviado.")
            # Adicionar espera para um indicador de sucesso ou navegação
            time.sleep(2) # Do script original
        except PlaywrightTimeoutError:
            print("Timeout: Botão 'Enviar Pedido' não ficou visível/habilitado a tempo.")
            # Tentar um seletor alternativo se o get_by_role falhar em algum contexto
            #if self.page.is_visible(self.PROCEED_TO_PAYMENT_BUTTON_SELECTOR): 
            
            #