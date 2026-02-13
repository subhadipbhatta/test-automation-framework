"""
Playwright Test Generator Agent
Converts test plans into executable Python Playwright tests
"""

import asyncio
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class PlaywrightTestGenerator:
    """
    Generates Python Playwright tests from test plan specifications.
    Based on the playwright-test-generator agent pattern.
    """
    
    def __init__(self, output_dir: str = "tests/generated"):
        """
        Initialize the test generator.
        
        Args:
            output_dir: Directory where generated tests will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.test_log: List[Dict] = []
        
    async def setup_page(self, browser_context, url: str):
        """
        Set up the page for test scenario recording.
        
        Args:
            browser_context: Playwright browser context
            url: URL to navigate to
            
        Returns:
            Playwright page object
        """
        page = await browser_context.new_page()
        await page.goto(url)
        logger.info(f"Page setup complete: {url}")
        return page
    
    def log_action(self, action: str, selector: str = None, value: str = None, intent: str = None):
        """
        Log a test action for code generation.
        
        Args:
            action: Action type (click, fill, navigate, etc.)
            selector: Element selector
            value: Value for fill actions
            intent: Human-readable description of the step
        """
        self.test_log.append({
            'action': action,
            'selector': selector,
            'value': value,
            'intent': intent
        })
        logger.debug(f"Logged action: {action} on {selector}")
    
    def generate_test_code(
        self,
        test_suite: str,
        test_name: str,
        test_steps: List[Dict],
        seed_file: Optional[str] = None
    ) -> str:
        """
        Generate Python test code from recorded steps.
        
        Args:
            test_suite: Test suite/describe block name
            test_name: Test case name
            test_steps: List of test steps with actions and expectations
            seed_file: Optional seed file reference
            
        Returns:
            Generated Python test code
        """
        code_lines = [
            '"""',
            f'Generated test: {test_name}',
            f'Suite: {test_suite}',
        ]
        
        if seed_file:
            code_lines.append(f'Seed: {seed_file}')
        
        code_lines.extend([
            '"""',
            '',
            'import pytest',
            'from playwright.async_api import Page, expect',
            '',
            '',
            f'class Test{self._sanitize_class_name(test_suite)}:',
            f'    """Test suite for {test_suite}"""',
            '',
            '    @pytest.mark.asyncio',
            '    @pytest.mark.web',
            f'    async def test_{self._sanitize_method_name(test_name)}(self, page: Page):',
            f'        """',
            f'        Test: {test_name}',
            f'        """',
        ])
        
        # Generate test steps
        for step in test_steps:
            # Add comment for step description
            if step.get('intent'):
                code_lines.append(f'        # {step["intent"]}')
            
            # Generate code based on action type
            action = step.get('action')
            selector = step.get('selector')
            value = step.get('value')
            
            if action == 'navigate':
                code_lines.append(f'        await page.goto("{value}")')
            elif action == 'click':
                code_lines.append(f'        await page.click("{selector}")')
            elif action == 'fill':
                code_lines.append(f'        await page.fill("{selector}", "{value}")')
            elif action == 'type':
                code_lines.append(f'        await page.type("{selector}", "{value}")')
            elif action == 'select':
                code_lines.append(f'        await page.select_option("{selector}", "{value}")')
            elif action == 'wait_for_selector':
                code_lines.append(f'        await page.wait_for_selector("{selector}")')
            elif action == 'verify_visible':
                code_lines.append(f'        await expect(page.locator("{selector}")).to_be_visible()')
            elif action == 'verify_text':
                code_lines.append(f'        await expect(page.locator("{selector}")).to_have_text("{value}")')
            elif action == 'verify_value':
                code_lines.append(f'        await expect(page.locator("{selector}")).to_have_value("{value}")')
            elif action == 'take_screenshot':
                code_lines.append(f'        await page.screenshot(path="{value}")')
            elif action == 'evaluate':
                code_lines.append(f'        await page.evaluate("{value}")')
            
            code_lines.append('')
        
        return '\n'.join(code_lines)
    
    def _sanitize_class_name(self, name: str) -> str:
        """Convert test suite name to valid Python class name"""
        # Remove special characters and convert to PascalCase
        words = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in name).split()
        return ''.join(word.capitalize() for word in words)
    
    def _sanitize_method_name(self, name: str) -> str:
        """Convert test name to valid Python method name"""
        # Remove special characters and convert to snake_case
        name = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in name).lower()
        return '_'.join(name.split())
    
    async def write_test(
        self,
        file_name: str,
        test_suite: str,
        test_name: str,
        test_steps: List[Dict],
        seed_file: Optional[str] = None
    ) -> Path:
        """
        Generate and write test to file.
        
        Args:
            file_name: Name of the test file (without extension)
            test_suite: Test suite name
            test_name: Test case name
            test_steps: List of test steps
            seed_file: Optional seed file reference
            
        Returns:
            Path to the generated test file
        """
        # Generate code
        code = self.generate_test_code(test_suite, test_name, test_steps, seed_file)
        
        # Ensure file has .py extension
        if not file_name.endswith('.py'):
            file_name = f"{file_name}.py"
        
        # Write to file
        file_path = self.output_dir / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(code)
        
        logger.info(f"Test written to: {file_path}")
        return file_path
    
    def read_log(self) -> List[Dict]:
        """
        Read the current test log.
        
        Returns:
            List of logged test actions
        """
        return self.test_log.copy()
    
    def clear_log(self):
        """Clear the test log"""
        self.test_log.clear()
    
    async def generate_from_plan(
        self,
        plan_file: str,
        browser_context,
        base_url: str
    ) -> List[Path]:
        """
        Generate tests from a test plan markdown file.
        
        Args:
            plan_file: Path to test plan markdown file
            browser_context: Playwright browser context
            base_url: Base URL for the application
            
        Returns:
            List of generated test file paths
        """
        generated_files = []
        
        # Parse test plan (simplified - would need proper markdown parser)
        with open(plan_file, 'r') as f:
            plan_content = f.read()
        
        # This is a simplified parser - in production, use proper markdown parsing
        logger.info(f"Processing test plan: {plan_file}")
        
        # Set up page
        page = await self.setup_page(browser_context, base_url)
        
        # Parse and generate tests
        # This would involve parsing the markdown structure and extracting:
        # - Test suites (describe blocks)
        # - Test cases (test blocks)
        # - Steps and expectations
        # Then calling write_test() for each test case
        
        logger.info(f"Generated {len(generated_files)} test files")
        
        await page.close()
        return generated_files


# Example usage
async def example_usage():
    """Example of using the test generator"""
    from playwright.async_api import async_playwright
    
    generator = PlaywrightTestGenerator(output_dir="tests/generated")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        
        # Define test steps
        test_steps = [
            {
                'action': 'navigate',
                'value': 'https://example.com/login',
                'intent': 'Navigate to login page'
            },
            {
                'action': 'fill',
                'selector': '#username',
                'value': 'testuser',
                'intent': 'Enter username'
            },
            {
                'action': 'fill',
                'selector': '#password',
                'value': 'password123',
                'intent': 'Enter password'
            },
            {
                'action': 'click',
                'selector': 'button[type="submit"]',
                'intent': 'Click login button'
            },
            {
                'action': 'verify_visible',
                'selector': '.dashboard',
                'intent': 'Verify dashboard is visible'
            }
        ]
        
        # Generate test
        test_file = await generator.write_test(
            file_name='test_login_flow.py',
            test_suite='Login Tests',
            test_name='successful login with valid credentials',
            test_steps=test_steps
        )
        
        print(f"Generated test: {test_file}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
