import datetime
import logging
from pathlib import Path

from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

        self.title = page.locator('h2:text("Dashboard")')
        self.menu_opened = page.locator('[hoverlabel="Menu"]')
        self.new_order_button = page.get_by_label("newOrder")
        self.order_sheet_button = page.get_by_label("Gestão de pedidos")
        self.tables_button = page.locator('[hoverlabel="Todas as Mesas"]')
        self.cash_manager_button = page.get_by_label("Gerenciador de caixa")
        self.clients_button = page.locator('[hoverlabel="Clientes"]')
        self.logout_button = page.get_by_role("button", name="Sair")

    def login_verification_sucessfull(self):
        # Some deployments may not show the exact H2 title; accept either the title or the presence
        # of a logout button/menu as evidence of a successful login.
        try:
            expect(self.title).to_be_visible(timeout=5000)
            logger.debug("Dashboard title visible after login")
            return
        except Exception:
            logger.debug("Dashboard title not visible; checking logout button and capturing debug info")

        try:
            expect(self.logout_button).to_be_visible(timeout=10000)
            logger.debug("Logout button visible — login considered successful")
            return
        except Exception as exc:
            # Collect debug context: URL and a screenshot
            ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            try:
                Path("tests/screenshots").mkdir(parents=True, exist_ok=True)
                self.page.screenshot(path=f"tests/screenshots/dashboard_login_failure_{ts}.png")
                logger.error("Login verification failed — screenshot written: tests/screenshots/dashboard_login_failure_%s.png", ts)
            except Exception:
                logger.exception("Failed to write dashboard failure screenshot")

            logger.error("Login verification failed: page.url=%s; exception=%s", self.page.url, exc)
            raise

    def handle_payment_modal_if_appears(self):
        close_modal_button = self.page.locator(".ReactModal__Overlay")

        try:
            expect(close_modal_button).to_be_visible(timeout=7000)
            print("Modal de pagamento encontrado. Fechando...")
            close_modal_button.click(position={"x": 10, "y": 10})
        except Exception:
            print("Modal de pagamento não apareceu. Continuando...")

    def logout_system(self):
        self.menu_opened.click()
        self.logout_button.click()

    def go_to_new_order(self):
        self.new_order_button.click()

    def go_to_clients(self):
        self.clients_button.click()

    def go_to_order_sheet(self):
        self.order_sheet_button.click()

    def go_to_tables(self):
        self.tables_button.click()

    def go_to_cache_menager(self):
        self.cash_manager_button.click()
