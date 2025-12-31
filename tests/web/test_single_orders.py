import pytest
from playwright.sync_api import Page

from config.settings import get_config
from data.data import Customers, Products
from models.web.dashboard_page import DashboardPage
from models.web.login_page import LoginPage
from models.web.new_order_page import NewOrderPage
from models.web.payment_page import PaymentPage

cfg = get_config()


payment_methods_to_test = [
    "Dinheiro",
    "Pix",
    "Débito",
    "Crédito",
    "Fiado",
    ("Outros", "Vale Refeição"),
    ("Outros", "Vale Presente"),
    ("Outros", "Cortesia"),
]

payment_methods = [
    "Dinheiro",
    "Pix",
    "Débito",
    "Crédito",
]


@pytest.mark.frontend
@pytest.mark.parametrize("payment_method", payment_methods_to_test)
def test_create_order_balcony(logged_in_page: Page, payment_method: str):
    dashboard_page = DashboardPage(logged_in_page)
    new_order_page = NewOrderPage(logged_in_page)
    payment_page = PaymentPage(logged_in_page)

    dashboard_page.go_to_new_order()

    new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
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
        payment_page.select_payment_method(payment_method)
        payment_page.launch_order()
        payment_page.send_order()
        payment_page.handle_fiscal_note_modal_if_appears()

    else:
        payment_page.select_payment_method(payment_method)
        payment_page.launch_order()
        payment_page.send_order()
        payment_page.handle_fiscal_note_modal_if_appears()

    dashboard_page.login_verification_sucessfull()


@pytest.mark.frontend
@pytest.mark.parametrize("payment_method", payment_methods)
def test_create_order_withdrawal(page: Page, payment_method: str):
    dashboard_page = DashboardPage(page)
    new_order_page = NewOrderPage(page)
    payment_page = PaymentPage(page)

    # Use shared login fixture to ensure a consistent, clean logged-in state
    # when the test asks for `page` we do a manual login to preserve compatibility
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(cfg.USERNAME, cfg.PASSWORD)

    dashboard_page.handle_payment_modal_if_appears()
    dashboard_page.login_verification_sucessfull()
    dashboard_page.go_to_new_order()

    new_order_page.select_order_type_withdrawal()
    new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
    new_order_page.add_product_to_order(Products.TAMBAQUI)
    new_order_page.proceed_to_payment()

    payment_page.select_payment_method(payment_method)
    payment_page.send_order()
    payment_page.handle_fiscal_note_modal_if_appears()

    dashboard_page.login_verification_sucessfull()


@pytest.mark.frontend
@pytest.mark.parametrize("payment_method", payment_methods)
def test_create_order_delivery(page: Page, payment_method: str):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    new_order_page = NewOrderPage(page)
    payment_page = PaymentPage(page)

    login_page.navigate()
    login_page.login(cfg.USERNAME, cfg.PASSWORD)

    dashboard_page.handle_payment_modal_if_appears()
    dashboard_page.login_verification_sucessfull()
    dashboard_page.go_to_new_order()

    new_order_page.select_order_type_delivery()
    new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
    new_order_page.add_product_to_order(Products.TAMBAQUI)
    new_order_page.proceed_to_payment()
    #--------------------
    payment_page.handle_delivery_fee()
    payment_page.select_payment_method(payment_method)

    payment_page.send_order()
    payment_page.handle_fiscal_note_modal_if_appears()

    dashboard_page.login_verification_sucessfull()
