# Architecture Guide

## Framework Architecture

This document describes the architecture and design patterns of the Test Automation Framework.

## Core Components

### 1. Browser Management

**File**: `src/core/browser_manager.py`

Handles browser lifecycle:
- Browser launch with configuration
- Context creation and management
- Page creation and lifecycle
- Resource cleanup

```python
async with BrowserManager() as manager:
    context = await manager.create_context()
    page = await manager.create_page(context)
    # Use page
    await manager.close_page(page)
```

### 2. Base Page Object

**File**: `src/core/base_page.py`

Provides common functionality for all page objects:
- Element interaction methods
- Navigation
- Waits and synchronization
- Screenshots
- JavaScript execution

All page objects inherit from `BasePage`.

### 3. API Client

**File**: `src/core/api_client.py`

Handles HTTP requests:
- GET, POST, PUT, PATCH, DELETE methods
- Header management
- Authentication
- Response handling
- Error handling

### 4. Configuration Management

**File**: `src/utils/config.py`

Manages application configuration:
- Environment variable loading
- Default values
- YAML configuration support
- Type conversion

## Automation Layers

### Web Automation

**Location**: `src/pages/`

Page objects for UI automation:
- `LoginPage` - Login functionality
- `HomePage` - Authenticated pages
- Custom pages inherit from `BasePage`

### API Automation

**Location**: `src/api/`

API testing utilities:
- `APIClient` - HTTP client
- `APITestBase` - Common assertions and utilities
- Response validation

### Salesforce Automation

**Location**: `src/salesforce/`

Salesforce-specific functionality:
- `SalesforceAuth` - OAuth2 authentication
- `SalesforceAPIClient` - REST API client
- `SalesforcePage` - UI page objects
- SOQL queries and metadata operations

## Utilities

### Wait Utilities

**File**: `src/utils/wait_utils.py`

Smart wait mechanisms:
- Conditional waits
- Element state waits
- Text waits
- Custom timeout and polling

### Data Generator

**File**: `src/utils/data_generator.py`

Test data generation:
- Random strings, emails, phones
- User data generation
- Date generation
- Realistic test data

## Design Patterns

### 1. Page Object Model

Each page is represented as a class:

```python
class LoginPage(BasePage):
    USERNAME_INPUT = 'input[id="username"]'
    LOGIN_BUTTON = 'button[id="login"]'
    
    async def login(self, username, password):
        await self.fill_text(self.USERNAME_INPUT, username)
        await self.click(self.LOGIN_BUTTON)
```

Benefits:
- Test code is independent of page structure
- Locators are centralized
- Easy to maintain and update
- Reusable components

### 2. Async/Await Pattern

All interactions are asynchronous:

```python
async def test_login(page):
    login_page = LoginPage(page)
    await login_page.navigate()
    await login_page.login("user", "pass")
```

Benefits:
- Non-blocking operations
- Better resource utilization
- Improved performance
- Modern Python patterns

### 3. Fixture Pattern

Pytest fixtures for setup/teardown:

```python
@pytest.fixture
async def page(browser_context, browser_manager):
    page = await browser_manager.create_page(browser_context)
    yield page
    await browser_manager.close_page(page)
```

Benefits:
- Clean test setup
- Resource management
- Reusable fixtures
- Proper cleanup

### 4. Configuration as Code

Externalized configuration:

```python
config = Config()  # Loads from .env
browser_type = config.browser_type
api_url = config.api_base_url
```

Benefits:
- Environment-specific settings
- No hardcoded values
- Easy CI/CD integration
- Sensitive data protection

## Test Execution Flow

```
pytest
    ↓
conftest.py (setup)
    ↓
Browser Launch
    ↓
Test Execution
    ├─ Navigate
    ├─ Interact
    ├─ Assert
    └─ Screenshot (on failure)
    ↓
Cleanup
    ↓
Report Generation
```

## Module Dependencies

```
Base Framework
├── core/
│   ├── base_page.py
│   ├── browser_manager.py
│   └── api_client.py
├── utils/
│   ├── config.py
│   ├── wait_utils.py
│   └── data_generator.py
│
Automation Layers
├── pages/ (depends on core)
├── api/ (depends on core)
└── salesforce/ (depends on core)
│
Tests
├── web/ (depends on pages)
├── api/ (depends on api)
└── salesforce/ (depends on salesforce)
```

## Extensibility

### Adding a New Page Object

```python
from src.core.base_page import BasePage

class MyNewPage(BasePage):
    # Define locators
    ELEMENT = "selector"
    
    async def wait_for_page_load(self):
        await self.wait_for_selector(self.ELEMENT)
    
    async def my_action(self):
        await self.click(self.ELEMENT)
```

### Adding a New API Test

```python
from src.api.test_base import APITestBase
from src.core.api_client import APIClient

class MyAPITest(APITestBase):
    async def test_my_endpoint(self):
        response = await self.api_client.get("/endpoint")
        await self.assert_status_code(response, 200)
```

### Creating Custom Utilities

```python
from src.utils.wait_utils import WaitUtils

class CustomUtils:
    @staticmethod
    async def wait_for_custom_condition():
        await WaitUtils.wait_until(
            custom_condition,
            timeout=10
        )
```

## Performance Considerations

1. **Parallel Execution**: Use pytest-xdist for parallel test runs
2. **Async Operations**: Leverage async/await for better concurrency
3. **Resource Management**: Proper cleanup in fixtures
4. **Smart Waits**: Use conditional waits instead of sleeps
5. **Browser Reuse**: Context sharing between tests

## Scalability

The framework supports:
- Multiple browser types (Chromium, Firefox, WebKit)
- Multiple environments (dev, staging, prod)
- Multiple test categories (smoke, regression, integration)
- Distributed test execution
- CI/CD pipeline integration
