# conftest.py
import pytest
import time
import allure
import os
from playwright.sync_api import sync_playwright
from config.settings import get_config
from models.web.login_page import LoginPage
from utils.perfomance_tracker import PerformanceTracker

cfg = get_config()

@pytest.fixture
def context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=cfg.HEADLESS)

        context = browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720}
        )

        yield context

        context.close()
        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item):
    start = time.time()
    yield
    duration = time.time() - start

    PerformanceTracker.record(f"TESTE: {item.nodeid}", duration)

@pytest.fixture
def logged_in_page(context):
    page = context.new_page()

    login = LoginPage(page)
    login.navigate()
    login.login(cfg.USERNAME, cfg.PASSWORD)

    yield page

    video = page.video

    page.close()

    if video:
        video_path = video.path()
        if os.path.exists(video_path):
            allure.attach.file(
                video_path,
                name=os.path.basename(video_path),
                attachment_type=allure.attachment_type.WEBM,
            )
