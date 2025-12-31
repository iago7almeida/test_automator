import re
from playwright.sync_api import Page, expect
from models.web.base_page import BasePage

class OrderManagementPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.order_rows = page.locator("tbody tr") # Assumindo estrutura de tabela
        self.tab_in_progress = page.get_by_text("Em andamento")

    def filter_by_in_progress(self):
        self.tab_in_progress.click()
        self.page.wait_for_load_state("networkidle")

    def get_count_of_unpaid_orders(self):
        """Conta quantos botões 'Não pago' visíveis existem."""
        return self.page.locator("text=Não pago").count()

    def open_first_unpaid_order(self):
        """
        Encontra o primeiro pedido 'Não pago', captura o ID e clica.
        Retorna o ID do pedido (str) ou None se não achar nada.
        """
        # Filtra as linhas que têm o texto "Não pago"
        unpaid_row = self.order_rows.filter(has_text="Não pago").first
        
        if unpaid_row.is_visible():
            # Tenta capturar o ID (geralmente é o número de 6 dígitos)
            row_text = unpaid_row.inner_text()
            # Regex simples para pegar o primeiro numero grande (ID)
            match = re.search(r'\d{6}', row_text) 
            order_id = match.group() if match else "ID_DESCONHECIDO"
            
            print(f"🔍 Abrindo pagamento do pedido ID: {order_id}")
            
            # Clica no botão "Não pago" dentro dessa linha
            unpaid_row.get_by_text("Não pago", exact=True).click()
            return order_id
        
        return None

    def verify_order_is_paid(self, order_id: str):
        """
        Verifica se o pedido específico agora está com status 'Recebido'.
        """
        # Localiza a linha pelo ID
        row = self.order_rows.filter(has_text=order_id)
        
        # Procura EXATAMENTE o botão/badge visível, ignorando tooltips escondidos
        # Usamos filter visível para não pegar o texto de ajuda do rodapé
        status_recebido = row.get_by_text("Recebido").filter(has=self.page.locator("visible=true"))
        
        expect(status_recebido).to_be_visible()
        print(f"✅ Pedido {order_id} confirmado como PAGO.")

    