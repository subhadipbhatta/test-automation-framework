"""
Base Page Object Model implementation for web automation
"""

import logging
from typing import Any, Callable, Optional, Union
from abc import ABC, abstractmethod

from playwright.async_api import Page, Locator, TimeoutError as PlaywrightTimeoutError


logger = logging.getLogger(__name__)


class BasePage(ABC):
    """
    Base page class that all page objects should inherit from.
    Provides common functionality for element interactions and navigation.
    """

    def __init__(self, page: Page, base_url: str = ""):
        """
        Initialize the page object.

        Args:
            page: Playwright Page instance
            base_url: Base URL for the application
        """
        self.page = page
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)

    async def navigate(self, path: str = "") -> None:
        """
        Navigate to a URL.

        Args:
            path: Path to append to base_url
        """
        url = f"{self.base_url}{path}" if path else self.base_url
        self.logger.info(f"Navigating to: {url}")
        await self.page.goto(url)

    async def fill_text(self, selector: str, text: str) -> None:
        """
        Fill text in an input field.

        Args:
            selector: Element selector
            text: Text to fill
        """
        self.logger.info(f"Filling text '{text}' in {selector}")
        await self.page.fill(selector, text)

    async def click(self, selector: str) -> None:
        """
        Click on an element.

        Args:
            selector: Element selector
        """
        self.logger.info(f"Clicking on {selector}")
        await self.page.click(selector)

    async def click_locator(self, locator: Locator) -> None:
        """
        Click on a locator element.

        Args:
            locator: Playwright Locator
        """
        self.logger.info(f"Clicking on locator")
        await locator.click()

    async def get_text(self, selector: str) -> str:
        """
        Get text content of an element.

        Args:
            selector: Element selector

        Returns:
            Text content
        """
        self.logger.info(f"Getting text from {selector}")
        return await self.page.text_content(selector) or ""

    async def get_locator_text(self, locator: Locator) -> str:
        """
        Get text content from a locator.

        Args:
            locator: Playwright Locator

        Returns:
            Text content
        """
        return await locator.text_content() or ""

    async def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if element is visible.

        Args:
            selector: Element selector
            timeout: Timeout in milliseconds

        Returns:
            True if element is visible, False otherwise
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            return True
        except PlaywrightTimeoutError:
            return False

    async def is_enabled(self, selector: str) -> bool:
        """
        Check if element is enabled.

        Args:
            selector: Element selector

        Returns:
            True if enabled, False otherwise
        """
        return await self.page.is_enabled(selector)

    async def select_option(self, selector: str, value: Union[str, int]) -> None:
        """
        Select an option from a dropdown.

        Args:
            selector: Dropdown selector
            value: Option value
        """
        self.logger.info(f"Selecting option '{value}' from {selector}")
        await self.page.select_option(selector, str(value))

    async def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """
        Get attribute value of an element.

        Args:
            selector: Element selector
            attribute: Attribute name

        Returns:
            Attribute value or None
        """
        return await self.page.get_attribute(selector, attribute)

    async def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        """
        Wait for element to appear in DOM.

        Args:
            selector: Element selector
            timeout: Timeout in milliseconds
        """
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def wait_for_load_state(self, state: str = "networkidle") -> None:
        """
        Wait for page load state.

        Args:
            state: Load state (load, domcontentloaded, networkidle)
        """
        await self.page.wait_for_load_state(state)

    async def get_locator(self, selector: str) -> Locator:
        """
        Get a locator for an element.

        Args:
            selector: Element selector

        Returns:
            Playwright Locator
        """
        return self.page.locator(selector)

    async def take_screenshot(self, path: str) -> None:
        """
        Take a screenshot of the page.

        Args:
            path: File path to save screenshot
        """
        self.logger.info(f"Taking screenshot: {path}")
        await self.page.screenshot(path=path)

    async def execute_script(self, script: str, *args: Any) -> Any:
        """
        Execute JavaScript on the page.

        Args:
            script: JavaScript code
            *args: Arguments to pass to script

        Returns:
            Script execution result
        """
        return await self.page.evaluate(script, *args)

    async def get_title(self) -> str:
        """
        Get page title.

        Returns:
            Page title
        """
        return await self.page.title()

    async def get_current_url(self) -> str:
        """
        Get current page URL.

        Returns:
            Current URL
        """
        return self.page.url

    async def close(self) -> None:
        """Close the page"""
        await self.page.close()

    @abstractmethod
    async def wait_for_page_load(self) -> None:
        """
        Wait for page to fully load.
        Must be implemented by subclasses.
        """
        pass
