"""
Pytest configuration and fixtures
"""

import pytest
import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path

from src.core.browser_manager import BrowserManager
from src.utils.config import Config


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def config():
    """Load configuration"""
    return Config()


@pytest.fixture(scope="session")
async def browser_manager(config):
    """Create and manage browser"""
    manager = BrowserManager(
        browser_type=config.browser_type,
        headless=config.headless
    )
    await manager.launch_browser(
        slow_mo=config.playwright_slow_mo
    )
    yield manager
    await manager.close_browser()


@pytest.fixture
async def browser_context(browser_manager):
    """Create browser context"""
    context = await browser_manager.create_context(
        viewport={
            "width": browser_manager.browser_manager.playwright_viewport_width,
            "height": browser_manager.browser_manager.playwright_viewport_height,
        }
    )
    yield context
    await browser_manager.close_context(context)


@pytest.fixture
async def page(browser_context, browser_manager):
    """Create page"""
    page = await browser_manager.create_page(browser_context)
    yield page
    await browser_manager.close_page(page)


@pytest.fixture
def screenshot_dir(config):
    """Create screenshot directory"""
    report_dir = Path(config.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    return report_dir


@pytest.fixture
def test_data():
    """Provide test data"""
    return {
        "valid_user": {
            "username": "test_user",
            "password": "Test@1234"
        },
        "invalid_user": {
            "username": "invalid_user",
            "password": "wrong_password"
        }
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.failed and hasattr(item, "funcargs"):
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = item.funcargs.get("screenshot_dir")

            if screenshot_dir:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = screenshot_dir / f"failed_{item.name}_{timestamp}.png"

                # Take screenshot asynchronously
                async def take_ss():
                    await page.screenshot(path=str(screenshot_path))

                try:
                    asyncio.run(take_ss())
                    print(f"\nScreenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"Failed to take screenshot: {e}")
