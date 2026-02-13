"""
Example home page object
"""

import logging
from playwright.async_api import Page
from src.core.base_page import BasePage


logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Home page object"""

    # Locators
    WELCOME_MESSAGE = '.welcome-message'
    USER_MENU = '.user-menu'
    LOGOUT_BUTTON = 'button[id="logout"]'
    NAVIGATION_MENU = '.navigation-menu'

    async def wait_for_page_load(self) -> None:
        """Wait for home page to load"""
        await self.wait_for_selector(self.WELCOME_MESSAGE)

    async def get_welcome_message(self) -> str:
        """
        Get welcome message.

        Returns:
            Welcome message text
        """
        return await self.get_text(self.WELCOME_MESSAGE)

    async def click_user_menu(self) -> None:
        """Click user menu"""
        await self.click(self.USER_MENU)
        logger.info("Clicked user menu")

    async def click_logout(self) -> None:
        """Click logout button"""
        await self.click(self.LOGOUT_BUTTON)
        logger.info("Clicked logout button")

    async def logout(self) -> None:
        """Perform logout"""
        await self.click_user_menu()
        await self.click_logout()

    async def is_logged_in(self) -> bool:
        """
        Check if user is logged in.

        Returns:
            True if user is logged in
        """
        return await self.is_visible(self.WELCOME_MESSAGE)
