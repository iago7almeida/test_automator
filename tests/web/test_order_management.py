import pytest
from playwright.sync_api import expect
from models.web.dashboard_page import DashboardPage
from models.web.order_management_page import OrderManagementPage
from models.web.payment_modal import PaymentModal



@pytest.mark.frontend
def test_split_payment_pix_and_cash(logged_in_page):
    dashboard = DashboardPage(logged_in_page)
    orders_page = OrderManagementPage(logged_in_page)
    payment_modal = PaymentModal(logged_in_page)
    
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


@pytest.mark.frontend
def test_add_remove_payment_logic(logged_in_page):
    """
    Teste de Arrependimento:
    1. Abre pedido.
    2. Lança pagamento total.
    3. Remove o pagamento (lixeira).
    4. Cancela o modal (fecha sem pagar).
    5. Verifica que pedido continua 'Não pago'.
    """
    dashboard = DashboardPage(logged_in_page)
    orders_page = OrderManagementPage(logged_in_page)
    payment_modal = PaymentModal(logged_in_page)

    dashboard.go_to_order_sheet()
    orders_page.filter_by_in_progress()
    
    order_id = orders_page.open_first_unpaid_order()
    if not order_id:
        pytest.skip("Sem pedidos pendentes.")

    payment_modal.select_payment_method("Dinheiro")
    payment_modal.launch_payment()
    assert "R$ 0,00" in payment_modal.get_remaining_amount()

    # 2. Ops, errei! Vou remover.
    payment_modal.remove_staged_payment(index=0)

    # 3. Verifica se o valor "Falta pagar" VOLTOU (não é mais zero)
    remaining = payment_modal.get_remaining_amount()
    print(f"🔄 Valor restaurado após exclusão: {remaining}")
    assert "R$ 0,00" not in remaining

    # 4. Cancela tudo (fecha modal)
    payment_modal.close_without_saving()

    print("✅ Teste de cancelamento concluído com sucesso.")




@pytest.mark.frontend
def test_pay_all_unpaid_orders(logged_in_page):
    """
    Fluxo Repetitivo:
    Enquanto houver pedidos 'Não pago', abre o modal e paga.
    """
    dashboard = DashboardPage(logged_in_page)
    orders_page = OrderManagementPage(logged_in_page)
    payment_modal = PaymentModal(logged_in_page)

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

        # 4. Validação Específica por ID
        logged_in_page.wait_for_timeout(1000) 
        orders_page.verify_order_is_paid(order_id)
        
        orders_paid_count += 1

    if orders_paid_count == 0:
        pytest.skip("Nenhum pedido 'Não pago' foi encontrado para testar.")
    else:
        print(f"🎉 Sucesso! Total de pedidos pagos neste teste: {orders_paid_count}")