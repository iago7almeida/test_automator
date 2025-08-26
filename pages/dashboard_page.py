# pages/dashboard_page.py

from pages.base_page import BasePage

class DashboardPage(BasePage):
    # Locators
    TABLES_MENU_ITEM = '//*[@id="__next"]/div/aside/div[5]' # Menu "Mesas e Comandas"
    NEW_ORDER_MENU_ITEM = 'div[hoverlabel="Novo pedido"]'
    CLIENTS_MENU_ITEM = 'div[hoverlabel="Clientes"]'
    # Adicione outros itens de menu conforme necessário

    def navigate_to_tables(self):
        print("Navegando para Mesas e Comandas")
        self.click(self.TABLES_MENU_ITEM)
        # Esperar por um elemento específico da página de mesas
        self.wait_for_selector('section button:has-text("Mesa")') # Exemplo

    def navigate_to_new_order(self):
        print("Navegando para Novo Pedido")
        self.click(self.NEW_ORDER_MENU_ITEM)
        # Esperar por um elemento da página de novo pedido

    def navigate_to_clients(self):
        print("Navegando para Clientes")
        self.click(self.CLIENTS_MENU_ITEM)
        # Esperar por um elemento da página de clientes