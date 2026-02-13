"""
Web automation tests for home page functionality
"""

import pytest
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage
from src.utils.config import Config


@pytest.mark.web
@pytest.mark.asyncio
class TestHomePage:
    """Home page tests"""

    @pytest.fixture
    async def logged_in_page(self, page, config):
        """Fixture to provide logged-in page"""
        login_page = LoginPage(page, config.base_url)
        await login_page.navigate()
        await login_page.wait_for_page_load()
        await login_page.login("test_user", "Test@1234")
        yield page

    async def test_welcome_message_displayed(self, logged_in_page, config):
        """Test welcome message is displayed"""
        home_page = HomePage(logged_in_page, config.base_url)
        assert await home_page.is_logged_in()

        welcome_msg = await home_page.get_welcome_message()
        assert welcome_msg, "Welcome message is empty"

    async def test_user_menu_clickable(self, logged_in_page, config):
        """Test user menu is clickable"""
        home_page = HomePage(logged_in_page, config.base_url)
        assert await home_page.is_visible(home_page.USER_MENU)

    async def test_navigation_menu_visible(self, logged_in_page, config):
        """Test navigation menu is visible"""
        home_page = HomePage(logged_in_page, config.base_url)
        assert await home_page.is_visible(home_page.NAVIGATION_MENU)
