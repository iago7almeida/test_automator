# ==============================================================================
# Login Page - Page Object Model
# ==============================================================================

import logging

from playwright.sync_api import Page

from config.settings import get_config

logger = logging.getLogger(__name__)


class LoginPage:
    """
    Representa a página de login da aplicação Gestão Pigz.

    Encapsula todos os elementos e ações relacionados ao processo de autenticação.
    """

    # Localizadores
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button:text('Entrar')"
    ERROR_MESSAGE = "text='E-mail ou senha inválidos'"

    def __init__(self, page: Page):
        """
        Inicializa a página de login.

        Args:
            page: Instância de Page do Playwright
        """
        self.page = page
        self.config = get_config()

        # Armazenar locators para reutilização
        self.email_input = page.locator(self.EMAIL_INPUT)
        self.password_input = page.locator(self.PASSWORD_INPUT)
        self.login_button = page.get_by_role("button", name="Entrar")

    def navigate(self):
        """
        Navega para a página de login da aplicação.

        Raises:
            TimeoutError: Se a página não carregar no tempo esperado
        """
        login_url = f"{self.config.BASE_URL}/sign-in"
        logger.info("Navegando para: %s", login_url)

        self.page.goto(login_url)
        self.page.wait_for_load_state("networkidle")

        logger.info("Página de login carregada com sucesso")

    def login(self, email: str, password: str):
        """
        Realiza o login na aplicação.

        Args:
            email: Email do usuário
            password: Senha do usuário

        Raises:
            TimeoutError: Se elementos não forem encontrados
            AssertionError: Se credenciais forem inválidas
        """
        logger.info("Realizando login com usuário: %s", email)

        try:
            self.email_input.fill(email)
            self.password_input.fill(password)
            self.login_button.click()

            # Aguardar navegação pós-login
            self.page.wait_for_load_state("networkidle")
            logger.info("Credenciais enviadas com sucesso")

        except TimeoutError as e:
            logger.error("Timeout ao preencher formulário de login: %s", e)
            raise
        except Exception as e:
            logger.error("Erro durante login: %s", e)
            raise

    def get_error_message(self) -> str:
        """
        Obtém mensagem de erro de login se houver.

        Returns:
            Mensagem de erro ou string vazia se não houver erro
        """
        try:
            error = self.page.locator(self.ERROR_MESSAGE)
            if error.is_visible():
                message = error.text_content()
                logger.warning("Erro de login: %s", message)
                return message
        except Exception as e:
            logger.debug("Nenhum erro encontrado: %s", e)

        return ""

    def navigate_to_login_page(self):
        """
        Alias para navigate() - mantém compatibilidade com testes existentes.
        """
        self.navigate()
