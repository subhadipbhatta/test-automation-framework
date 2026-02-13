# Test Automation Framework

A comprehensive, enterprise-grade test automation framework built with Python, Playwright, and MCP support. This framework implements the Page Object Model pattern and supports web, API, and Salesforce automation.

## Features

- **Page Object Model (POM)** - Clean, maintainable test structure
- **Web Automation** - Using Playwright for cross-browser testing
- **API Automation** - Comprehensive REST API testing capabilities
- **Salesforce Automation** - Dedicated support for Salesforce UI and API automation
- **MCP Integration** - Model Context Protocol server for AI-powered test generation
- **Async/Await Support** - Fully asynchronous framework for better performance
- **Configuration Management** - Environment-based configuration with `.env` support
- **Test Data Generation** - Utilities for generating realistic test data
- **Screenshots on Failure** - Automatic screenshot capture on test failures
- **Wait Utilities** - Smart waits with configurable polling
- **HTML Reports** - Detailed test reports with Allure integration

## Project Structure

```
Test-Automation-Framework/
├── src/                          # Source code
│   ├── core/                    # Core framework classes
│   │   ├── base_page.py        # Base page object class
│   │   ├── browser_manager.py  # Browser lifecycle management
│   │   └── api_client.py       # Base API client
│   ├── pages/                   # Web page objects
│   │   ├── login_page.py       # Login page object
│   │   └── home_page.py        # Home page object
│   ├── api/                     # API automation
│   │   └── test_base.py        # Base API test class
│   ├── salesforce/              # Salesforce automation
│   │   ├── auth.py             # Salesforce OAuth2
│   │   ├── api_client.py       # Salesforce API client
│   │   └── base_salesforce_page.py  # Salesforce page objects
│   ├── utils/                   # Utilities
│   │   ├── config.py           # Configuration management
│   │   ├── wait_utils.py       # Wait utilities
│   │   └── data_generator.py   # Test data generation
│   └── mcp_server/              # MCP server
│       ├── __init__.py         # MCP server implementation
│       └── server.py           # Server entry point
├── tests/                        # Test files
│   ├── web/                     # Web automation tests
│   │   ├── test_login.py
│   │   └── test_home.py
│   ├── api/                     # API automation tests
│   │   └── test_api.py
│   ├── salesforce/              # Salesforce tests
│   │   └── test_salesforce.py
│   └── conftest.py             # Pytest fixtures and configuration
├── config/                       # Configuration files
├── reports/                      # Test reports (generated)
├── docs/                         # Documentation
├── pyproject.toml               # Project configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment file
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.9+
- pip or poetry
- Git

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/subhadipbhatta/test-automation-framework.git
cd test-automation-framework
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**

```bash
playwright install
```

5. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Browser Settings
BROWSER_TYPE=chromium          # chromium, firefox, webkit
HEADLESS=true                  # true or false
BASE_URL=http://localhost:3000

# API Settings
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30

# Salesforce Settings
SALESFORCE_INSTANCE=https://login.salesforce.com
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password

# Test Settings
TEST_TIMEOUT=30000
SCREENSHOT_ON_FAILURE=true
REPORT_DIR=./reports

# Playwright Settings
PLAYWRIGHT_SLOW_MO=0
PLAYWRIGHT_VIEWPORT_WIDTH=1280
PLAYWRIGHT_VIEWPORT_HEIGHT=720
```

## Usage

### Running Tests

#### Run all tests
```bash
pytest
```

#### Run web tests only
```bash
pytest tests/web -m web
```

#### Run API tests only
```bash
pytest tests/api -m api
```

#### Run Salesforce tests only
```bash
pytest tests/salesforce -m salesforce
```

#### Run with HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

#### Run with coverage
```bash
pytest --cov=src --cov-report=html
```

#### Run in verbose mode
```bash
pytest -v
```

#### Run specific test file
```bash
pytest tests/web/test_login.py
```

#### Run specific test
```bash
pytest tests/web/test_login.py::TestLogin::test_successful_login
```

### Web Automation Example

```python
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage

async def test_login(page, config):
    # Initialize page object
    login_page = LoginPage(page, config.base_url)
    
    # Navigate
    await login_page.navigate()
    
    # Wait for page load
    await login_page.wait_for_page_load()
    
    # Perform login
    await login_page.login("username", "password")
    
    # Verify
    home_page = HomePage(page, config.base_url)
    assert await home_page.is_logged_in()
```

### API Automation Example

```python
from src.core.api_client import APIClient
from src.api.test_base import APITestBase

async def test_create_user(api_client):
    # Create API client
    test_base = APITestBase(api_client)
    
    # Make request
    response = await api_client.post(
        "/users",
        data={"name": "John", "email": "john@example.com"}
    )
    
    # Assert
    await test_base.assert_status_code(response, 201)
    await test_base.assert_response_contains(response, "id")
```

### Salesforce Automation Example

```python
from src.salesforce.auth import SalesforceAuth
from src.salesforce.api_client import SalesforceAPIClient

async def test_salesforce_query():
    # Authenticate
    auth = SalesforceAuth(
        instance="https://login.salesforce.com",
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password"
    )
    
    token = await auth.authenticate()
    
    # Create API client
    api = SalesforceAPIClient(auth.instance_url, token)
    
    # Query
    result = await api.query("SELECT Id, Name FROM Account LIMIT 10")
    
    # Get metadata
    metadata = await api.get_metadata("Account")
```

### Using Test Data Generator

```python
from src.utils.data_generator import DataGenerator

# Generate random data
email = DataGenerator.generate_email()
username = DataGenerator.generate_username()
password = DataGenerator.generate_password()

# Generate complete user data
user_data = DataGenerator.generate_user_data()
```

### Using Wait Utilities

```python
from src.utils.wait_utils import WaitUtils

# Wait for condition
await WaitUtils.wait_until(
    condition=async_callable,
    timeout=10,
    message="Condition not met"
)

# Wait for element state
await WaitUtils.wait_for_element_state(
    element_locator=element,
    state="visible",
    timeout=5
)

# Wait for text
await WaitUtils.wait_for_text(
    element_locator=element,
    text="Expected text",
    timeout=5
)
```

## Page Object Model Pattern

### Creating a Page Object

```python
from src.core.base_page import BasePage
from playwright.async_api import Page

class MyPage(BasePage):
    """My custom page object"""
    
    # Define locators as class attributes
    TITLE = "h1.title"
    BUTTON = "button[id='submit']"
    INPUT = "input[name='search']"
    
    async def wait_for_page_load(self) -> None:
        """Wait for page-specific elements"""
        await self.wait_for_selector(self.TITLE)
    
    async def click_button(self) -> None:
        """Custom action method"""
        await self.click(self.BUTTON)
    
    async def search(self, query: str) -> None:
        """Custom search action"""
        await self.fill_text(self.INPUT, query)
```

## Best Practices

1. **Use Page Objects** - Keep test logic separated from page interactions
2. **Async/Await** - Use async patterns for better performance
3. **Explicit Waits** - Use waits instead of sleeps
4. **Data Generators** - Use for realistic test data
5. **Configuration** - Externalize configuration to `.env`
6. **Logging** - Use logging for debugging
7. **Screenshots** - Enable on failure for debugging
8. **Fixtures** - Use pytest fixtures for setup/teardown
9. **Markers** - Use markers to categorize tests
10. **Comments** - Document complex test logic

## MCP Server Integration

The framework includes an MCP server for AI-powered test automation:

```python
from src.mcp_server import PlaywrightMCPServer

server = PlaywrightMCPServer()
tools = server.get_tools()
```

Available tools:
- navigate - Navigate to URL
- click - Click elements
- fill - Fill input fields
- get_text - Extract text
- wait_for_selector - Wait for elements
- take_screenshot - Capture screenshots
- execute_script - Run JavaScript
- select_option - Select dropdown options

## Troubleshooting

### Browser Installation Issues

```bash
# Install browser dependencies
playwright install-deps
```

### Timeout Issues

Increase timeout in `.env`:
```env
TEST_TIMEOUT=60000
```

### Credential Issues

Verify `.env` file has correct credentials and is not in version control.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/subhadipbhatta/test-automation-framework/issues
- Documentation: https://github.com/subhadipbhatta/test-automation-framework/docs

## Roadmap

- [ ] Visual regression testing
- [ ] Performance testing integration
- [ ] Mobile testing support
- [ ] Custom report templates
- [ ] Test result analytics
- [ ] Parallel execution optimization
