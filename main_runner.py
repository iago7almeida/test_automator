# main_runner.py
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.tables_page import TablesPage
# Importar outras pages e o que mais for necessário

def run_table_order_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome", args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        page.evaluate("document.body.style.zoom='80%'")

        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        tables_page = TablesPage(page)

        try:
            login_page.navigate_to_login_page()
            login_page.login("teste_teste@gmail.com", "123")
            dashboard_page.navigate_to_tables()

            for i in range(1, 3): # Teste com 2 mesas
                print(f"Processando Mesa: {i}")
                tables_page.open_or_add_to_table(i)
                # Adicionar asserções
            
            # Exemplo de cancelamento
            # tables_page.cancel_order_sheet_for_table(1)

        except Exception as e:
            print(f"Erro na execução da automação: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_table_order_flow()
    # Você pode chamar outros fluxos de teste aqui
    # run_single_order_flow()