import time
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError


def Keep_open(page): #Manter aberto
    while True:
        try:
            # Verifica se o modal está visível
            modal_visible = page.query_selector('header.sc-60baa1a1-0.iranfm')
            if modal_visible:
                print("Modal detectado! Clicando no botão 'Manter aberto'.") 
                page.click('button.sc-60baa1a1-4.kcgrGw') # Clica no botão "Manter aberto"
                break
            else:
                time.sleep(0.5)
        except Exception as e:
            print(f"Erro ao verificar modal: {e}")
            time.sleep(0.5)  # Espera antes de tentar novamente
#-----------------------------------------------------------------------------------------------------------------------------------           
def Close_seller(page): 
    while True:
        try:
            # Verifica se o modal está visível
            modal_visible = page.query_selector('header.sc-60baa1a1-0.iranfm')
            if modal_visible:
                print("Modal detectado! Clicando no botão 'Manter aberto'.") 
                page.click('button.sc-60baa1a1-4.kcgrGw') # Clica no botão "Manter aberto"
                break
            else:
                time.sleep(0.5)
        except Exception as e:
            print(f"Erro ao verificar modal: {e}")
            time.sleep(0.5)  # Espera antes de tentar novamente
#---------------------------------------------------------------------------------------------------------------------------------------------------            
def registered_payments(page, timeout: int = 2): #quando for cancelar comanda em que haja pagamentos registrados
    start_time = time.time()
    while True:
        try:
            # Calcula o tempo decorrido
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print("Tempo limite atingido; o modal não foi detectado.")
                break
            
            # Verifica se o modal está visível
            modal_visible = page.query_selector('h1:has-text("Pagamentos registrados")')
            if modal_visible:
                print("Modal detectado! Clicando no botão 'Manter aberto'.")
                page.click('button:has-text("Ok, entendi")')  # Clica em "Ok, entendi que você não gosta do Raça Negra"
                break
            else:
                time.sleep(0.5)
        except Exception as e:
            print(f"Erro ao verificar modal: {e}")
            time.sleep(0.5)  # Pausa breve antes de tentar novamente
##-------------------------------------------------------------------------------------------------------------------------------------------------------            
def orderSheet_opened(page: Page) -> bool:
    selector = 'div[class="sc-fa3a0b24-2 bAbjMs"]'
    try:
        page.wait_for_selector(selector, state="visible", timeout=2000)
        return True
    except PlaywrightTimeoutError:
        return False
#-----------------------------------------------------------------------------------------------------------------------------------------------   
def multiple_commands(page: Page) -> bool:
    selector = 'label[class="sc-32e0be68-12 gTfRrT"]'
    try:
        page.wait_for_selector(selector, state="visible", timeout=2000)        
        return True
    except PlaywrightTimeoutError:
        return False
    
#----------------------------------------------------------------------------------------------------------------------------------------------
def tax_note(page: Page):
    selector = 'div[class="sc-22f52115-2 dsJuxn"]'
    try:
        page.wait_for_selector(selector, state="visible", timeout=3000)
        return True
    except PlaywrightTimeoutError:
        return False