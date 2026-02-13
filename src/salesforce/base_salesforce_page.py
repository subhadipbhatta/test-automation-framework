"""
Salesforce page object base class
"""

import logging
from typing import Optional
from playwright.async_api import Page

from src.core.base_page import BasePage


logger = logging.getLogger(__name__)


class SalesforcePage(BasePage):
    """Base class for Salesforce page objects"""

    SALESFORCE_BASE_URL = "https://login.salesforce.com"

    def __init__(self, page: Page, base_url: str = SALESFORCE_BASE_URL):
        """
        Initialize Salesforce page object.

        Args:
            page: Playwright Page instance
            base_url: Salesforce base URL
        """
        super().__init__(page, base_url)

    async def wait_for_page_load(self) -> None:
        """Wait for Salesforce page to fully load"""
        await self.wait_for_load_state("networkidle")

    async def login(self, username: str, password: str) -> None:
        """
        Login to Salesforce.

        Args:
            username: Salesforce username
            password: Salesforce password
        """
        # Navigate to login page
        await self.navigate()

        # Wait for login form to appear
        await self.wait_for_selector('input[name="username"]')

        # Fill credentials
        await self.fill_text('input[name="username"]', username)
        await self.fill_text('input[name="pw"]', password)

        # Click login button
        await self.click('input[id="Login"]')

        # Wait for page to load after login
        await self.wait_for_page_load()

        logger.info("Salesforce login successful")

    async def logout(self) -> None:
        """Logout from Salesforce"""
        # Click user profile menu
        await self.click('[id="userNavLabel"]')

        # Click logout
        await self.click('a[title="Logout"]')

        logger.info("Salesforce logout successful")

    async def navigate_to_object(self, object_name: str) -> None:
        """
        Navigate to a Salesforce object.

        Args:
            object_name: Object API name (e.g., 'Account', 'Contact')
        """
        # Click on App Launcher
        await self.click('[aria-label="App Launcher"]')

        # Wait for search box
        await self.wait_for_selector('input[placeholder="Search apps or items..."]')

        # Search for object
        await self.fill_text('input[placeholder="Search apps or items..."]', object_name)

        # Wait and click on result
        await self.wait_for_selector(f'//a[contains(., "{object_name}")]')
        await self.click(f'//a[contains(., "{object_name}")]')

        # Wait for page to load
        await self.wait_for_page_load()

        logger.info(f"Navigated to {object_name}")

    async def search_record(self, search_term: str) -> None:
        """
        Search for a record using global search.

        Args:
            search_term: Search term
        """
        # Click on global search
        await self.click('[aria-label="Search"]')

        # Type search term
        await self.fill_text('input[placeholder="Search..."]', search_term)

        # Wait for results
        await self.wait_for_selector('.listContent')

        logger.info(f"Searched for: {search_term}")

    async def create_record(self, object_name: str, field_values: dict) -> str:
        """
        Create a new record.

        Args:
            object_name: Object API name
            field_values: Dictionary of field API names and values

        Returns:
            Record ID
        """
        # Navigate to object
        await self.navigate_to_object(object_name)

        # Click new button
        await self.click('div[title="New"]')

        # Wait for form
        await self.wait_for_selector('form')

        # Fill form fields
        for field_name, field_value in field_values.items():
            await self.fill_text(f'input[data-label="{field_name}"]', field_value)

        # Click save button
        await self.click('button[title="Save"]')

        # Wait for success
        await self.wait_for_page_load()

        # Extract and return record ID from URL
        current_url = await self.get_current_url()
        record_id = current_url.split('/')[-1]

        logger.info(f"Record created: {record_id}")
        return record_id

    async def update_record(self, field_values: dict) -> None:
        """
        Update current record fields.

        Args:
            field_values: Dictionary of field API names and values
        """
        # Click edit button
        await self.click('button[title="Edit"]')

        # Wait for form
        await self.wait_for_selector('form')

        # Update fields
        for field_name, field_value in field_values.items():
            await self.fill_text(f'input[data-label="{field_name}"]', field_value)

        # Click save
        await self.click('button[title="Save"]')

        # Wait for success
        await self.wait_for_page_load()

        logger.info("Record updated")

    async def delete_record(self) -> None:
        """Delete current record"""
        # Click dropdown menu
        await self.click('[aria-label="More"]')

        # Click delete
        await self.click('[title="Delete"]')

        # Confirm deletion
        await self.click('button[title="Delete"]')

        logger.info("Record deleted")
