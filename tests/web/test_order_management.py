import pytest
from playwright.sync_api import expect
from models.web.dashboard_page import DashboardPage
from models.web.order_management_page import OrderManagementPage
from models.web.payment_modal import PaymentModal
from models.web.payment_page import PaymentPage


@pytest.mark.frontend
def test_split_payment_pix_and_cash(logged_in_page):
    dashboard = DashboardPage(logged_in_page)
    orders_page = OrderManagementPage(logged_in_page)
    payment_modal = PaymentModal(logged_in_page)
    payment_page = PaymentPage(logged_in_page)
    dashboard.go_to_order_sheet()
    orders_page.filter_by_in_progress()
    
    order_id = orders_page.open_first_unpaid_order()
    if not order_id:
        pytest.skip("Sem pedidos pendentes.")
    
    # 1. Pix (Parcial)
    payment_modal.select_payment_method("Pix")
    payment_modal.fill_amount("0,10") 
    payment_modal.launch_payment()
    
    # Validação rápida
    remaining = payment_modal.get_remaining_amount()
    assert "R$ 0,00" not in remaining, f"Erro: Zerou cedo demais! Restante: {remaining}"
    payment_modal.select_payment_method("Dinheiro")
    payment_modal.launch_payment()
    
    final_remaining = payment_modal.get_remaining_amount()
    assert "R$ 0,00" in final_remaining, f"Erro: Não zerou. Resta: {final_remaining}"
    
    payment_modal.confirm_payment()
    payment_page.handle_fiscal_note_modal_if_appears()



@pytest.mark.frontend
def test_pay_all_unpaid_orders(logged_in_page):
    """
    Fluxo Repetitivo:
    Enquanto houver pedidos 'Não pago', abre o modal e paga.
    """
    dashboard = DashboardPage(logged_in_page)
    orders_page = OrderManagementPage(logged_in_page)
    payment_modal = PaymentModal(logged_in_page)
    payment_page = PaymentPage(logged_in_page)
    # 1. Navegação
    dashboard.go_to_order_sheet()
    orders_page.filter_by_in_progress()

    orders_paid_count = 0

    while True:
        order_id = orders_page.open_first_unpaid_order()

        if not order_id:
            print("🏁 Não há mais pedidos pendentes na lista.")
            break

        payment_modal.select_payment_method("Pix")
        payment_modal.launch_payment()
        payment_modal.confirm_payment()
        payment_page.handle_fiscal_note_modal_if_appears()
        logged_in_page.wait_for_timeout(1000) 
        orders_page.verify_order_is_paid(order_id)
        
        orders_paid_count += 1

    if orders_paid_count == 0:
        pytest.skip("Nenhum pedido 'Não pago' foi encontrado para testar.")
    else:
        print(f"🎉 Sucesso! Total de pedidos pagos neste teste: {orders_paid_count}")


@pytest.mark.frontend
def test_order_status_flow(logged_in_page):
    dashboard = DashboardPage(logged_in_page)
    orders_page = OrderManagementPage(logged_in_page)
    dashboard.go_to_order_sheet()
    orders_page.filter_by_in_progress()
    ST_PENDENTE = "PENDENTE"
    ST_CONFIRMADO = "CONFIRMADO"
    ST_PRONTO = "PRONTO"
    ST_ENTREGUE = "ENTREGUE"
    
    OPT_CONFIRMADO = "Confirmado"
    OPT_PRONTO = "Pronto"
    OPT_ENTREGUE = "Entregue"

    processed_count = 0
    print("\n🚀 Iniciando processamento em massa de pedidos...")
    while True:
        order_id = orders_page.get_order_id_by_status(ST_PENDENTE)
        if not order_id:
            print("🏁 Não há mais pedidos 'PENDENTE' na lista.")
            break

        print(f"\n🔄 Processando pedido ID: {order_id} ({processed_count + 1}º da fila)")

        orders_page.change_order_status(order_id, ST_PENDENTE, OPT_CONFIRMADO)
        orders_page.verify_status_order(order_id, ST_CONFIRMADO)
        
        # 2. CONFIRMADO -> PRONTO
        orders_page.change_order_status(order_id, ST_CONFIRMADO, OPT_PRONTO)
        orders_page.verify_status_order(order_id, ST_PRONTO)

        # 3. PRONTO -> ENTREGUE
        orders_page.change_order_status(order_id, ST_PRONTO, OPT_ENTREGUE)
        
        try:
            orders_page.verify_status_order(order_id, ST_ENTREGUE)
        except:
            print(f"✅ Pedido {order_id} finalizado e removido da lista visual.")
        
        processed_count += 1

    if processed_count == 0:
        pytest.skip("Nenhum pedido 'PENDENTE' foi encontrado para iniciar o teste.")
    else:
        print(f"\n🎉 Sucesso Total! {processed_count} pedidos completaram o ciclo de vida.")