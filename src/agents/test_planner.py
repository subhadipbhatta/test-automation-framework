"""
Playwright Test Planner Agent
Creates comprehensive test plans by exploring web applications
"""

import asyncio
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PlaywrightTestPlanner:
    """
    Creates comprehensive test plans for web applications.
    Based on the playwright-test-planner agent pattern.
    """
    
    def __init__(self, output_dir: str = "tests/plans"):
        """
        Initialize the test planner.
        
        Args:
            output_dir: Directory where test plans will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.explored_urls: List[str] = []
        self.discovered_elements: List[Dict] = []
        
    async def setup_page(self, browser_context, url: str):
        """
        Set up the page for exploration.
        
        Args:
            browser_context: Playwright browser context
            url: URL to explore
            
        Returns:
            Playwright page object
        """
        page = await browser_context.new_page()
        await page.goto(url)
        self.explored_urls.append(url)
        logger.info(f"Page setup complete: {url}")
        return page
    
    async def explore_page(self, page) -> Dict:
        """
        Explore a page and identify interactive elements.
        
        Args:
            page: Playwright page object
            
        Returns:
            Dictionary with page analysis
        """
        analysis = {
            'url': page.url,
            'title': await page.title(),
            'buttons': [],
            'links': [],
            'forms': [],
            'inputs': [],
            'interactive_elements': []
        }
        
        # Find buttons
        buttons = await page.locator('button, input[type="button"], input[type="submit"]').all()
        for button in buttons:
            try:
                text = await button.inner_text()
                analysis['buttons'].append({
                    'text': text,
                    'visible': await button.is_visible()
                })
            except Exception as e:
                logger.debug(f"Error reading button: {e}")
        
        # Find links
        links = await page.locator('a[href]').all()
        for link in links:
            try:
                text = await link.inner_text()
                href = await link.get_attribute('href')
                analysis['links'].append({
                    'text': text,
                    'href': href,
                    'visible': await link.is_visible()
                })
            except Exception as e:
                logger.debug(f"Error reading link: {e}")
        
        # Find forms
        forms = await page.locator('form').all()
        for i, form in enumerate(forms):
            try:
                action = await form.get_attribute('action')
                method = await form.get_attribute('method')
                analysis['forms'].append({
                    'index': i,
                    'action': action,
                    'method': method or 'GET'
                })
            except Exception as e:
                logger.debug(f"Error reading form: {e}")
        
        # Find input fields
        inputs = await page.locator('input, textarea, select').all()
        for inp in inputs:
            try:
                input_type = await inp.get_attribute('type') or 'text'
                name = await inp.get_attribute('name')
                placeholder = await inp.get_attribute('placeholder')
                analysis['inputs'].append({
                    'type': input_type,
                    'name': name,
                    'placeholder': placeholder,
                    'visible': await inp.is_visible()
                })
            except Exception as e:
                logger.debug(f"Error reading input: {e}")
        
        logger.info(f"Explored page: {analysis['url']}")
        logger.info(f"Found: {len(analysis['buttons'])} buttons, {len(analysis['links'])} links, "
                   f"{len(analysis['forms'])} forms, {len(analysis['inputs'])} inputs")
        
        self.discovered_elements.append(analysis)
        return analysis
    
    def create_test_scenarios(self, page_analysis: Dict) -> List[Dict]:
        """
        Create test scenarios based on page analysis.
        
        Args:
            page_analysis: Dictionary with page analysis
            
        Returns:
            List of test scenarios
        """
        scenarios = []
        
        # Happy path scenarios for forms
        for i, form in enumerate(page_analysis['forms']):
            scenario = {
                'suite': f"Form Submission - Form {i+1}",
                'name': 'Submit form with valid data',
                'steps': [
                    {'step': f'Navigate to {page_analysis["url"]}'},
                ],
                'expectations': []
            }
            
            # Add steps for filling inputs
            for inp in page_analysis['inputs']:
                if inp['visible']:
                    scenario['steps'].append({
                        'step': f'Fill {inp["name"] or inp["type"]} field',
                        'detail': f'Enter valid {inp["type"]} data'
                    })
            
            # Add submission step
            submit_button = next((b for b in page_analysis['buttons'] if 'submit' in b['text'].lower()), None)
            if submit_button:
                scenario['steps'].append({
                    'step': f'Click "{submit_button["text"]}" button'
                })
            
            scenario['expectations'].append('Form should submit successfully')
            scenario['expectations'].append('Success message or redirect should occur')
            
            scenarios.append(scenario)
        
        # Validation scenarios
        if page_analysis['forms']:
            scenario = {
                'suite': 'Form Validation',
                'name': 'Submit form with empty required fields',
                'steps': [
                    {'step': f'Navigate to {page_analysis["url"]}'},
                    {'step': 'Leave required fields empty'},
                    {'step': 'Click submit button'}
                ],
                'expectations': [
                    'Validation errors should be displayed',
                    'Form should not submit'
                ]
            }
            scenarios.append(scenario)
        
        # Navigation scenarios
        if page_analysis['links']:
            scenario = {
                'suite': 'Navigation Tests',
                'name': 'Navigate through application links',
                'steps': [],
                'expectations': ['Each link should navigate to valid page']
            }
            for link in page_analysis['links'][:5]:  # Limit to first 5 links
                if link['visible'] and link['href'] and not link['href'].startswith('#'):
                    scenario['steps'].append({
                        'step': f'Click "{link["text"]}" link',
                        'detail': f'Navigates to {link["href"]}'
                    })
            if scenario['steps']:
                scenarios.append(scenario)
        
        # Button interaction scenarios
        if page_analysis['buttons']:
            scenario = {
                'suite': 'Button Interactions',
                'name': 'Verify all buttons are clickable',
                'steps': [],
                'expectations': ['All buttons should be clickable and functional']
            }
            for button in page_analysis['buttons']:
                if button['visible']:
                    scenario['steps'].append({
                        'step': f'Click "{button["text"]}" button',
                        'detail': 'Verify button responds to click'
                    })
            if scenario['steps']:
                scenarios.append(scenario)
        
        return scenarios
    
    def generate_plan_markdown(
        self,
        app_name: str,
        overview: str,
        scenarios: List[Dict],
        seed_file: Optional[str] = None
    ) -> str:
        """
        Generate test plan in markdown format.
        
        Args:
            app_name: Application name
            overview: Brief overview of the application
            scenarios: List of test scenarios
            seed_file: Optional seed file reference
            
        Returns:
            Markdown formatted test plan
        """
        lines = [
            f'# Test Plan: {app_name}',
            '',
            f'**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '',
            '## Overview',
            '',
            overview,
            '',
        ]
        
        if seed_file:
            lines.extend([
                '## Seed File',
                '',
                f'`{seed_file}`',
                ''
            ])
        
        lines.extend([
            '## Test Scenarios',
            '',
        ])
        
        # Group scenarios by suite
        suites = {}
        for scenario in scenarios:
            suite = scenario['suite']
            if suite not in suites:
                suites[suite] = []
            suites[suite].append(scenario)
        
        # Generate scenarios by suite
        for suite_num, (suite_name, suite_scenarios) in enumerate(suites.items(), 1):
            lines.extend([
                f'### {suite_num}. {suite_name}',
                ''
            ])
            
            if seed_file:
                lines.extend([
                    f'**Seed:** `{seed_file}`',
                    ''
                ])
            
            for test_num, scenario in enumerate(suite_scenarios, 1):
                lines.extend([
                    f'#### {suite_num}.{test_num} {scenario["name"]}',
                    '',
                    '**Steps:**',
                    ''
                ])
                
                for step_num, step in enumerate(scenario['steps'], 1):
                    step_text = step if isinstance(step, str) else step.get('step', '')
                    lines.append(f'{step_num}. {step_text}')
                    if isinstance(step, dict) and 'detail' in step:
                        lines.append(f'   - {step["detail"]}')
                
                lines.append('')
                
                if scenario.get('expectations'):
                    lines.extend([
                        '**Expected Results:**',
                        ''
                    ])
                    for exp in scenario['expectations']:
                        lines.append(f'- {exp}')
                    lines.append('')
        
        return '\n'.join(lines)
    
    async def save_plan(
        self,
        file_name: str,
        app_name: str,
        overview: str,
        scenarios: List[Dict],
        seed_file: Optional[str] = None
    ) -> Path:
        """
        Save test plan to markdown file.
        
        Args:
            file_name: Name of the plan file
            app_name: Application name
            overview: Brief overview
            scenarios: List of test scenarios
            seed_file: Optional seed file reference
            
        Returns:
            Path to the saved plan file
        """
        # Generate markdown
        markdown = self.generate_plan_markdown(app_name, overview, scenarios, seed_file)
        
        # Ensure file has .md extension
        if not file_name.endswith('.md'):
            file_name = f"{file_name}.md"
        
        # Write to file
        file_path = self.output_dir / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(markdown)
        
        logger.info(f"Test plan saved to: {file_path}")
        return file_path
    
    async def create_plan_from_url(
        self,
        browser_context,
        url: str,
        app_name: str,
        overview: str,
        file_name: str,
        seed_file: Optional[str] = None
    ) -> Path:
        """
        Create a complete test plan by exploring a URL.
        
        Args:
            browser_context: Playwright browser context
            url: URL to explore
            app_name: Application name
            overview: Brief overview
            file_name: Output file name
            seed_file: Optional seed file reference
            
        Returns:
            Path to the saved plan file
        """
        # Set up page
        page = await self.setup_page(browser_context, url)
        
        # Explore page
        analysis = await self.explore_page(page)
        
        # Create scenarios
        scenarios = self.create_test_scenarios(analysis)
        
        # Save plan
        plan_path = await self.save_plan(
            file_name=file_name,
            app_name=app_name,
            overview=overview,
            scenarios=scenarios,
            seed_file=seed_file
        )
        
        await page.close()
        return plan_path


# Example usage
async def example_usage():
    """Example of using the test planner"""
    from playwright.async_api import async_playwright
    
    planner = PlaywrightTestPlanner(output_dir="tests/plans")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        
        # Create test plan
        plan_file = await planner.create_plan_from_url(
            browser_context=context,
            url='https://example.com/app',
            app_name='Example Application',
            overview='A web application for testing automation framework',
            file_name='example_app_test_plan.md',
            seed_file='tests/seed.spec.py'
        )
        
        print(f"Test plan created: {plan_file}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
