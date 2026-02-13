"""
Example login page object
"""

import logging
from playwright.async_api import Page
from src.core.base_page import BasePage


logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page object"""

    # Locators
    USERNAME_INPUT = 'input[id="username"]'
    PASSWORD_INPUT = 'input[id="password"]'
    LOGIN_BUTTON = 'button[id="login"]'
    ERROR_MESSAGE = '.error-message'
    SUCCESS_MESSAGE = '.success-message'

    async def wait_for_page_load(self) -> None:
        """Wait for login page to load"""
        await self.wait_for_selector(self.USERNAME_INPUT)

    async def enter_username(self, username: str) -> None:
        """
        Enter username.

        Args:
            username: Username to enter
        """
        await self.fill_text(self.USERNAME_INPUT, username)
        logger.info(f"Entered username: {username}")

    async def enter_password(self, password: str) -> None:
        """
        Enter password.

        Args:
            password: Password to enter
        """
        await self.fill_text(self.PASSWORD_INPUT, password)
        logger.info("Entered password")

    async def click_login(self) -> None:
        """Click login button"""
        await self.click(self.LOGIN_BUTTON)
        logger.info("Clicked login button")

    async def login(self, username: str, password: str) -> None:
        """
        Perform login.

        Args:
            username: Username
            password: Password
        """
        await self.enter_username(username)
        await self.enter_password(password)
        await self.click_login()

    async def get_error_message(self) -> str:
        """
        Get error message.

        Returns:
            Error message text
        """
        return await self.get_text(self.ERROR_MESSAGE)

    async def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error is displayed
        """
        return await self.is_visible(self.ERROR_MESSAGE)

    async def is_success_displayed(self) -> bool:
        """
        Check if success message is displayed.

        Returns:
            True if success message is displayed
        """
        return await self.is_visible(self.SUCCESS_MESSAGE)
