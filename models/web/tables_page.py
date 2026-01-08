import random

from playwright.sync_api import Page, expect
from models.web.order_sheet_page import OrderSheetPage
import time
import re

class TablesPage:
    def __init__(self, page: Page):
        self.page = page

        # locators
        self.order_sheet = OrderSheetPage(page)
        self.confirm_page_table = page.get_by_title("Todas as mesas")
        self.get_all_active_tables = page.locator('button[status="active"] strong')
        self.get_active_table_button = page.locator('button[status="active"]').first
        self.get_empty_table_button = page.locator('button[status="empty"]').first
        self.get_waiting_table_button = page.locator('button[status="waiting"]').first
        self.save_button = page.get_by_role("button", name="Salvar")
        self.button_open_tab = page.get_by_role("button", name="Abrir comanda")
        self.button_new_tab = page.get_by_role("button", name="Nova comanda")
        self.button_join_tab = page.get_by_role("button", name="Juntar comandas")
        self.join_modal = page.locator("div[role='dialog']").filter(has_text="Juntar comandas")
        self.select_table = page.get_by_text("Selecionar mesa", exact=True)
        self.close_dropdown = page.get_by_label("arrow-down-button")
        self.select_destination_tab = page.get_by_text("N° comanda", exact=True)
        self.button__history = page.get_by_role("button", name="Histórico")
        self.confirm_join_button = self.join_modal.get_by_role("button", name="Aplicar")
        self.confirm_action_button = page.get_by_role("button", name="Confirmar")
        self.receive_payment_button = page.get_by_role("button", name="Receber")
        self.send_payment_button = page.get_by_role("button", name="Lançar")
        self.ended_tab_button = page.get_by_role("button", name="Finalizar comanda")

        self.areas_grid = self.page.locator('svg[aria-label="info-icon"]')
        self.btn_actions = self.page.get_by_text("Ações").locator("..")
        self.btn_join_tabs = self.page.get_by_text("Juntar Comandas")
        self.modal_confirm_join = page.locator("div[role='dialog']").filter(has_text="Confirmar junção?")
        self.btn_confirm_join = self.modal_confirm_join.get_by_role("button", name="Confirmar")


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

    def select_area(self, area_index: int = 0):
        print(f"🏙️ Abrindo menu de áreas e selecionando a opção {area_index}...")
        self.areas_grid.click()
        dropdown = self.page.locator("div[open]")        
        try:
            dropdown.wait_for(state="visible", timeout=3000)
        except:
            print("❌ Erro: O menu dropdown não abriu (não encontrei div[open]).")
            return
        options = dropdown.locator("> div:not(.divider)")
        count = options.count()
        if area_index >= count:
            print(f"⚠️ Índice {area_index} inválido. Existem apenas {count} áreas disponíveis.")
            self.page.keyboard.press("Escape")
            return
        target_option = options.nth(area_index)
        text = target_option.inner_text()
        print(f"✅ Selecionando área: {text}")
        
        target_option.click()

    @property
    def join_orders_items(self):
        return self.join_modal.locator('div[class*="ToToF"]')

    def join_tabs_in_a_table(self):
        print("Iniciando o processo de juntar comandas...")
        self.select_area(1)       
        self.btn_actions.click()
        self.btn_join_tabs.click()
        
        self.input_orderSheet = self.join_modal.locator('input[placeholder="Busque um local/comanda"]')
        self.input_orderSheet.fill("0")
        try:
            print("Aguardando resultados da busca carregarem...")
            self.join_orders_items.nth(1).wait_for(state="visible", timeout=10000)
        except:
            print("⚠️ Timeout: A lista não expandiu (ainda tem apenas 1 ou 0 itens).")

        targets = [0, 2]
        count = self.join_orders_items.count()
        print(f"Total de itens visíveis agora: {count}")

        for target in targets:
            item_to_click = None
            
            if isinstance(target, int):
                if target < count:
                    item_to_click = self.join_orders_items.nth(target)
                else:
                    print(f"⚠️ Índice {target} inválido (Lista tem {count} itens).")        
            elif isinstance(target, str):
                item_to_click = self.join_orders_items.filter(has_text=target).first
            
            if item_to_click:
                item_to_click.scroll_into_view_if_needed()
                item_to_click.click()
                print(f"☑️ Clicado: {target}")
                self.page.wait_for_timeout(500)
            

        print("Abrindo seleção de destino...")
        dropdown_trigger = self.join_modal.locator('div:has-text("N° da comanda")').last
        dropdown_trigger.scroll_into_view_if_needed()
        dropdown_trigger.click()
        print("🔽 Dropdown de destino aberto.")
        opcao_destino = self.page.locator('div').filter(has_text=re.compile(r"Mesa|Comanda|Avulsa")).last

        opcao_destino.wait_for(state="visible", timeout=5000)            
        texto_opcao = opcao_destino.inner_text().splitlines()[0]
        print(f"✅ Clicando na opção: {texto_opcao}")            
        opcao_destino.click()
        self.confirm_join_button.click()
        self.order_sheet.handle_administrative_password()
        self.modal_confirm_join.is_visible(timeout=5000)
        self.btn_confirm_join.click()

        print("☑️ Junção de mesas concluídas com sucesso")

        self.page.wait_for_timeout(5000)

