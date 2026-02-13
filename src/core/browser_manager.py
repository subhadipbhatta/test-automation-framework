"""
Browser driver management and context initialization
"""

import logging
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page


logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages browser lifecycle and contexts"""

    def __init__(self, browser_type: str = "chromium", headless: bool = True):
        """
        Initialize browser manager.

        Args:
            browser_type: Browser type (chromium, firefox, webkit)
            headless: Run in headless mode
        """
        self.browser_type = browser_type
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None

    async def launch_browser(self, **kwargs: Any) -> Browser:
        """
        Launch browser.

        Args:
            **kwargs: Additional arguments for browser launch

        Returns:
            Browser instance
        """
        self.playwright = await async_playwright().start()

        browser_launch_args = {
            "headless": self.headless,
            **kwargs
        }

        logger.info(f"Launching {self.browser_type} browser with args: {browser_launch_args}")

        if self.browser_type == "chromium":
            self.browser = await self.playwright.chromium.launch(**browser_launch_args)
        elif self.browser_type == "firefox":
            self.browser = await self.playwright.firefox.launch(**browser_launch_args)
        elif self.browser_type == "webkit":
            self.browser = await self.playwright.webkit.launch(**browser_launch_args)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        return self.browser

    async def create_context(self, **kwargs: Any) -> BrowserContext:
        """
        Create browser context.

        Args:
            **kwargs: Context options

        Returns:
            BrowserContext instance
        """
        if not self.browser:
            raise RuntimeError("Browser not launched. Call launch_browser() first.")

        logger.info(f"Creating browser context with options: {kwargs}")
        context = await self.browser.new_context(**kwargs)
        return context

    async def create_page(self, context: BrowserContext) -> Page:
        """
        Create a page in context.

        Args:
            context: BrowserContext

        Returns:
            Page instance
        """
        logger.info("Creating new page")
        page = await context.new_page()
        return page

    async def close_page(self, page: Page) -> None:
        """
        Close a page.

        Args:
            page: Page to close
        """
        logger.info("Closing page")
        await page.close()

    async def close_context(self, context: BrowserContext) -> None:
        """
        Close a browser context.

        Args:
            context: Context to close
        """
        logger.info("Closing browser context")
        await context.close()

    async def close_browser(self) -> None:
        """Close browser"""
        if self.browser:
            logger.info("Closing browser")
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

    async def __aenter__(self):
        """Async context manager entry"""
        await self.launch_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_browser()
