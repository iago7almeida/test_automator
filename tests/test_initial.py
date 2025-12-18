import inspect

from config.settings import get_config
from models.web.base_page import BasePage


def test_base_page_importable():
    """Base smoke: BasePage class should be importable and have the expected API."""
    assert inspect.isclass(BasePage)
    # check expected methods exist
    for method in ("click", "fill", "navigate", "wait_for_selector"):
        assert hasattr(BasePage, method), f"BasePage missing method: {method}"


def test_config_loads_env_values():
    """Config smoke: get_config returns object with USERNAME/PASSWORD attributes."""
    cfg = get_config()
    assert hasattr(cfg, "USERNAME")
    assert hasattr(cfg, "PASSWORD")
    # values may be empty in CI; just ensure attributes exist and types are correct
    assert isinstance(cfg.USERNAME, str)
    assert isinstance(cfg.PASSWORD, str)
