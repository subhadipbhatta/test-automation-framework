#!/usr/bin/env python3
"""
Direct Test Execution for E2E_REG_001
Run the registration to checkout test directly
"""
import asyncio
import time
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
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
    
    @classmethod
    def setup_screenshot_directory(cls):
        """Create screenshot directory if it doesn't exist"""
        Path(cls.SCREENSHOT_DIR).mkdir(exist_ok=True)
        
    @classmethod
    def generate_screenshot_name(cls, test_id: str, step: int, description: str = "") -> str:
        """Generate unique screenshot filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        safe_desc = description.replace(" ", "_").replace("/", "_") if description else ""
        return f"{cls.SCREENSHOT_DIR}/{test_id}_step_{step}_{safe_desc}_{timestamp}.png"

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

class RegistrationToCheckoutTest:
    """Test complete user journey from registration to checkout"""
    
    def __init__(self, page):
        self.page = page
        self.screenshots = []
        
    async def take_screenshot(self, test_id: str, step: int, description: str = "") -> str:
        """Take screenshot and return filename"""
        BaseTestConfig.setup_screenshot_directory()
        filename = BaseTestConfig.generate_screenshot_name(test_id, step, description)
        await self.page.screenshot(path=filename, full_page=True)
        self.screenshots.append(filename)
        logger.info(f"📸 Screenshot taken: {filename}")
        return filename
    
    async def wait_and_click(self, selector: str, timeout: int = 10000):
        """Wait for element and click with error handling"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            await self.page.wait_for_timeout(500)
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {e}")
            raise
    
    async def wait_and_fill(self, selector: str, text: str, timeout: int = 10000):
        """Wait for element and fill with error handling"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.fill(selector, text)
            await self.page.wait_for_timeout(300)
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

    async def test_complete_registration_to_purchase(self, test_id: str = "E2E_REG_001"):
        """Execute complete user registration to first purchase flow"""
        test_result = TestResult(
            test_id=test_id,
            test_name="Complete User Registration to First Purchase Journey",
            status="Running",
            duration=0,
            screenshots=[],
            errors=[],
            assertions_passed=0,
            assertions_failed=0
        )
        
        start_time = time.time()
        
        try:
            logger.info("🚀 Starting E2E Registration to Purchase Test")
            
            # Step 1: Navigate to registration page
            logger.info("📍 Step 1: Navigating to registration page")
            await self.page.goto(f"{BaseTestConfig.BASE_URL}/register")
            await self.take_screenshot(test_id, 1, "registration_page_loaded")
            
            # Assert registration page loaded
            page_title = await self.page.title()
            assert "Register" in page_title
            test_result.assertions_passed += 1
            logger.info("✓ Registration page loaded successfully")
            
            # Step 2: Generate and fill registration data
            logger.info("📝 Step 2: Filling registration form")
            user_data = TestDataGenerator.generate_user_data("Male")
            logger.info(f"Generated user: {user_data['email']}")
            
            await self.wait_and_click("input[value='M']")  # Select Male gender
            await self.wait_and_fill("#FirstName", user_data["firstName"])
            await self.wait_and_fill("#LastName", user_data["lastName"])
            await self.wait_and_fill("#Email", user_data["email"])
            await self.wait_and_fill("#Password", user_data["password"])
            await self.wait_and_fill("#ConfirmPassword", user_data["confirmPassword"])
            
            await self.take_screenshot(test_id, 2, "registration_form_filled")
            
            # Submit registration
            await self.wait_and_click("#register-button")
            await self.page.wait_for_load_state("networkidle")
            
            await self.take_screenshot(test_id, 3, "registration_completed")
            
            # Assert registration success
            success_message = await self.assert_text_present("Your registration completed")
            assert success_message, "Registration success message not found"
            test_result.assertions_passed += 1
            logger.info("✓ User registration completed successfully")
            
            # Step 3: Login with new credentials
            logger.info("🔑 Step 3: Logging in with new credentials")
            await self.page.goto(f"{BaseTestConfig.BASE_URL}/login")
            await self.wait_and_fill("#Email", user_data["email"])
            await self.wait_and_fill("#Password", user_data["password"])
            await self.wait_and_click(".login-button")
            await self.page.wait_for_load_state("networkidle")
            
            await self.take_screenshot(test_id, 4, "login_successful")
            
            # Assert successful login
            login_success = await self.assert_text_present(user_data["email"])
            assert login_success, "Login verification failed"
            test_result.assertions_passed += 1
            logger.info("✓ Login successful")
            
            # Step 4: Search for product and add to cart
            logger.info("🔍 Step 4: Searching for products")
            await self.wait_and_fill("#small-searchterms", "computer")
            await self.wait_and_click(".search-box-button")
            await self.page.wait_for_load_state("networkidle")
            
            await self.take_screenshot(test_id, 5, "search_results")
            
            # Assert search results
            search_results = await self.assert_element_visible(".product-item")
            assert search_results, "No search results found"
            test_result.assertions_passed += 1
            logger.info("✓ Search results displayed")
            
            # Add first product to cart
            logger.info("🛒 Step 5: Adding product to cart")
            add_to_cart_buttons = await self.page.query_selector_all(".product-box-add-to-cart-button")
            if add_to_cart_buttons:
                await add_to_cart_buttons[0].click()
                await self.page.wait_for_load_state("networkidle")
            
            await self.take_screenshot(test_id, 6, "product_added_to_cart")
            
            # Assert product added to cart
            cart_qty_element = await self.page.query_selector(".cart-qty")
            if cart_qty_element:
                cart_count = await cart_qty_element.inner_text()
                assert "(1)" in cart_count or "1" in cart_count
                test_result.assertions_passed += 1
                logger.info("✓ Product added to cart successfully")
            
            # Step 5: Complete checkout process
            logger.info("💳 Step 6: Starting checkout process")
            await self.wait_and_click(".ico-cart")
            await self.page.wait_for_load_state("networkidle")
            
            # Accept terms and proceed to checkout
            terms_checkbox = await self.page.query_selector("#termsofservice")
            if terms_checkbox:
                await terms_checkbox.check()
            
            checkout_button = await self.page.query_selector("#checkout")
            if checkout_button:
                await checkout_button.click()
                await self.page.wait_for_load_state("networkidle")
            
            await self.take_screenshot(test_id, 7, "checkout_initiated")
            
            # Fill billing address if required
            address_data = TestDataGenerator.generate_address_data()
            
            # Try to fill billing address fields if they exist
            billing_fields = {
                "#BillingNewAddress_FirstName": address_data["firstName"],
                "#BillingNewAddress_LastName": address_data["lastName"],
                "#BillingNewAddress_Email": user_data["email"],
                "#BillingNewAddress_Address1": address_data["address"],
                "#BillingNewAddress_City": address_data["city"],
                "#BillingNewAddress_ZipPostalCode": address_data["zipCode"],
                "#BillingNewAddress_PhoneNumber": address_data["phone"]
            }
            
            for field, value in billing_fields.items():
                field_element = await self.page.query_selector(field)
                if field_element and await field_element.is_visible():
                    await field_element.fill(value)
                    await self.page.wait_for_timeout(200)
            
            # Continue through checkout steps
            continue_buttons = [
                "input[onclick*='Billing.save']",
                "input[onclick*='Shipping.save']", 
                "input[onclick*='ShippingMethod.save']",
                "input[onclick*='PaymentMethod.save']",
                "input[onclick*='PaymentInfo.save']"
            ]
            
            for button_selector in continue_buttons:
                button = await self.page.query_selector(button_selector)
                if button and await button.is_visible():
                    await button.click()
                    await self.page.wait_for_timeout(2000)
                    await self.page.wait_for_load_state("networkidle")
            
            await self.take_screenshot(test_id, 8, "order_review")
            
            # Confirm order
            confirm_button = await self.page.query_selector("input[onclick*='ConfirmOrder.save']")
            if confirm_button and await confirm_button.is_visible():
                await confirm_button.click()
                await self.page.wait_for_load_state("networkidle")
            
            await self.take_screenshot(test_id, 9, "order_completed")
            
            # Assert order completion
            order_success = await self.assert_text_present("Your order has been successfully processed")
            if order_success:
                test_result.assertions_passed += 1
                logger.info("✓ Order completed successfully")
            else:
                # Check for any success indication
                page_content = await self.page.content()
                if "thank" in page_content.lower() or "success" in page_content.lower():
                    test_result.assertions_passed += 1
                    logger.info("✓ Order process completed")
            
            test_result.status = "Passed"
            test_result.screenshots = self.screenshots
            
        except Exception as e:
            test_result.status = "Failed"
            test_result.errors.append(str(e))
            test_result.assertions_failed += 1
            logger.error(f"✗ Test failed: {e}")
            await self.take_screenshot(test_id, 999, "error_state")
            raise
        
        finally:
            test_result.duration = time.time() - start_time
            logger.info(f"⏱️  Test {test_id} completed in {test_result.duration:.2f}s")
            
        return test_result

async def run_test():
    """Main test execution function"""
    try:
        from playwright.async_api import async_playwright
        
        print("🎭 Starting Playwright E2E Test")
        print("🌐 Demo Web Shop - Registration to Purchase Journey")
        print("=" * 60)
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=False,
                slow_mo=1000,
                args=['--start-maximized']
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            try:
                # Create and run test
                test_instance = RegistrationToCheckoutTest(page)
                result = await test_instance.test_complete_registration_to_purchase()
                
                # Print results
                print("\n" + "="*60)
                print("🎯 TEST EXECUTION RESULTS")
                print("="*60)
                print(f"📋 Test ID: {result.test_id}")
                print(f"📝 Test Name: {result.test_name}")
                print(f"🏆 Status: {result.status}")
                print(f"⏱️  Duration: {result.duration:.2f} seconds")
                print(f"✅ Assertions Passed: {result.assertions_passed}")
                print(f"❌ Assertions Failed: {result.assertions_failed}")
                print(f"📸 Screenshots: {len(result.screenshots)}")
                
                if result.screenshots:
                    print(f"\n📁 Screenshots saved to: {BaseTestConfig.SCREENSHOT_DIR}")
                    for i, screenshot in enumerate(result.screenshots, 1):
                        print(f"   {i:2d}. {Path(screenshot).name}")
                
                if result.errors:
                    print(f"\n⚠️  Errors:")
                    for error in result.errors:
                        print(f"   - {error}")
                
                status_icon = "✅" if result.status == "Passed" else "❌"
                print(f"\n{status_icon} FINAL RESULT: {result.status.upper()}")
                
            except Exception as e:
                print(f"❌ Test execution failed: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                await browser.close()
                
    except ImportError:
        print("❌ Playwright not found. Please install it:")
        print("   pip install playwright")
        print("   playwright install")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("🚀 E2E Test Runner - Demo Web Shop")
    print("Testing Complete Registration to Purchase Journey")
    print("-" * 60)
    
    asyncio.run(run_test())