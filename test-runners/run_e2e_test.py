"""
Simple Test Runner for E2E_REG_001
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def run_registration_test():
    """Run the registration to checkout test"""
    try:
        from playwright.async_api import async_playwright
        from tests.web.TricentisWeb_E2E_REG_01 import RegistrationToCheckoutTest
        
        print("🚀 Starting E2E Registration Test...")
        
        async with async_playwright() as p:
            # Launch browser in non-headless mode to see the test execution
            browser = await p.chromium.launch(headless=False, slow_mo=1000)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Create test instance
                test_instance = RegistrationToCheckoutTest(page)
                
                print("📋 Executing test steps...")
                
                # Run the test
                result = await test_instance.test_complete_registration_to_purchase()
                
                print("\n" + "="*60)
                print("🎯 TEST EXECUTION COMPLETED")
                print("="*60)
                print(f"Test ID: {result.test_id}")
                print(f"Test Name: {result.test_name}")
                print(f"Status: {result.status}")
                print(f"Duration: {result.duration:.2f} seconds")
                print(f"Assertions Passed: {result.assertions_passed}")
                print(f"Assertions Failed: {result.assertions_failed}")
                print(f"Screenshots Taken: {len(result.screenshots)}")
                
                if result.screenshots:
                    print("\n📸 Screenshots:")
                    for i, screenshot in enumerate(result.screenshots, 1):
                        print(f"  {i}. {screenshot}")
                
                if result.errors:
                    print(f"\n❌ Errors:")
                    for error in result.errors:
                        print(f"  - {error}")
                
                if result.status == "Passed":
                    print("\n✅ TEST PASSED SUCCESSFULLY!")
                else:
                    print(f"\n❌ TEST FAILED!")
                    
                print("="*60)
                
            except Exception as e:
                print(f"\n❌ Test execution failed: {str(e)}")
                print(f"Error type: {type(e).__name__}")
                import traceback
                traceback.print_exc()
            
            finally:
                print("\n🔄 Closing browser...")
                await browser.close()
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure Playwright is installed: pip install playwright")
        print("And install browsers: playwright install")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🎭 Playwright E2E Test Runner")
    print("Testing: Demo Web Shop Registration to Purchase Journey")
    print("-" * 60)
    
    asyncio.run(run_registration_test())