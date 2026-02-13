# Quick Start Guide

## Getting Started

A quick reference guide to get up and running with the Test Automation Framework.

## 5-Minute Setup

### 1. Clone and Setup
```bash
git clone https://github.com/subhadipbhatta/test-automation-framework.git
cd test-automation-framework
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Tests
```bash
pytest tests/
```

## First Web Test

```python
# tests/web/test_example.py
import pytest
from src.pages.login_page import LoginPage

@pytest.mark.web
@pytest.mark.asyncio
async def test_login_page_loads(page, config):
    # Create page object
    login = LoginPage(page, config.base_url)
    
    # Navigate
    await login.navigate()
    
    # Wait for elements
    await login.wait_for_page_load()
    
    # Assert
    assert await login.is_visible(login.USERNAME_INPUT)
```

Run:
```bash
pytest tests/web/test_example.py
```

## First API Test

```python
# tests/api/test_example.py
import pytest
from src.core.api_client import APIClient

@pytest.mark.api
@pytest.mark.asyncio
async def test_api_health(config):
    async with APIClient(config.api_base_url) as client:
        response = await client.get("/health")
        assert response["status"] == 200
```

Run:
```bash
pytest tests/api/test_example.py
```

## First Salesforce Test

```python
# tests/salesforce/test_example.py
import pytest
from src.salesforce.api_client import SalesforceAPIClient
from src.salesforce.auth import SalesforceAuth

@pytest.mark.salesforce
@pytest.mark.asyncio
async def test_query_accounts(config):
    # Authenticate
    auth = SalesforceAuth(
        config.salesforce_instance,
        config.salesforce_client_id,
        config.salesforce_client_secret,
        config.salesforce_username,
        config.salesforce_password
    )
    token = await auth.authenticate()
    
    # Create client
    api = SalesforceAPIClient(auth.instance_url, token)
    
    # Query
    result = await api.query("SELECT Id FROM Account LIMIT 1")
    assert "records" in result
```

Run:
```bash
pytest tests/salesforce/test_example.py
```

## Common Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/web/test_login.py

# Run specific test
pytest tests/web/test_login.py::TestLogin::test_successful_login

# Run by marker
pytest -m web           # Web tests only
pytest -m api           # API tests only
pytest -m salesforce    # Salesforce tests only
pytest -m smoke         # Smoke tests only

# Run with options
pytest -v              # Verbose
pytest -s              # Show print statements
pytest -x              # Stop on first failure
pytest -k "login"      # Filter by test name
pytest --tb=short      # Short traceback
pytest --html=report.html  # HTML report

# Run with coverage
pytest --cov=src --cov-report=html
```

## Creating a Page Object

```python
# src/pages/my_page.py
from src.core.base_page import BasePage

class MyPage(BasePage):
    # Locators
    TITLE = "h1"
    BUTTON = "button[id='submit']"
    
    async def wait_for_page_load(self):
        await self.wait_for_selector(self.TITLE)
    
    async def click_submit(self):
        await self.click(self.BUTTON)
```

## Creating a Test

```python
# tests/web/test_my_page.py
import pytest
from src.pages.my_page import MyPage

@pytest.mark.web
@pytest.mark.asyncio
async def test_my_page(page, config):
    my_page = MyPage(page, config.base_url)
    await my_page.navigate()
    await my_page.wait_for_page_load()
    await my_page.click_submit()
```

## Debugging

### Take Screenshots
```python
await page_obj.take_screenshot("path/to/screenshot.png")
```

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Run Single Test with Output
```bash
pytest tests/web/test_login.py::TestLogin::test_successful_login -v -s
```

### Use pdb Debugger
```python
import pdb; pdb.set_trace()
```

## Next Steps

1. Read [README.md](../README.md) for full documentation
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) for design patterns
3. Review [API_GUIDE.md](API_GUIDE.md) for API testing
4. See [SALESFORCE_GUIDE.md](SALESFORCE_GUIDE.md) for Salesforce automation

## Tips

- Use `.env` for all configuration
- Create reusable page objects
- Use pytest fixtures for setup/teardown
- Use markers to organize tests
- Take screenshots on failure
- Use logging for debugging
- Run tests frequently during development
- Use async/await properly

## Resources

- [Playwright Documentation](https://playwright.dev)
- [Pytest Documentation](https://docs.pytest.org)
- [Python Asyncio](https://docs.python.org/3/library/asyncio.html)
- [Salesforce API Documentation](https://developer.salesforce.com)
