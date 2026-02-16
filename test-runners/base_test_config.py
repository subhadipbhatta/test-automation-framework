"""
Base Test Configuration for Web Regression Test Suite
"""

import time
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TestResultData:
    """Test result data structure"""
    test_id: str
    test_name: str
    status: str
    duration: float
    screenshots: List[str]
    errors: List[str]
    assertions_passed: int
    assertions_failed: int

class BaseTestConfig:
    """Base configuration for all test cases"""
    
    BASE_URL = "https://demowebshop.tricentis.com"
    SCREENSHOT_DIR = "test-artifacts/screenshots"
    TEST_DATA_FILE = "Web_Regression_Test.json"
    
    @classmethod
    def setup_screenshot_directory(cls):
        """Create screenshot directory if it doesn't exist"""
        Path(cls.SCREENSHOT_DIR).mkdir(exist_ok=True)
        
    @classmethod
    def generate_screenshot_name(cls, test_id: str, step: int, description: str = "") -> str:
        """Generate unique screenshot filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_desc = description.replace(" ", "_").replace("/", "_") if description else ""
        return f"{cls.SCREENSHOT_DIR}/{test_id}_step_{step}_{safe_desc}_{timestamp}.png"

class DatabaseHelper:
    """Database operations helper"""
    
    @staticmethod
    def validate_user_exists(email: str) -> bool:
        """Validate if user exists in database"""
        logger.info(f"Database validation for user: {email}")
        # For demo purposes, return True (would integrate with actual DB)
        return True

class TestDataGenerator:
    """Generate test data for various scenarios"""
    
    @staticmethod
    def generate_user_data(gender: str = "Male") -> Dict[str, str]:
        """Generate random user data"""
        timestamp = str(int(time.time() * 1000))
        
        male_names = ["Michael", "John", "David", "Robert", "James"]
        female_names = ["Sarah", "Emily", "Jessica", "Ashley", "Jennifer"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
        
        first_names = male_names if gender == "Male" else female_names
        
        return {
            "gender": gender,
            "firstName": random.choice(first_names),
            "lastName": random.choice(last_names),
            "email": f"test.user.{timestamp}@testmail.com",
            "password": f"TestPass{timestamp[-4:]}!",
            "confirmPassword": f"TestPass{timestamp[-4:]}!",
            "timestamp": timestamp
        }
    
    @staticmethod
    def generate_address_data() -> Dict[str, str]:
        """Generate random address data"""
        return {
            "firstName": "Test",
            "lastName": "User",
            "address": f"{random.randint(100, 999)} Test Street",
            "city": "Test City",
            "zipCode": f"{random.randint(10000, 99999)}",
            "country": "United States",
            "phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        }

class PageObjectBase:
    """Base page object with common functionality"""
    
    def __init__(self, page):
        self.page = page
        self.screenshots = []
        
    async def take_screenshot(self, test_id: str, step: int, description: str = "") -> str:
        """Take screenshot and return filename"""
        BaseTestConfig.setup_screenshot_directory()
        filename = BaseTestConfig.generate_screenshot_name(test_id, step, description)
        await self.page.screenshot(path=filename, full_page=True)
        self.screenshots.append(filename)
        logger.info(f"Screenshot taken: {filename}")
        return filename
    
    async def wait_and_click(self, selector: str, timeout: int = 10000):
        """Wait for element and click with error handling"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            await self.page.wait_for_timeout(500)  # Small delay after click
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {e}")
            raise
    
    async def wait_and_fill(self, selector: str, text: str, timeout: int = 10000):
        """Wait for element and fill with error handling"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.fill(selector, text)
            await self.page.wait_for_timeout(300)  # Small delay after fill
        except Exception as e:
            logger.error(f"Failed to fill element {selector}: {e}")
            raise
    
    async def assert_element_visible(self, selector: str, timeout: int = 10000) -> bool:
        """Assert element is visible"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return await self.page.is_visible(selector)
        except Exception as e:
            logger.error(f"Element {selector} not visible: {e}")
            return False
    
    async def assert_text_present(self, text: str) -> bool:
        """Assert text is present on page"""
        try:
            content = await self.page.content()
            return text in content
        except Exception as e:
            logger.error(f"Text '{text}' not found: {e}")
            return False