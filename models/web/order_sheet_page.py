import re
import random
import time
import uuid
from playwright.sync_api import Page, expect
from models.web.base_page import BasePage
from models.web.payment_modal import PaymentModal
from models.web.new_order_page import NewOrderPage
from data.data import Customers, Products

class OrderSheetPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # --- Componente de Pagamento (Reutilizável) ---
        self.payment_modal = PaymentModal(page)

        # --- Seção de Mesas (Visão Geral) ---
        self.tables_section = page.locator("section").first 
        
        # --- Modal 1: Mesa Vazia ("Abrir comanda") ---
        self.modal_open_order = page.locator("div[role='dialog']").filter(has_text="Abrir ")
        self.input_main_identifier = self.modal_open_order.get_by_placeholder("Número ou nome da comanda")
        self.input_customer_name = self.modal_open_order.get_by_placeholder("Nome do cliente")
        self.btn_confirm_open = self.modal_open_order.get_by_role("button", name="Abrir comanda")
        self.btn_cancel_open = self.modal_open_order.get_by_role("button", name="Cancelar")
        
        # --- Modal: Senha administrativa
        self.modal_password = page.locator("div[role='dialog']").filter(has_text="Digite a senha administrativa")
        self.input_password = self.modal_password.locator("input[name=\"password\"]")
        self.btn_confirm_password = self.modal_password.get_by_role("button", name="Confirmar")

        # --- Modal 3: Mesa Ocupada (Ações) --- 
        self.modal_table_details = page.locator('div[class="sc-fa3a0b24-2 bAbjMs"]')
        # Múltiplas comandas
        self.multiple_modal = page.get_by_text("Selecionar comanda")
        # Botões de ação principais
        self.btn_new_item = self.modal_table_details.locator("button", has_text="Novo")      # Botão Laranja
        self.btn_receive = self.modal_table_details.get_by_role("button", name="Receber")     # Botão Verde
        self.btn_transfer = self.modal_table_details.get_by_role("button", name="Transferir") # Botão Branco
        self.btn_cancel_sheet = self.modal_table_details.get_by_role("button", name="Cancelar") # Botão Cancelar
        # transeferêcia de itens
        self.modal_transfer_itens = page.locator("div[role='dialog']").filter(has_text="Transferir")
        self.checkbox_select_all = self.modal_transfer_itens.get_by_text("Selecionar todos os itens")
        self.btn_next_transfer = self.modal_transfer_itens.get_by_role("button", name="Próximo")
        self.btn_cancel_transfer = self.modal_transfer_itens.get_by_role("button", name="Cancelar")
        self.btn_input_transfer = self.modal_transfer_itens.locator('input[placeholder="Busque por Comanda ou local"]')
        self.order_sheets_destiny = self.modal_transfer_itens.locator(".sc-a1e5d594-8")
        self.btn_confirm_transfer_final = self.modal_transfer_itens.get_by_role("button", name="Aplicar")
        self.btn_back_transfer = self.modal_transfer_itens.get_by_role("button", name="Voltar")
        self.modal_atentention = page.get_by_role("dialog").filter(has_text="Atenção!")
        self.btn_back_without_transfer = self.modal_atentention.get_by_role("button", name="Sim, sair sem transferir")
        self.alert_error_transfer = page.get_by_role("alert").filter(has_text="Erro ao transferir items")
        # Cancelar Comanda
        self.modal_cancel_sheet = page.get_by_role("dialog").filter(has_text="Cancelar Comanda")
        self.btn_confirm_cancel = self.modal_cancel_sheet.get_by_role("button", name="Confirmar")
        # --- Tela de Adição de Itens (Categorias e Produtos) ---
        self.btn_confirm_items = page.locator('button[buttontype="confirm"]')


    # ==========================================
    # Ações Principais
    # ==========================================

    def select_table(self, table_number: int):
        index = table_number - 1
        print(f"🪑 Selecionando a mesa na posição {index} (Mesa {table_number})...")
        target_table = self.tables_section.locator("button").nth(index)
        try:
            target_table.wait_for(state="visible", timeout=12000)
        except:
            print("❌ Timeout: As mesas não carregaram na tela a tempo.")
            return False

        target_table.click()
        self.handle_keep_open_modal()        
        return True


    def handle_table_opening_if_needed(self, customer_name="Cliente Teste"):
        try:
            if self.modal_open_order.is_visible(timeout=2000):
                print("✨ Mesa vazia detectada. Abrindo comanda...")
                identifier_value = str(uuid.uuid1())
                self.input_main_identifier.fill(str(identifier_value))
                self.input_customer_name.fill(customer_name)
                self.btn_confirm_open.click()
                self.page.wait_for_timeout(1000)
                return True
        except Exception as e:
            print(f"⚠️ Erro ao tentar selecionar comanda múltipla: {e}")
        return False
    
    def select_first_order_if_multiple(self):
        try:
            if self.multiple_modal.is_visible(timeout=2000):
                print("🗂️ Mesa com múltiplas comandas detectada.")
                card_regex = re.compile(r"comanda\s.+", re.IGNORECASE)            
                first_orderSheet = self.page.get_by_role("button").filter(has_text=card_regex).first              
                print(f"👆 Clicando na comanda: '{first_orderSheet.inner_text().splitlines()[0]}'")
                
                first_orderSheet.click(force=True)                
                self.multiple_modal.wait_for(state="hidden", timeout=5000)
                return True         
        except Exception as e:
            print(f"⚠️ ERRO CRÍTICO ao selecionar comanda: {e}")
            raise e 
            
        return False

    def handle_administrative_password(self):
        try:
            if self.modal_password.is_visible(timeout=2000):
                print("Necessário inserir senha administrativa")
                self.input_password.fill("12345")
                self.btn_confirm_password.click()
                self.page.wait_for_timeout(1000)
                return True
        except:
            pass
        return False
    
    def is_order_sheet_opened(self):
        try:
            if self.modal_table_details.is_visible(timeout=2000):
                print("Mesa aberta!!")
                self.btn_new_item.click()
                print("Clicando em Novo")

        except:
            pass
        return False

    def add_item_to_table(self, table_number: int, category_index=0, product_index=0):
        self.select_table(table_number)
        
        # Se a mesa estiver vazia, abre ela primeiro
        self.handle_table_opening_if_needed()
        self.select_first_order_if_multiple()
        self.is_order_sheet_opened()
        
        # --- Seleção de Produtos ---
        print("🛒 Selecionando produtos...")
        new_order_page = NewOrderPage(self.page)
        new_order_page.add_product_to_order(Products.TAMBAQUI)

        
        # Confirma a adição
        self.btn_confirm_items.click()
        print("✅ Item adicionado com sucesso.")
        self.page.wait_for_timeout(1000)



    def select_transfer_destination(self, destination_index: int):
        print(f"📍 Buscando destino de transferência na posição {destination_index}...")
        destinations = self.order_sheets_destiny.locator("> div")
        try:
            destinations.first.wait_for(state="visible", timeout=10000)
        except:
            print("❌ Timeout: A lista de destinos não carregou.")
            return False
        count = destinations.count()
        if destination_index >= count:
            print(f"❌ Erro: Tentou selecionar índice {destination_index}, mas só existem {count} destinos disponíveis.")
            return False
        target = destinations.nth(destination_index)

        try:
            local_name = target.locator("p").first.inner_text()
            print(f"✅ Selecionando destino: {local_name}")
        except:
            print("✅ Selecionando destino...")

        target.click()
        return True


    def transfer_order_sheet(self, table_number: int, destination_index: int = 0):
        if not self.select_table(table_number):
            return
        if self.modal_open_order.is_visible():
            print("⚠️ A mesa está vazia! Não há nada para transferir.")
            self.btn_cancel_open.click()
            return
        self.select_first_order_if_multiple()
        print("Clicando em 'Transferir'...")

        self.btn_transfer.click()
        self.modal_transfer_itens.wait_for(state="visible", timeout=3000)
        self.checkbox_select_all.click()
        self.page.wait_for_timeout(500)           
        print("➡️ Clicando em 'Próximo'...")
        self.btn_next_transfer.click()
        self.btn_input_transfer.fill("0")
        if not self.select_transfer_destination(destination_index):
            return 
        print("🚀 Confirmando transferência...")
        self.btn_confirm_transfer_final.click()
        self.handle_administrative_password()
        try:
            print("⏳ Verificando se houve erro na transferência...")
            self.alert_error_transfer.wait_for(state="visible", timeout=5000)
            print("🚨 Erro ao transferir itens detectado!")
            self.btn_back_transfer.click()           
            self.btn_cancel_transfer.click()
            self.btn_back_without_transfer.wait_for(state="visible", timeout=3000)
            self.btn_back_without_transfer.click()
            self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(1).click()    
            return
        except Exception:
            print("✅ Nenhum erro detectado. Prosseguindo.")
        self.page.wait_for_timeout(500) 
        print("✅ Transferência concluída.")


    def cancel_order_sheet(self, table_number: int, reason_text: str = None):
        print(f"Iniciando cancelamento da mesa {table_number}...")
        self.select_table(table_number)
        if self.modal_open_order.is_visible():
            print("⚠️ A mesa está vazia! Não há nada para pagar.")
            self.btn_cancel_open.click()
            return
        self.select_first_order_if_multiple()
        self.btn_cancel_sheet.click()
        self.modal_cancel_sheet.wait_for(state="visible", timeout=5000)
        options = [
            "Desistência",
            "Saiu sem pagar",
            "Insatisfação com o atendimento",
            "Insatisfação com o produto"
        ]

        if reason_text:
            target_reason = reason_text
            print(f"🎯 Motivo selecionado manualmente: {target_reason}")
        else:
            target_reason = random.choice(options)
            print(f"🎲 Motivo selecionado aleatoriamente: {target_reason}")
        btn_reason = self.modal_cancel_sheet.locator("button").filter(has_text=target_reason).first
        btn_reason.wait_for(state="visible", timeout=5000)
        btn_reason.click()
        print(f"✅ Botão '{target_reason}' clicado com sucesso.")
        
        input_pass = self.modal_cancel_sheet.locator('input[type="password"]')
        if input_pass.is_visible():
            print("🔑 Inserindo senha administrativa...")
            input_pass.fill("12345")
        self.btn_confirm_cancel.click()
        print("✅ Cancelamento confirmado.")
        
        self.page.wait_for_timeout(1000)
        


    def pay_table(self, table_number: int, payment_method: str = "Débito", amount: str = None):
        self.select_table(table_number)        
        if self.modal_open_order.is_visible():
            print("⚠️ A mesa está vazia! Não há nada para pagar.")
            self.btn_cancel_open.click()
            return
        self.select_first_order_if_multiple()
        print("💸 Clicando em 'Receber'...")
        self.btn_receive.click()
        self.payment_modal.select_payment_method(payment_method)
        
        #if amount:
        #    self.payment_modal.fill_amount(amount)
         
        self.payment_modal.launch_payment() 
        time.sleep(2)
        print(f"✅ Pagamento de {payment_method} realizado na Mesa {table_number}.") 
        self.payment_modal.finalize_order_sheet()
        self.handle_administrative_password()
        time.sleep(2)
        

    # ==========================================
    # Utilitários
    # ==========================================

    def handle_keep_open_modal(self):
        """Fecha modal de 'Caixa Aberto' se aparecer."""
        try:
            btn = self.page.get_by_role("button", name="Manter aberto")
            if btn.is_visible(timeout=1500):
                btn.click()
        except:
            pass

