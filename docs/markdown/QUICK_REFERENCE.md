# Quick Reference Card

## Installation (30 seconds)

```bash
cd Test-Automation-Framework
make setup
```

## Run Tests (10 seconds)

```bash
pytest tests/              # All tests
pytest -m web             # Web only
pytest -m api             # API only
pytest -m salesforce      # Salesforce only
```

## Common Commands

```bash
make help              # Show all commands
make test              # Run all tests
make test-web          # Web tests
make coverage          # Coverage report
make lint              # Lint code
make format            # Format code
pytest -v -s           # Verbose with print
```

## Create a Test

```python
# tests/web/test_example.py
import pytest
from src.pages.login_page import LoginPage

@pytest.mark.web
@pytest.mark.asyncio
async def test_example(page, config):
    page_obj = LoginPage(page, config.base_url)
    await page_obj.navigate()
    # Add assertions
    assert await page_obj.is_visible(page_obj.USERNAME_INPUT)
```

## Create a Page Object

```python
# src/pages/my_page.py
from src.core.base_page import BasePage

class MyPage(BasePage):
    MY_ELEMENT = "selector"
    
    async def wait_for_page_load(self):
        await self.wait_for_selector(self.MY_ELEMENT)
    
    async def my_action(self):
        await self.click(self.MY_ELEMENT)
```

## API Test

```python
@pytest.mark.api
@pytest.mark.asyncio
async def test_api(api_client):
    response = await api_client.get("/endpoint")
    assert response["status"] == 200
```

## Salesforce Test

```python
@pytest.mark.salesforce
@pytest.mark.asyncio
async def test_salesforce():
    auth = SalesforceAuth(...)
    token = await auth.authenticate()
    api = SalesforceAPIClient(auth.instance_url, token)
    result = await api.query("SELECT Id FROM Account")
```

## Page Object Methods

```python
# Navigation
await page.navigate("/path")
await page.navigate()  # Uses base_url

# Interaction
await page.click("selector")
await page.fill_text("selector", "text")
await page.select_option("selector", "value")

# Wait
await page.wait_for_selector("selector")
await page.wait_for_load_state("networkidle")

# Get Info
text = await page.get_text("selector")
attr = await page.get_attribute("selector", "attr")
is_visible = await page.is_visible("selector")
is_enabled = await page.is_enabled("selector")

# Screenshots & JS
await page.take_screenshot("path.png")
result = await page.execute_script("javascript code")
```

## API Client Methods

```python
# Requests
response = await client.get("/endpoint")
response = await client.post("/endpoint", data={...})
response = await client.put("/endpoint", data={...})
response = await client.patch("/endpoint", data={...})
response = await client.delete("/endpoint")

# Auth
client.set_auth_header("token")
client.set_auth_header("token", auth_type="Basic")

# Response structure
response["status"]   # HTTP status code
response["body"]     # Parsed response body
response["headers"]  # Response headers
```

## Test Data Generation

```python
from src.utils.data_generator import DataGenerator

email = DataGenerator.generate_email()
username = DataGenerator.generate_username()
password = DataGenerator.generate_password()
user = DataGenerator.generate_user_data()
```

## Configuration

```python
from src.utils.config import Config

config = Config()
config.base_url
config.api_base_url
config.browser_type
config.headless
config.test_timeout
```

## Assertions

```python
from src.utils.assertions import Assertions

await Assertions.assert_equal(actual, expected)
await Assertions.assert_in(value, container)
await Assertions.assert_not_none(value)
await Assertions.assert_true(condition)
await Assertions.assert_greater_than(a, b)
```

## Pytest Markers

```python
@pytest.mark.web           # Web test
@pytest.mark.api           # API test
@pytest.mark.salesforce    # Salesforce test
@pytest.mark.smoke         # Smoke test
@pytest.mark.regression    # Regression test
@pytest.mark.asyncio       # Async test
@pytest.mark.slow          # Slow test
```

## Fixtures

```python
# In conftest.py
@pytest.fixture
async def page(browser_manager):
    # Setup
    page = await browser_manager.create_page(context)
    yield page
    # Teardown
    await browser_manager.close_page(page)
```

## Environment Variables

```env
BROWSER_TYPE=chromium          # Browser
HEADLESS=true                  # Headless mode
BASE_URL=http://localhost:3000 # App URL
API_BASE_URL=http://localhost:8000
SALESFORCE_INSTANCE=https://login.salesforce.com
SALESFORCE_USERNAME=username
SALESFORCE_PASSWORD=password
TEST_TIMEOUT=30000
SCREENSHOT_ON_FAILURE=true
```

## File Locations

```
Framework/
├── src/core          - Base classes
├── src/pages         - Web page objects
├── src/api           - API automation
├── src/salesforce    - Salesforce
├── src/utils         - Utilities
├── tests/            - Test files
└── docs/             - Documentation
```

## Debugging

```bash
# Run with output
pytest -v -s test.py

# Run single test
pytest tests/web/test_login.py::TestLogin::test_successful_login

# Stop on first failure
pytest -x tests/

# Show last failed
pytest --lf tests/

# With debugger
# Add: import pdb; pdb.set_trace()

# View logs
tail -f logs/test_framework.log
```

## Common Errors & Solutions

| Error | Solution |
|-------|----------|
| Playwright not installed | `playwright install` |
| .env not found | `cp .env.example .env` |
| Browser timeout | Increase `TEST_TIMEOUT` in .env |
| Salesforce auth fails | Verify credentials in .env |
| Element not found | Add explicit waits, take screenshot |

## Links

- **README**: Full documentation
- **QUICKSTART**: 5-minute setup
- **ARCHITECTURE**: Design patterns
- **API_GUIDE**: API testing
- **SALESFORCE_GUIDE**: Salesforce automation
- **ADVANCED_GUIDE**: Advanced patterns

## Tips

✓ Use `.env` for all config  
✓ Create reusable page objects  
✓ Use fixtures for setup/teardown  
✓ Mark tests appropriately  
✓ Take screenshots on failure  
✓ Log important steps  
✓ Use async/await properly  
✓ Run tests frequently  

---

**For more info, see `/docs` or run `make help`**
