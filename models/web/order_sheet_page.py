import time
from playwright.sync_api import Page, expect
from models.web.base_page import BasePage
from models.web.payment_modal import PaymentModal

class OrderSheetPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # --- Componente de Pagamento (Reutilizável) ---
        self.payment_modal = PaymentModal(page)

        # --- Seção de Mesas (Visão Geral) ---
        self.tables_section = page.locator("section").first 
        
        # --- Modal 1: Mesa Vazia ("Abrir comanda") ---
        self.modal_open_order = page.locator("div[role='dialog']").filter(has_text="Abrir comanda")
        self.input_main_identifier = self.modal_open_order.get_by_placeholder("Número ou nome da comanda")
        self.input_customer_name = self.modal_open_order.get_by_placeholder("Nome do cliente")
        self.btn_confirm_open = self.modal_open_order.get_by_role("button", name="Abrir comanda")
        
        # --- Modal 2: Mesa Ocupada (Ações) ---
        self.modal_table_details = page.locator("div[role='dialog']").filter(has_text="Informações do cliente") 
        # Botões de ação principais
        self.btn_new_item = self.modal_table_details.locator("button", has_text="Novo")      # Botão Laranja
        self.btn_receive = self.modal_table_details.get_by_role("button", name="Receber")     # Botão Verde
        self.btn_transfer = self.modal_table_details.get_by_role("button", name="Transferir") # Botão Branco
        self.btn_cancel_sheet = self.modal_table_details.get_by_role("button", name="Cancelar") # Botão Cancelar
        
        # --- Tela de Adição de Itens (Categorias e Produtos) ---
        self.btn_confirm_items = page.locator('button[buttontype="confirm"]')

    # ==========================================
    # Ações Principais
    # ==========================================

    def select_table(self, table_number: int):
        """
        Clica na mesa especificada. 
        Nota: Não lida com o modal automaticamente, apenas clica.
        """
        print(f"🪑 Clicando na Mesa {table_number}...")
        # Tenta clicar pelo texto exato do número da mesa (ex: "01", "1")
        # Ajuste o seletor se o número estiver dentro de um span ou div específico
        self.page.locator("button").filter(has_text=str(table_number)).first.click()
        self.handle_keep_open_modal() # Fecha modal "Caixa Aberto" se aparecer

    def handle_table_opening_if_needed(self, customer_name="Cliente Teste"):
        """
        Verifica se apareceu o modal de 'Abrir comanda' (Mesa Vazia).
        Se aparecer, preenche e abre.
        Retorna True se precisou abrir, False se já estava ocupada.
        """
        try:
            # Espera um pouco para ver qual modal aparece
            if self.modal_open_order.is_visible(timeout=2000):
                print("✨ Mesa vazia detectada. Abrindo comanda...")
                
                self.input_customer_name.fill(customer_name)
                self.btn_confirm_open.click()
                
                # Espera a transição (geralmente vai para detalhes ou produtos)
                self.page.wait_for_timeout(1000)
                return True
        except:
            pass
        return False

    def add_item_to_table(self, table_number: int, category_index=0, product_index=0):
        """
        Fluxo completo: Clica na mesa -> (Abre se vazia) -> Clica em Novo -> Adiciona Item.
        """
        self.select_table(table_number)
        
        # Se a mesa estiver vazia, abre ela primeiro
        self.handle_table_opening_if_needed()
        
        # Agora deve estar no modal de detalhes (Mesa Ocupada). Clicamos em "Novo".
        if self.btn_new_item.is_visible():
            print("➕ Clicando em 'Novo' para adicionar itens...")
            self.btn_new_item.click()
        
        # --- Seleção de Produtos ---
        print("🛒 Selecionando produtos...")
        # Clica na primeira categoria (ajuste o seletor conforme seu HTML real de categorias)
        self.page.locator("div[class*='sc-categories']").first.click() # Exemplo genérico
        # Se não achar categoria, tenta clicar direto no produto
        
        # Clica no primeiro produto disponível (geralmente tem preço R$)
        self.page.locator("button").filter(has_text="R$").first.click()
        
        # Confirma a adição
        self.btn_confirm_items.click()
        print("✅ Item adicionado com sucesso.")
        self.page.wait_for_timeout(1000)

    def pay_table(self, table_number: int, payment_method: str = "Dinheiro", amount: str = None):
        """
        Fluxo de Pagamento: Clica na mesa -> Clica em Receber -> Usa PaymentModal.
        """
        self.select_table(table_number)
        
        # Garante que não é mesa vazia (não dá pra pagar mesa vazia)
        if self.modal_open_order.is_visible():
            print("⚠️ A mesa está vazia! Não há nada para pagar.")
            self.page.keyboard.press("Escape") # Fecha o modal de abrir
            return

        # Clica no botão "Receber" (Verde) do modal de detalhes
        print("💸 Clicando em 'Receber'...")
        self.btn_receive.click()
        
        # --- Integração com PaymentModal ---
        # Agora delegamos para a classe especialista que já consertamos
        self.payment_modal.select_payment_method(payment_method)
        
        if amount:
            self.payment_modal.fill_amount(amount)
            
        self.payment_modal.launch_payment()
        self.payment_modal.confirm_payment()
        
        print(f"✅ Pagamento de {payment_method} realizado na Mesa {table_number}.")

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