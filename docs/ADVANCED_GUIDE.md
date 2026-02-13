# Advanced Usage Guide

## Advanced Features

This guide covers advanced usage patterns and features of the Test Automation Framework.

## Custom Fixtures

### Creating Reusable Fixtures

```python
# tests/conftest.py
@pytest.fixture
async def logged_in_user(page, config, test_data):
    """Fixture that returns a logged-in page"""
    from src.pages.login_page import LoginPage
    
    login_page = LoginPage(page, config.base_url)
    await login_page.navigate()
    await login_page.login(
        test_data["valid_user"]["username"],
        test_data["valid_user"]["password"]
    )
    yield page

# Usage in tests
async def test_dashboard(logged_in_user):
    dashboard = DashboardPage(logged_in_user)
    assert await dashboard.is_visible(dashboard.WELCOME_MESSAGE)
```

### Parameterized Tests

```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
    ("user3", "pass3"),
])
@pytest.mark.asyncio
async def test_login_with_multiple_users(page, config, username, password):
    login_page = LoginPage(page, config.base_url)
    await login_page.navigate()
    await login_page.login(username, password)
    # Assert login successful
```

## Page Object Extensions

### Using Locators

```python
from playwright.async_api import Locator

class AdvancedPage(BasePage):
    async def get_table_rows(self) -> list[Locator]:
        """Get all rows from a table"""
        return await self.page.locator("table tbody tr").all()
    
    async def get_cell_text(self, row: int, col: int) -> str:
        """Get text from specific cell"""
        rows = await self.get_table_rows()
        row_locator = rows[row]
        cell = row_locator.locator("td").nth(col)
        return await cell.text_content() or ""
```

### Complex Interactions

```python
class ComplexPage(BasePage):
    async def drag_and_drop(self, source: str, target: str) -> None:
        """Perform drag and drop"""
        await self.page.locator(source).drag_to(
            self.page.locator(target)
        )
    
    async def upload_file(self, file_input_selector: str, file_path: str) -> None:
        """Upload file"""
        await self.page.locator(file_input_selector).set_input_files(file_path)
    
    async def hover_and_click(self, hover_selector: str, click_selector: str) -> None:
        """Hover over element then click another"""
        await self.page.locator(hover_selector).hover()
        await self.page.locator(click_selector).click()
    
    async def get_all_text_in_elements(self, selector: str) -> list[str]:
        """Get text from all matching elements"""
        elements = await self.page.locator(selector).all()
        texts = []
        for elem in elements:
            text = await elem.text_content()
            if text:
                texts.append(text.strip())
        return texts
```

## API Testing Advanced Patterns

### Custom API Client

```python
from src.core.api_client import APIClient

class CustomAPIClient(APIClient):
    async def create_resource(self, resource_type: str, data: dict):
        """Create a resource with logging"""
        self.logger.info(f"Creating {resource_type}")
        return await self.post(f"/{resource_type}", data=data)
    
    async def update_resource(self, resource_type: str, id: str, data: dict):
        """Update a resource"""
        return await self.put(f"/{resource_type}/{id}", data=data)
    
    async def list_resources(self, resource_type: str, filters: dict = None):
        """List resources with optional filters"""
        params = filters or {}
        return await self.get(f"/{resource_type}", params=params)
```

### API Request Chaining

```python
async def test_resource_workflow(api_client):
    """Test complete resource workflow"""
    
    # Create resource
    create_response = await api_client.post("/items", data={"name": "Test"})
    item_id = create_response["body"]["id"]
    
    # Update resource
    await api_client.put(f"/items/{item_id}", data={"name": "Updated"})
    
    # Get resource
    get_response = await api_client.get(f"/items/{item_id}")
    assert get_response["body"]["name"] == "Updated"
    
    # Delete resource
    await api_client.delete(f"/items/{item_id}")
```

### Mock API Responses

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mocked_api():
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={"id": 1, "name": "Test"}
        )
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Your test code here
```

## Salesforce Advanced Patterns

### Batch Operations

```python
async def create_multiple_records(api, records):
    """Create multiple records efficiently"""
    created_ids = []
    
    for record in records:
        try:
            record_id = await api.create_record("Account", record)
            created_ids.append(record_id)
        except Exception as e:
            logger.error(f"Failed to create record: {e}")
    
    return created_ids
```

### Complex SOQL Queries

```python
# Subqueries
soql = """
SELECT Id, Name, 
  (SELECT FirstName, LastName FROM Contacts),
  (SELECT Amount FROM Opportunities WHERE StageName = 'Closed Won')
FROM Account
WHERE Industry = 'Technology'
"""

result = await api.query(soql)
```

## Performance Optimization

### Parallel Test Execution

```bash
# Run tests in parallel with pytest-xdist
pytest -n auto tests/
```

### Browser Context Reuse

```python
@pytest.fixture(scope="function")
async def reusable_context(browser_manager):
    """Reuse browser context across tests"""
    context = await browser_manager.create_context()
    yield context
    await browser_manager.close_context(context)
```

### Connection Pooling

```python
class OptimizedAPIClient(APIClient):
    def __init__(self, base_url: str, connector_limit: int = 100):
        super().__init__(base_url)
        self.connector_limit = connector_limit
    
    async def __aenter__(self):
        import aiohttp
        connector = aiohttp.TCPConnector(limit=self.connector_limit)
        self.session = aiohttp.ClientSession(connector=connector)
        return self
```

## Error Handling and Retry Logic

### Retry Decorator

```python
import asyncio
from functools import wraps

def async_retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry async functions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    await asyncio.sleep(delay)
            return None
        return wrapper
    return decorator

# Usage
@async_retry(max_attempts=3, delay=1.0)
async def test_with_retry(page):
    login_page = LoginPage(page)
    await login_page.login("user", "pass")
```

### Error Screenshots

```python
from src.core.base_page import BasePage
import traceback

class ErrorHandlingPage(BasePage):
    async def safe_click(self, selector: str) -> bool:
        """Click with error handling"""
        try:
            await self.click(selector)
            return True
        except Exception as e:
            # Take screenshot on error
            await self.take_screenshot("error_click.png")
            self.logger.error(f"Click failed: {e}\n{traceback.format_exc()}")
            raise
```

## Custom Assertions

### Extended Assertions

```python
from src.utils.assertions import Assertions

class CustomAssertions(Assertions):
    @staticmethod
    async def assert_element_count(page, selector: str, expected_count: int):
        """Assert number of elements"""
        elements = await page.locator(selector).count()
        assert elements == expected_count, \
            f"Expected {expected_count} elements, found {elements}"
    
    @staticmethod
    async def assert_text_color(page, selector: str, expected_color: str):
        """Assert text color"""
        actual_color = await page.locator(selector).evaluate(
            "el => window.getComputedStyle(el).color"
        )
        assert actual_color == expected_color
```

## Data-Driven Testing

### CSV-based Data

```python
import csv

def load_test_data(csv_file: str) -> list[dict]:
    """Load test data from CSV"""
    data = []
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data

@pytest.mark.parametrize("test_data", load_test_data("test_data.csv"))
@pytest.mark.asyncio
async def test_with_csv_data(page, test_data):
    # Use test_data
    pass
```

### JSON-based Data

```python
import json

@pytest.fixture
def test_scenarios():
    """Load scenarios from JSON"""
    with open("scenarios.json") as f:
        return json.load(f)

async def test_scenarios(page, config, test_scenarios):
    for scenario in test_scenarios:
        # Execute each scenario
        pass
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install
    
    - name: Run tests
      run: pytest tests/ --cov=src
```

## Best Practices Summary

1. **DRY Principle** - Use fixtures and utilities to avoid repetition
2. **Type Hints** - Use for better IDE support and documentation
3. **Async Patterns** - Leverage async/await for performance
4. **Error Handling** - Implement proper error handling and logging
5. **Page Objects** - Keep UI logic separate from test logic
6. **Configuration** - Externalize all configuration
7. **Documentation** - Document complex test logic
8. **Maintainability** - Write tests for readability and maintenance
9. **Performance** - Use parallel execution and smart waits
10. **Monitoring** - Log and monitor test execution
