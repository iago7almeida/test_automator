# tests/test_single_orders.py
import os
import pytest
from data.data import Customers, Products
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.new_order_page import NewOrderPage
from pages.payment_page import PaymentPage

from dotenv import load_dotenv

load_dotenv()
# Define uma lista de métodos de pagamento a ser usada para parametrizar o teste.
payment_methods_to_test = [
    "Dinheiro",
    "Pix",
    "Débito",
    "Crédito",
    "Fiado",
    ("Outros", "Vale Refeição"),
    ("Outros", "Vale Presente"),
    ("Outros", "Cortesia")
]

payment_methods = [
    "Dinheiro",
    "Pix",
    "Débito",
    "Crédito",
]

# PEDIDOS NO BALCÃO COM CLIENTE PREVIAMENTE CADASTRADO
@pytest.mark.parametrize("payment_method", payment_methods_to_test)
def test_create_order_balcony(logged_in_page: Page, payment_method: str):

    dashboard_page = DashboardPage(logged_in_page)
    new_order_page = NewOrderPage(logged_in_page)
    payment_page = PaymentPage(logged_in_page)

    dashboard_page.go_to_new_order()

    new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
    new_order_page.add_product_to_order(Products.COCA_COLA)
    new_order_page.proceed_to_payment()

    if isinstance(payment_method, tuple):
        main_method, sub_method = payment_method
        payment_page.select_payment_method(main_method)
        payment_page.select_other_sub_method(sub_method)
        payment_page.launch_order()
        payment_page.send_order()
        payment_page.handle_fiscal_note_modal_if_appears()

    elif payment_method == 'Fiado':
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


# PEDIDOS PARA RETIRADA COM CLIENTE PREVIAMENTE CADASTRADO
@pytest.mark.parametrize("payment_method", payment_methods)
def test_create_order_withdrawal(page: Page, payment_method: str):

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    new_order_page = NewOrderPage(page)
    payment_page = PaymentPage(page)

    # --- PRÉ-CONDIÇÃO: FAZER LOGIN ---
    username = os.getenv("HOMOLOG_USER")
    password = os.getenv("HOMOLOG_PASSWORD")

    login_page.navigate()
    login_page.login(username, password)

    dashboard_page.handle_payment_modal_if_appears()
    dashboard_page.login_verification_sucessfull()
    dashboard_page.go_to_new_order()

    #Seleciona o tipo do pedido, o cliente e o produto
    new_order_page.select_order_type_withdrawal()
    new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
    new_order_page.add_product_to_order(Products.COCA_COLA)
    new_order_page.proceed_to_payment()

    #Seleciona o método de pagamento e procede para confirmar o pedido
    payment_page.select_payment_method(payment_method)
    payment_page.send_order()
    payment_page.handle_fiscal_note_modal_if_appears()

    dashboard_page.login_verification_sucessfull() #Verifica se a pagina foi redirecionada com sucesso confirmando o pedido



# PEDIDOS PARA RETIRADA COM CLIENTE PREVIAMENTE CADASTRADO
@pytest.mark.parametrize("payment_method", payment_methods)
def test_create_order_delivery(page: Page, payment_method: str):

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    new_order_page = NewOrderPage(page)
    payment_page = PaymentPage(page)

    # --- PRÉ-CONDIÇÃO: FAZER LOGIN ---
    username = os.getenv("HOMOLOG_USER")
    password = os.getenv("HOMOLOG_PASSWORD")

    login_page.navigate()
    login_page.login(username, password)

    dashboard_page.handle_payment_modal_if_appears()
    dashboard_page.login_verification_sucessfull()
    dashboard_page.go_to_new_order()

    #Seleciona o tipo do pedido, o cliente e o produto
    new_order_page.select_order_type_delivery()
    new_order_page.search_and_select_customer(Customers.DEFAULT_CUSTOMER)
    new_order_page.add_product_to_order(Products.COCA_COLA)
    new_order_page.proceed_to_payment()

    #Seleciona o método de pagamento e procede para confirmar o pedido
    payment_page.select_payment_method(payment_method)
    payment_page.send_order()
    payment_page.handle_fiscal_note_modal_if_appears()

    dashboard_page.login_verification_sucessfull() #Verifica se a pagina foi redirecionada com sucesso confirmando o pedido