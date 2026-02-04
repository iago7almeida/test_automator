import re
import logging
from playwright.sync_api import Page, expect
from models.web.base_page import BasePage

class OrderManagementPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.order_rows = page.locator("tbody tr")
        self.tab_in_progress = page.get_by_text("Em andamento")

    def filter_by_in_progress(self):
        self.tab_in_progress.click()
        self.page.wait_for_load_state("networkidle")

    def get_count_of_unpaid_orders(self):
        return self.page.locator("text=Não pago").count()

    def get_order_id_by_status(self, status_text: str):
        target_row = self.order_rows.filter(has_text=status_text).first
        
        if target_row.is_visible():
            row_text = target_row.inner_text()
            match = re.search(r'\d{6}', row_text)
            order_id = match.group() if match else None
            
            if order_id:
                logging.info(f"🔍 Pedido encontrado com status '{status_text}': {order_id}")
                return order_id
        
        logging.info(f"⚠️ Nenhum pedido encontrado com status: {status_text}")
        return None

    def open_first_unpaid_order(self):

        unpaid_row = self.order_rows.filter(has_text="Não pago").first   
        if unpaid_row.is_visible():
            row_text = unpaid_row.inner_text()
            match = re.search(r'\d{6}', row_text) 
            order_id = match.group() if match else "ID_DESCONHECIDO"
            
            logging.info(f"🔍 Abrindo pagamento do pedido ID: {order_id}")
            unpaid_row.get_by_text("Não pago", exact=True).click()
            return order_id
        
        return None
    
    def change_order_status(self, order_id: str, current_status: str, new_status: str):
        logging.info(f"🔄 Mudando status {order_id}: [{current_status}] ➔ [{new_status}]")
        
        row = self.order_rows.filter(has_text=order_id)
        status_btn = row.locator("button, div").filter(has_text=current_status).filter(has=self.page.locator("visible=true")).last
        
        status_btn.click()
        option = self.page.get_by_text(new_status, exact=True)
        expect(option).to_be_visible()
        option.click()
        self.page.wait_for_timeout(3000)


    def verify_order_is_paid(self, order_id: str):
        row = self.order_rows.filter(has_text=order_id)
        status_recebido = row.get_by_text("Recebido").filter(has=self.page.locator("visible=true"))   
        expect(status_recebido).to_be_visible()
        logging.info(f"✅ Pedido {order_id} confirmado como PAGO.")

    def verify_status_order(self, order_id: str, expected_status: str):
        logging.info(f"🔎 Verificando status esperado: {expected_status}")
        row = self.order_rows.filter(has_text=order_id)
        status_badge = row.get_by_text(expected_status, exact=False)
        expect(status_badge).to_be_visible()

    

    