# Test Automation Framework - Project Summary

## Overview

A comprehensive, enterprise-grade **Test Automation Framework** built with Python and Playwright, featuring a Page Object Model (POM) architecture with support for **Web, API, and Salesforce automation**. The framework includes **MCP (Model Context Protocol) integration** for AI-powered test generation.

**Location**: `/Users/Shub_Bhattacharyya/Library/CloudStorage/OneDrive-EPAM/AI/Test-Automation-Framework`

## Key Features

✅ **Page Object Model (POM)** - Clean, maintainable test structure  
✅ **Web Automation** - Playwright-based cross-browser testing  
✅ **API Automation** - Comprehensive REST API testing  
✅ **Salesforce Automation** - UI and REST API automation  
✅ **MCP Server Integration** - AI-powered test generation  
✅ **Async/Await Support** - Full asynchronous operations  
✅ **Configuration Management** - Environment-based `.env` support  
✅ **Test Data Generation** - Utilities for realistic test data  
✅ **Intelligent Waits** - Smart waiting mechanisms  
✅ **Screenshot on Failure** - Automatic screenshot capture  
✅ **HTML Reports** - Detailed test reporting  
✅ **Logging & Monitoring** - Comprehensive logging system  

## Project Structure

```
Test-Automation-Framework/
├── src/                                # Source code
│   ├── __init__.py
│   ├── core/                          # Core framework
│   │   ├── base_page.py              # Base page object
│   │   ├── browser_manager.py        # Browser management
│   │   └── api_client.py             # HTTP client
│   ├── pages/                        # Web page objects
│   │   ├── login_page.py
│   │   └── home_page.py
│   ├── api/                          # API automation
│   │   └── test_base.py
│   ├── salesforce/                   # Salesforce automation
│   │   ├── auth.py
│   │   ├── api_client.py
│   │   └── base_salesforce_page.py
│   ├── utils/                        # Utilities
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   ├── wait_utils.py
│   │   ├── data_generator.py
│   │   └── assertions.py
│   └── mcp_server/                   # MCP integration
│       ├── __init__.py
│       └── server.py
│
├── tests/                            # Test files
│   ├── conftest.py                  # Pytest configuration & fixtures
│   ├── web/                         # Web tests
│   │   ├── test_login.py
│   │   └── test_home.py
│   ├── api/                         # API tests
│   │   └── test_api.py
│   └── salesforce/                  # Salesforce tests
│       └── test_salesforce.py
│
├── docs/                            # Documentation
│   ├── QUICKSTART.md               # Quick start guide
│   ├── ARCHITECTURE.md             # Architecture guide
│   ├── API_GUIDE.md                # API testing guide
│   ├── SALESFORCE_GUIDE.md         # Salesforce guide
│   └── ADVANCED_GUIDE.md           # Advanced usage
│
├── config/                          # Configuration files
├── reports/                         # Test reports (generated)
├── logs/                            # Test logs (generated)
│
├── README.md                        # Main documentation
├── CHANGELOG.md                     # Version history
├── CONTRIBUTING.md                 # Contributing guidelines
├── LICENSE                          # MIT License
├── .env.example                    # Example env file
├── .gitignore                      # Git ignore rules
├── pyproject.toml                  # Project configuration
├── requirements.txt                # Python dependencies
└── Makefile                        # Build commands

```

## Core Components

### 1. **Base Page Object** (`src/core/base_page.py`)
- Foundation for all page objects
- Common methods: navigate, click, fill_text, is_visible, etc.
- Screenshot and JavaScript execution support
- Smart wait mechanisms

### 2. **Browser Manager** (`src/core/browser_manager.py`)
- Handles browser lifecycle
- Context and page creation
- Resource cleanup
- Cross-browser support (Chromium, Firefox, WebKit)

### 3. **API Client** (`src/core/api_client.py`)
- HTTP method support (GET, POST, PUT, PATCH, DELETE)
- Authentication handling
- Response parsing and error handling
- Header management

### 4. **Salesforce Automation** (`src/salesforce/`)
- OAuth2 authentication
- REST API client with SOQL support
- UI page objects
- Metadata operations

### 5. **Utilities** (`src/utils/`)
- **Config**: Environment variable management
- **DataGenerator**: Realistic test data generation
- **WaitUtils**: Smart conditional waits
- **Assertions**: Custom assertion methods
- **LoggingConfig**: Centralized logging setup

### 6. **MCP Server** (`src/mcp_server/`)
- Integration with Model Context Protocol
- Tools for Playwright automation
- AI-powered test generation support

## Dependencies

**Core Dependencies:**
- pytest >=7.4.0
- playwright >=1.40.0
- aiohttp >=3.9.0
- pydantic >=2.0.0
- python-dotenv >=1.0.0
- pyyaml >=6.0

**Optional Dependencies:**
- allure-pytest >=2.13.0 (Test reporting)
- selenium >=4.13.0 (Legacy support)
- pyotp >=2.9.0 (2FA)

See `requirements.txt` for full list.

## Installation & Setup

### Quick Start (5 minutes)

```bash
# Clone
git clone https://github.com/subhadipbhatta/test-automation-framework.git
cd test-automation-framework

# Setup
make setup

# Run tests
pytest tests/
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install

# Configure
cp .env.example .env
# Edit .env with your settings
```

## Usage Examples

### Web Automation
```python
async def test_login(page, config):
    login = LoginPage(page, config.base_url)
    await login.navigate()
    await login.login("user", "pass")
    assert await login.is_visible(login.LOGIN_BUTTON)
```

### API Testing
```python
async def test_create_user(api_client):
    response = await api_client.post("/users", data={"name": "John"})
    assert response["status"] == 201
```

### Salesforce Automation
```python
async def test_salesforce_query():
    auth = SalesforceAuth(...)
    token = await auth.authenticate()
    api = SalesforceAPIClient(auth.instance_url, token)
    result = await api.query("SELECT Id FROM Account")
```

## Test Execution

```bash
# All tests
pytest tests/ -v

# By category
pytest -m web              # Web tests
pytest -m api              # API tests
pytest -m salesforce       # Salesforce tests
pytest -m smoke            # Smoke tests

# With coverage
pytest --cov=src --cov-report=html

# With reports
pytest --html=reports/report.html
```

## Make Commands

```bash
make help              # Show all commands
make setup             # Install & configure
make test              # Run all tests
make test-web          # Web tests only
make test-api          # API tests only
make test-salesforce   # Salesforce tests
make coverage          # Coverage report
make lint              # Run linters
make format            # Format code
make clean             # Clean generated files
```

## Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Main documentation, setup, and usage |
| **QUICKSTART.md** | Get started in 5 minutes |
| **ARCHITECTURE.md** | Framework design and patterns |
| **API_GUIDE.md** | API automation detailed guide |
| **SALESFORCE_GUIDE.md** | Salesforce automation guide |
| **ADVANCED_GUIDE.md** | Advanced usage patterns |
| **CONTRIBUTING.md** | Contributing guidelines |

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.9+** | Programming language |
| **Playwright** | Web automation |
| **Pytest** | Test framework |
| **aiohttp** | Async HTTP client |
| **Pydantic** | Configuration validation |
| **PyYAML** | Configuration files |
| **python-dotenv** | Environment management |

## Test Markers

```python
@pytest.mark.web          # Web automation tests
@pytest.mark.api          # API automation tests
@pytest.mark.salesforce   # Salesforce automation tests
@pytest.mark.smoke        # Smoke tests
@pytest.mark.regression   # Regression tests
@pytest.mark.slow         # Slow running tests
@pytest.mark.asyncio      # Async tests
```

## Configuration

### Environment Variables (.env)

```env
# Browser
BROWSER_TYPE=chromium
HEADLESS=true
BASE_URL=http://localhost:3000

# API
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30

# Salesforce
SALESFORCE_INSTANCE=https://login.salesforce.com
SALESFORCE_CLIENT_ID=your_id
SALESFORCE_CLIENT_SECRET=your_secret
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password

# Test
TEST_TIMEOUT=30000
SCREENSHOT_ON_FAILURE=true
REPORT_DIR=./reports
```

## Best Practices Implemented

1. ✅ Page Object Model for maintainability
2. ✅ Async/await for performance
3. ✅ Configuration as code
4. ✅ Comprehensive logging
5. ✅ Proper error handling
6. ✅ Smart wait mechanisms
7. ✅ Test data generation
8. ✅ Screenshot on failure
9. ✅ Type hints throughout
10. ✅ Modular architecture

## Future Enhancements

- [ ] Visual regression testing
- [ ] Performance testing integration
- [ ] Mobile testing support
- [ ] Custom report templates
- [ ] Test analytics dashboard
- [ ] Parallel execution optimization
- [ ] CI/CD examples
- [ ] Video recording on failure
- [ ] Advanced Salesforce features

## Contributing

Contributions welcome! See `CONTRIBUTING.md` for guidelines.

## License

MIT License - See `LICENSE` file

## Support

- 📖 Documentation: See `/docs` folder
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📧 Email: test@example.com

## Quick Links

- [GitHub Repository](https://github.com/subhadipbhatta/test-automation-framework)
- [Playwright Docs](https://playwright.dev)
- [Pytest Docs](https://docs.pytest.org)
- [Salesforce API Docs](https://developer.salesforce.com)

---

**Created with ❤️ for automated testing excellence**
