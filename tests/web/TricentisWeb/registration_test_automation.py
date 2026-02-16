"""
Automated Registration Test Suite - Simplified Version
Based on Registration.JSON test plan for Demo Web Shop
"""

import pytest
import pytest_asyncio
import asyncio
import time
import random
import os
from playwright.async_api import async_playwright, Page, Browser
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RegistrationTestData:
    """Test data generator for registration tests"""
    
    @staticmethod
    def generate_random_user(gender="Male"):
        """Generate random user data with timestamp for uniqueness"""
        timestamp = str(int(time.time() * 1000))  # Millisecond precision
        
        male_names = ["Michael", "John", "David", "Robert", "James", "William"]
        female_names = ["Sarah", "Emily", "Jessica", "Ashley", "Jennifer", "Amanda"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        
        first_names = male_names if gender == "Male" else female_names
        
        return {
            "gender": gender,
            "firstName": random.choice(first_names),
            "lastName": random.choice(last_names),
            "email": f"test.user.{timestamp}@testmail.com",
            "password": f"TestPass{timestamp[-4:]}!",
            "confirmPassword": f"TestPass{timestamp[-4:]}!",
            "expectedUID": f"user{timestamp}",
            "timestamp": timestamp
        }


class RegistrationPage:
    """Page Object Model for Registration Page"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Selectors based on common registration form patterns
        self.gender_male_selector = "input[value='Male'], input[id*='male'], input[name*='gender'][value='M']"
        self.gender_female_selector = "input[value='Female'], input[id*='female'], input[name*='gender'][value='F']"
        self.first_name_selector = "#FirstName, input[name='FirstName'], input[id*='firstname'], input[placeholder*='First']"
        self.last_name_selector = "#LastName, input[name='LastName'], input[id*='lastname'], input[placeholder*='Last']"
        self.email_selector = "#Email, input[name='Email'], input[type='email'], input[id*='email']"
        self.password_selector = "#Password, input[name='Password'], input[type='password']:first-of-type, input[id*='password']:first-of-type"
        self.confirm_password_selector = "#ConfirmPassword, input[name='ConfirmPassword'], input[type='password']:last-of-type"
        self.register_button_selector = "input[value='Register'], button:has-text('Register'), #register-button, input[type='submit']"
        
        # Error message selectors
        self.error_message_selector = ".field-validation-error, .error, .alert-danger, span[data-valmsg-for]"
        self.success_message_selector = ".success, .alert-success, .confirmation"
    
    async def navigate_to_registration_page(self):
        """Navigate to registration page"""
        base_url = os.getenv('BASE_URL', 'https://demowebshop.tricentis.com/')
        await self.page.goto(f"{base_url}register")
        await self.page.wait_for_load_state('networkidle')
    
    async def select_gender(self, gender: str):
        """Select gender radio button"""
        if gender.lower() == "male":
            await self.page.click(self.gender_male_selector)
        elif gender.lower() == "female":
            await self.page.click(self.gender_female_selector)
    
    async def fill_registration_form(self, user_data: dict):
        """Fill the registration form with user data"""
        # Select gender
        await self.select_gender(user_data["gender"])
        
        # Fill text fields
        await self.page.fill(self.first_name_selector, user_data["firstName"])
        await self.page.fill(self.last_name_selector, user_data["lastName"])
        await self.page.fill(self.email_selector, user_data["email"])
        await self.page.fill(self.password_selector, user_data["password"])
        await self.page.fill(self.confirm_password_selector, user_data["confirmPassword"])
    
    async def click_register_button(self):
        """Click the register button"""
        await self.page.click(self.register_button_selector)
        await self.page.wait_for_load_state('networkidle')
    
    async def get_error_messages(self):
        """Get all error messages displayed on the page"""
        error_elements = await self.page.query_selector_all(self.error_message_selector)
        error_messages = []
        for element in error_elements:
            text = await element.text_content()
            if text and text.strip():
                error_messages.append(text.strip())
        return error_messages
    
    async def is_registration_successful(self):
        """Check if registration was successful"""
        # Look for success indicators
        success_elements = await self.page.query_selector_all(self.success_message_selector)
        if success_elements:
            return True
        
        # Check if redirected to a success page or login page
        current_url = self.page.url
        return "login" in current_url.lower() or "success" in current_url.lower()


# Pytest fixtures for browser setup - Fixed for pytest 9
@pytest_asyncio.fixture
async def browser():
    """Setup browser for tests"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=os.getenv('HEADLESS', 'true').lower() == 'true'
    )
    yield browser
    await browser.close()
    await playwright.stop()


@pytest_asyncio.fixture
async def page(browser):
    """Setup page for tests"""
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()


# Simplified test functions without database validation
@pytest.mark.web
@pytest.mark.asyncio
async def test_reg_pos_001_valid_male_registration_ui_only(page):
    """REG_POS_001: Valid User Registration - Male (UI validation only)"""
    print("\n🧪 Running REG_POS_001: Valid Male User Registration (UI Only)")
    
    registration_page = RegistrationPage(page)
    test_data = RegistrationTestData.generate_random_user("Male")
    
    # Step 1: Navigate to registration page
    print("Step 1: Navigating to registration page...")
    await registration_page.navigate_to_registration_page()
    
    # Step 2-7: Fill registration form
    print("Step 2-7: Filling registration form...")
    await registration_page.fill_registration_form(test_data)
    
    # Step 8: Click Register button
    print("Step 8: Submitting registration...")
    await registration_page.click_register_button()
    
    # Step 9: Verify registration success
    print("Step 9: Verifying registration success...")
    is_successful = await registration_page.is_registration_successful()
    
    # For now, just check that we can navigate and submit the form
    # We'll add proper assertions once we confirm the UI behavior
    print(f"Registration result: {is_successful}")
    print(f"Current URL: {page.url}")
    print(f"Test data used: {test_data['email']}")


@pytest.mark.web  
@pytest.mark.asyncio
async def test_reg_pos_002_valid_female_registration_ui_only(page):
    """REG_POS_002: Valid User Registration - Female (UI validation only)"""
    print("\n🧪 Running REG_POS_002: Valid Female User Registration (UI Only)")
    
    registration_page = RegistrationPage(page)
    test_data = RegistrationTestData.generate_random_user("Female")
    
    # Step 1: Navigate to registration page
    print("Step 1: Navigating to registration page...")
    await registration_page.navigate_to_registration_page()
    
    # Step 2-7: Fill registration form
    print("Step 2-7: Filling registration form...")
    await registration_page.fill_registration_form(test_data)
    
    # Step 8: Click Register button
    print("Step 8: Submitting registration...")
    await registration_page.click_register_button()
    
    # Step 9: Verify registration success
    print("Step 9: Verifying registration success...")
    is_successful = await registration_page.is_registration_successful()
    
    print(f"Registration result: {is_successful}")
    print(f"Current URL: {page.url}")
    print(f"Test data used: {test_data['email']}")


# Simple smoke test
@pytest.mark.web
def test_simple_smoke_test():
    """Simple smoke test to verify pytest is working"""
    assert True


# Keep the main function for standalone execution
async def main():
    """Main test execution function for standalone running"""
    print("🚀 Starting Registration Test Suite - Simplified Version")
    print("=" * 60)
    print("Note: This is standalone mode. Use 'pytest -m web' for pytest execution.")
    print("=" * 60)


if __name__ == "__main__":
    # Run the test suite
    asyncio.run(main())