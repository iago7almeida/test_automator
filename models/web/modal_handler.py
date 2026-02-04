import time
import logging
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def keep_open(page):
    while True:
        try:
            modal_visible = page.query_selector("header.sc-60baa1a1-0.iranfm")
            if modal_visible:
                logging.info("Modal detectado! Clicando no botão 'Manter aberto'.")
                page.click("button.sc-60baa1a1-4.kcgrGw")
                break

            time.sleep(0.5)
        except Exception as e:
            logging.info(f"Erro ao verificar modal: {e}")
            time.sleep(0.5)


def close_seller(page):
    while True:
        try:
            modal_visible = page.query_selector("header.sc-60baa1a1-0.iranfm")
            if modal_visible:
                logging.info("Modal detectado! Clicando no botão 'Manter aberto'.")
                page.click("button.sc-60baa1a1-4.kcgrGw")
                break
            time.sleep(0.5)
        except Exception as e:
            logging.info(f"Erro ao verificar modal: {e}")
            time.sleep(0.5)


def registered_payments(page, timeout: int = 2):
    start_time = time.time()
    while True:
        try:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                logging.info("Tempo limite atingido; o modal não foi detectado.")
                break

            modal_visible = page.query_selector('h1:has-text("Pagamentos registrados")')
            if modal_visible:
                logging.info("Modal detectado! Clicando no botão 'Manter aberto'.")
                page.click('button:has-text("Ok, entendi")')
                break
            time.sleep(0.5)
        except Exception as e:
            logging.info(f"Erro ao verificar modal: {e}")
            time.sleep(0.5)


def order_sheet_opened(page: Page) -> bool:
    selector = 'div[class="sc-fa3a0b24-2 bAbjMs"]'
    try:
        page.wait_for_selector(selector, state="visible", timeout=2000)
        return True
    except PlaywrightTimeoutError:
        return False


def multiple_commands(page: Page) -> bool:
    selector = 'label[class="sc-32e0be68-12 gTfRrT"]'
    try:
        page.wait_for_selector(selector, state="visible", timeout=2000)
        return True
    except PlaywrightTimeoutError:
        return False


def tax_note(page: Page):
    selector = 'div[class="sc-22f52115-2 dsJuxn"]'
    try:
        page.wait_for_selector(selector, state="visible", timeout=3000)
        return True
    except PlaywrightTimeoutError:
        return False
