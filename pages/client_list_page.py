# pages/client_list_page.py
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
import time

class ClientListPage(BasePage):
    # Locators (estes são exemplos baseados no seu script original, refine-os para maior robustez)
    # O ideal é usar IDs, data-testid, ou seletores CSS/XPath mais específicos e menos dependentes da estrutura.
    FIRST_CLIENT_ROW_XPATH = '//*[@id="__next"]/div/main/table/tbody/tr[1]'
    # Se houver uma maneira de identificar um cliente por nome ou ID, seria melhor:
    # CLIENT_ROW_BY_NAME_XPATH_TEMPLATE = '//tr[.//td[contains(text(), "{client_name}")]]'

    def __init__(self, page: Page):
        super().__init__(page)

    def select_first_client(self) -> bool:
        """
        Seleciona o primeiro cliente da lista.
        Retorna True se bem-sucedido, False caso contrário.
        """
        print("Tentando selecionar o primeiro cliente da lista.")
        try:
            # Esperar que a tabela de clientes esteja visível e tenha pelo menos uma linha
            self.page.wait_for_selector(self.FIRST_CLIENT_ROW_XPATH, state="visible", timeout=10000)
            self.click(self.FIRST_CLIENT_ROW_XPATH)
            print("Primeiro cliente selecionado.")
            # Idealmente, após clicar, espere por um elemento na página de detalhes do cliente
            # para confirmar que a navegação ocorreu.
            # Ex: self.page.wait_for_selector(ClientDetailsPage.SOME_ELEMENT_ON_DETAILS_PAGE, timeout=5000)
            return True
        except PlaywrightTimeoutError:
            print("Timeout: Nenhum cliente encontrado ou a lista de clientes não carregou a tempo.")
            return False
        except Exception as e:
            print(f"Erro ao selecionar o primeiro cliente: {e}")
            return False

    def select_client_by_name(self, client_name: str) -> bool:
        """
        Seleciona um cliente pelo nome (exemplo, precisa de locator adequado).
        """
        # client_selector = self.CLIENT_ROW_BY_NAME_XPATH_TEMPLATE.format(client_name=client_name)
        # print(f"Tentando selecionar o cliente: {client_name}")
        # try:
        #     self.page.wait_for_selector(client_selector, state="visible", timeout=7000)
        #     self.click(client_selector)
        #     print(f"Cliente {client_name} selecionado.")
        #     return True
        # except PlaywrightTimeoutError:
        #     print(f"Timeout: Cliente {client_name} não encontrado.")
        #     return False
        # except Exception as e:
        #     print(f"Erro ao selecionar cliente {client_name}: {e}")
        #     return False
        print(f"Funcionalidade 'select_client_by_name' não implementada com locators reais.")
        return False