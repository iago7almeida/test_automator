# Estrutura de Testes: Backend / Frontend / Mobile

Este documento descreve a nova organização de testes para separar responsabilidades e facilitar execução paralela/CI.

Organização proposta:

- `tests/`
  - `backend/`  -> testes de API e integração (marcador: `@pytest.mark.backend`)
  - `frontend/` -> testes de UI (Playwright) (marcador: `@pytest.mark.frontend`)
  - `mobile/`   -> testes mobile (scaffold para Appium/Playwright mobile) (marcador: `@pytest.mark.mobile`)
  - `common/`   -> fixtures e helpers compartilhados (`tests/common/conftest.py`)

Padrões e boas práticas:

- Usar fixtures do `tests/common/conftest.py` (ex: `logged_in_page`) para evitar repetição.
- Marcar testes com `@pytest.mark.backend` / `@pytest.mark.frontend` / `@pytest.mark.mobile` e usar `pytest -m`.
- Backend tests devem usar `APIAuthManager` (`config/api_auth.py`) e `get_config()` (`config/settings.py`).
- Frontend tests devem usar Page Objects em `pages/` (ex: `LoginPage`, `DashboardPage`, `TablesPage`).
- Evitar `time.sleep()`; usar waits explícitos do Playwright.

Execução:

- Apenas backend:
```
pytest -m backend -q
```
- Apenas frontend (headed):
```
HEADLESS=false pytest -m frontend -q
```
- Em CI: paralelizar por tipo ou por marcadores.

Referências:

- Fixtures raiz: `tests/conftest.py`
- Exemplo API auth: `tests/backend/test_api_health.py`
- Page Objects: `docs/Pages.md`
- Config: `config/settings.py`
- APIAuthManager: `config/api_auth.py`
