import random

from playwright.sync_api import Page, expect


class TablesPage:
    def __init__(self, page: Page):
        self.page = page

        # locators

        self.confirm_page_table = page.get_by_title("Todas as mesas")
        self.get_all_active_tables = page.locator('button[status="active"] strong')
        self.get_active_table_button = page.locator('button[status="active"]').first
        self.get_empty_table_button = page.locator('button[status="empty"]').first
        self.get_waiting_table_button = page.locator('button[status="waiting"]').first
        self.save_button = page.get_by_role("button", name="Salvar")
        self.button_open_tab = page.get_by_role("button", name="Abrir comanda")
        self.button_new_tab = page.get_by_role("button", name="Nova comanda")
        self.button_join_tab = page.get_by_role("button", name="Juntar comandas")
        self.join_modal = page.locator('h1:text("Juntar comandas")')
        self.select_table = page.get_by_text("Selecionar mesa", exact=True)
        self.close_dropdown = page.get_by_label("arrow-down-button")
        self.select_destination_tab = page.get_by_text("N° comanda", exact=True)
        self.button__history = page.get_by_role("button", name="Histórico")
        self.confirm_join_button = page.get_by_role("button", name="Aplicar")
        self.confirm_action_button = page.get_by_role("button", name="Confirmar")
        self.receive_payment_button = page.get_by_role("button", name="Receber")
        self.send_payment_button = page.get_by_role("button", name="Lançar")
        self.ended_tab_button = page.get_by_role("button", name="Finalizar comanda")

    def confirm_session_tables_pages(self):
        self.confirm_page_table.wait_for(state="visible", timeout=10000)
        print("Sessão de mesas confirmada.")

    def open_tab_in_a_empty_table(self):
        self.get_empty_table_button.click()
        self.button_open_tab.click()
        print("Comanda aberta com sucesso.")

    def open_tab_in_a_active_table(self):
        expect(self.get_active_table_button).to_be_visible(timeout=10000)
        self.get_active_table_button.click()
        expect(self.button_new_tab).to_be_visible(timeout=10000)
        self.button_new_tab.click()
        expect(self.save_button).to_be_visible(timeout=10000)
        self.save_button.click()
        print("Nova comanda aberta com sucesso.")

    def select_category(self, category_name: str):
        category_buttton = self.page.get_by_role("button", name=category_name)
        expect(category_buttton).to_be_visible(timeout=10000)
        category_buttton.click()

    def select_product(self, product_name: str):
        product_button = self.page.get_by_role("button", name=product_name)
        expect(product_button).to_be_visible(timeout=10000)
        product_button.click()

    def receive_payment_in_active_table(self):
        expect(self.get_active_table_button).to_be_visible(timeout=10000)
        self.get_active_table_button.click()
        expect(self.receive_payment_button).to_be_visible(timeout=10000)
        self.receive_payment_button.click()
        expect(self.send_payment_button).to_be_visible(timeout=10000)
        self.send_payment_button.click()
        expect(self.ended_tab_button).to_be_visible(timeout=10000)
        self.ended_tab_button.click()
        print("Pagamento recebido com sucesso.")

    def join_tabs_in_a_table(self):
        print("Iniciando o processo de juntar comandas...")
        expect(self.get_all_active_tables.nth(1)).to_be_visible(timeout=10000)
        all_active_tables = self.get_all_active_tables.all_inner_texts()

        if len(all_active_tables) < 2:
            raise ValueError("Não há mesas ativas suficientes para juntar comandas.")

        tables_to_join = random.sample(all_active_tables, 2)
        source_table_name = tables_to_join[0].strip()
        target_table_name = tables_to_join[1].strip()

        print(f"Mesas selecionadas para juntar comandas: {source_table_name} e {target_table_name}")
        print(f"mesa de destino sera: {target_table_name}")

        self.button_join_tab.click()
        expect(self.join_modal).to_be_visible()

        expect(self.select_table).to_be_visible(timeout=10000)
        self.select_table.click()

        self.page.get_by_text(f"Mesa {source_table_name}", exact=True).click()
        self.page.get_by_text(f"Mesa {target_table_name}", exact=True).click()

        print("Fechando o dropdown de seleção de mesa.")
        self.close_dropdown.click()

        print("Selecionando mesa de destino")
        self.select_destination_tab.click()
        expect(self.page.get_by_text(f"Mesa {target_table_name}", exact=True).last).to_be_visible()
        self.page.get_by_text(f"Mesa {target_table_name}", exact=True).last.click()

        print("Mesa de destino selecionanda, confirmando ação...")
        expect(self.confirm_join_button).to_be_enabled()
        self.confirm_join_button.click()

        expect(self.confirm_action_button).to_be_visible(timeout=10000)
        self.confirm_action_button.click()

        print("Comandas juntadas com sucesso.")
