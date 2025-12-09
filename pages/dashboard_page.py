from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

        self.title = page.locator('h2:text("Dashboard")')
        self.menu_opened = page.locator('[hoverlabel="Menu"]')
        self.new_order_button = page.get_by_label("newOrder")
        self.order_sheet_button = page.get_by_label("Gestão de pedidos")
        self.tables_button = page.locator('[hoverlabel="Todas as Mesas"]')
        self.cash_manager_button = page.get_by_label("Gerenciador de caixa")
        self.clients_button = page.locator('[hoverlabel="Clientes"]')
        self.logout_button = page.get_by_role("button", name="Sair")

    def login_verification_sucessfull(self):
        expect(self.title).to_be_visible(timeout=10000)

    def handle_payment_modal_if_appears(self):
        close_modal_button = self.page.locator(".ReactModal__Overlay")

        try:
            # Espera por até 5 segundos pelo botão do modal
            expect(close_modal_button).to_be_visible(timeout=7000)
            print("Modal de pagamento encontrado. Fechando...")
            close_modal_button.click(position={"x": 10, "y": 10})
        except Exception:
            # Se o botão não aparecer, o expect() lança um TimeoutError,
            # que é capturado aqui para que o teste prossiga normalmente.
            print("Modal de pagamento não apareceu. Continuando...")

    def logout_system(self):
        self.menu_opened.click()
        self.logout_button.click()

    def go_to_new_order(self):
        self.new_order_button.click()

    def go_to_clients(self):
        self.clients_button.click()

    def go_to_order_sheet(self):
        self.order_sheet_button.click()

    def go_to_tables(self):
        self.tables_button.click()

    def go_to_cache_menager(self):
        self.cash_manager_button.click()
