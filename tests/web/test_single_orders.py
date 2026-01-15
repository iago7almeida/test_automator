import pytest
from playwright.sync_api import Page

from config.settings import get_config
from data.data import Customers, Products
from models.web.dashboard_page import DashboardPage
from models.web.login_page import LoginPage
from models.web.new_order_page import NewOrderPage
from models.web.payment_page import PaymentPage

cfg = get_config()

payment_methods_to_test_balcony = [
    "Dinheiro",
    "Pix",
    "Débito",
    "Crédito",
    "Fiado",
    ("Outros", "Vale Refeição"),
    ("Outros", "Vale Presente"),
    ("Outros", "Cortesia"),
]

payment_methods_simple = [
    "Dinheiro",
    "Pix",
    "Débito",
    "Crédito",
]

@pytest.mark.frontend
def test_create_order_balcony(logged_in_page: Page):
    dashboard_page = DashboardPage(logged_in_page)
    new_order_page = NewOrderPage(logged_in_page)
    payment_page = PaymentPage(logged_in_page)
    dashboard_page.handle_payment_modal_if_appears()
    for payment_method in payment_methods_to_test_balcony:
        print(f"🔄 Testando pagamento: {payment_method}")
        
        dashboard_page.go_to_new_order()
        new_order_page.add_product_to_order(Products.TAMBAQUI)
        new_order_page.proceed_to_payment()

        if isinstance(payment_method, tuple):
            main_method, sub_method = payment_method
            payment_page.select_payment_method(main_method)
            payment_page.select_other_sub_method(sub_method)
            payment_page.launch_order()
            payment_page.send_order()
            payment_page.handle_fiscal_note_modal_if_appears()

        elif payment_method == "Fiado":
            new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
            payment_page.select_payment_method(payment_method)
            payment_page.launch_order()
            payment_page.send_order()
            payment_page.handle_fiscal_note_modal_if_appears()

        else:
            payment_page.select_payment_method(payment_method)
            payment_page.launch_order()
            payment_page.send_order()
            payment_page.handle_fiscal_note_modal_if_appears()
            print(f"✅ Pagamento {payment_method} concluído com sucesso.\n")
    dashboard_page.login_verification_sucessfull()
        


@pytest.mark.frontend
def test_create_order_withdrawal(logged_in_page: Page):
    dashboard_page = DashboardPage(logged_in_page)
    new_order_page = NewOrderPage(logged_in_page)
    payment_page = PaymentPage(logged_in_page)
    dashboard_page.handle_payment_modal_if_appears()
    for payment_method in payment_methods_simple:
        print(f"🔄 Testando Retirada com: {payment_method}")
        
        dashboard_page.go_to_new_order()
        new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
        new_order_page.select_order_type_withdrawal()  
        new_order_page.add_product_to_order(Products.TAMBAQUI)
        
        new_order_page.proceed_to_payment()

        payment_page.select_payment_method(payment_method)
        payment_page.send_order()
        payment_page.handle_fiscal_note_modal_if_appears()
        print(f"✅ Retirada com {payment_method} finalizada.\n")
    dashboard_page.login_verification_sucessfull()
        


@pytest.mark.frontend
def test_create_order_delivery(logged_in_page: Page):
    dashboard_page = DashboardPage(logged_in_page)
    new_order_page = NewOrderPage(logged_in_page)
    payment_page = PaymentPage(logged_in_page)
    dashboard_page.handle_payment_modal_if_appears()
    for payment_method in payment_methods_simple:
        print(f"🔄 Testando Delivery com: {payment_method}")

        dashboard_page.go_to_new_order()
        new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
        new_order_page.select_order_type_delivery()
        new_order_page.add_product_to_order(Products.TAMBAQUI)
        new_order_page.proceed_to_payment()
        
        payment_page.handle_delivery_fee()
        payment_page.select_payment_method(payment_method)

        payment_page.send_order()
        payment_page.handle_fiscal_note_modal_if_appears()

        print(f"✅ Delivery com {payment_method} finalizado.\n")
    dashboard_page.login_verification_sucessfull()
        