"""
Web automation tests for login functionality
"""

import pytest
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage
from src.utils.config import Config


@pytest.mark.web
@pytest.mark.asyncio
class TestLogin:
    """Login tests"""

    async def test_successful_login(self, page, config):
        """Test successful login"""
        # Initialize pages
        login_page = LoginPage(page, config.base_url)

        # Navigate to login page
        await login_page.navigate()

        # Wait for page to load
        await login_page.wait_for_page_load()

        # Perform login
        await login_page.login("test_user", "Test@1234")

        # Verify successful login
        home_page = HomePage(page, config.base_url)
        assert await home_page.is_logged_in(), "Login was not successful"

    async def test_failed_login_with_invalid_credentials(self, page, config):
        """Test login with invalid credentials"""
        login_page = LoginPage(page, config.base_url)

        # Navigate to login page
        await login_page.navigate()

        # Wait for page to load
        await login_page.wait_for_page_load()

        # Attempt login with invalid credentials
        await login_page.login("invalid_user", "wrong_password")

        # Verify error message
        assert await login_page.is_error_displayed(), "Error message was not displayed"
        error_msg = await login_page.get_error_message()
        assert error_msg, "Error message is empty"

    async def test_login_page_elements_visible(self, page, config):
        """Test that all login page elements are visible"""
        login_page = LoginPage(page, config.base_url)

        # Navigate to login page
        await login_page.navigate()

        # Wait for page to load
        await login_page.wait_for_page_load()

        # Verify elements are visible
        assert await login_page.is_visible(login_page.USERNAME_INPUT)
        assert await login_page.is_visible(login_page.PASSWORD_INPUT)
        assert await login_page.is_visible(login_page.LOGIN_BUTTON)

    async def test_login_and_logout(self, page, config):
        """Test login and logout flow"""
        login_page = LoginPage(page, config.base_url)
        home_page = HomePage(page, config.base_url)

        # Navigate and login
        await login_page.navigate()
        await login_page.wait_for_page_load()
        await login_page.login("test_user", "Test@1234")

        # Verify logged in
        assert await home_page.is_logged_in()

        # Logout
        await home_page.logout()

        # Verify logged out (back to login page)
        await login_page.wait_for_page_load()
        assert await login_page.is_visible(login_page.USERNAME_INPUT)
