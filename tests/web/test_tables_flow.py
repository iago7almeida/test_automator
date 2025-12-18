import pytest

from models.web.dashboard_page import DashboardPage
from models.web.order_sheet_page import OrderSheetPage
from models.web.tables_page import TablesPage


@pytest.mark.frontend
def test_join_and_transfer_order(logged_in_page):
    """Exemplo: fluxo de UI usando fixtures compartilhadas (Playwright)."""
    page = logged_in_page
    dashboard = DashboardPage(page)
    tables = TablesPage(page)
    order_sheet = OrderSheetPage(page)

    dashboard.go_to_tables()
    assert tables.select_table(1)
    tables.join_tabs_in_a_table()
    order_sheet.open_order(1)
    order_sheet.transfer_order(2)
