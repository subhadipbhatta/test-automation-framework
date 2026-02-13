# Framework File Structure Index

## Overview

Complete index of all framework files and their purposes.

## Root Configuration Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation with setup and usage |
| `PROJECT_SUMMARY.md` | Complete project overview and features |
| `CHANGELOG.md` | Version history and changes |
| `CONTRIBUTING.md` | Contributing guidelines |
| `LICENSE` | MIT License |
| `.env.example` | Example environment configuration |
| `.gitignore` | Git ignore patterns |
| `pyproject.toml` | Project metadata and dependencies |
| `requirements.txt` | Python package dependencies |
| `Makefile` | Build and test automation commands |

## Documentation Files (`/docs`)

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | 5-minute setup guide |
| `ARCHITECTURE.md` | Framework design and patterns |
| `API_GUIDE.md` | API automation detailed guide |
| `SALESFORCE_GUIDE.md` | Salesforce automation guide |
| `ADVANCED_GUIDE.md` | Advanced usage patterns and features |

## Source Code Structure (`/src`)

### Core Framework (`/src/core`)

| File | Purpose |
|------|---------|
| `__init__.py` | Core module initialization |
| `base_page.py` | Base Page Object class with common methods |
| `browser_manager.py` | Browser lifecycle and context management |
| `api_client.py` | HTTP client for REST API testing |

### Utilities (`/src/utils`)

| File | Purpose |
|------|---------|
| `__init__.py` | Utils module initialization |
| `config.py` | Environment and YAML configuration management |
| `logging_config.py` | Centralized logging setup |
| `wait_utils.py` | Smart wait mechanisms |
| `data_generator.py` | Test data generation utilities |
| `assertions.py` | Custom assertion methods |

### Web Automation (`/src/pages`)

| File | Purpose |
|------|---------|
| `__init__.py` | Pages module initialization |
| `login_page.py` | Login page object example |
| `home_page.py` | Home page object example |

### API Automation (`/src/api)

| File | Purpose |
|------|---------|
| `__init__.py` | API module initialization |
| `test_base.py` | Base API test class with assertions |

### Salesforce Automation (`/src/salesforce`)

| File | Purpose |
|------|---------|
| `__init__.py` | Salesforce module initialization |
| `auth.py` | OAuth2 authentication handler |
| `api_client.py` | Salesforce REST API client |
| `base_salesforce_page.py` | Salesforce page object base class |

### MCP Server Integration (`/src/mcp_server`)

| File | Purpose |
|------|---------|
| `__init__.py` | MCP server implementation |
| `server.py` | MCP server entry point |

## Test Files (`/tests`)

### Configuration

| File | Purpose |
|------|---------|
| `conftest.py` | Pytest configuration and fixtures |

### Web Tests (`/tests/web`)

| File | Purpose |
|------|---------|
| `__init__.py` | Web tests module initialization |
| `test_login.py` | Login functionality tests |
| `test_home.py` | Home page functionality tests |

### API Tests (`/tests/api`)

| File | Purpose |
|------|---------|
| `__init__.py` | API tests module initialization |
| `test_api.py` | REST API endpoint tests |

### Salesforce Tests (`/tests/salesforce`)

| File | Purpose |
|------|---------|
| `__init__.py` | Salesforce tests module initialization |
| `test_salesforce.py` | Salesforce automation tests |

## Additional Directories

| Directory | Purpose |
|-----------|---------|
| `/config` | Configuration files (empty, ready for use) |
| `/reports` | Generated test reports |
| `/logs` | Generated test logs |

## File Count Summary

- **Python Files**: 31
- **Documentation Files**: 8
- **Configuration Files**: 5
- **Total**: 44+ files

## Quick File Lookup

### By Function

**If you want to...**

- Test web applications → See `/tests/web` and `/src/pages`
- Test APIs → See `/tests/api` and `/src/api`
- Test Salesforce → See `/tests/salesforce` and `/src/salesforce`
- Configure the framework → See `/src/utils/config.py` and `.env.example`
- Generate test data → See `/src/utils/data_generator.py`
- Add waits/synchronization → See `/src/utils/wait_utils.py`
- Create custom assertions → See `/src/utils/assertions.py`
- Understand architecture → See `/docs/ARCHITECTURE.md`
- Get started quickly → See `/docs/QUICKSTART.md`
- Use MCP integration → See `/src/mcp_server`

### By Technology

**Playwright Web Automation**
- `/src/core/base_page.py` - Base page object
- `/src/core/browser_manager.py` - Browser management
- `/src/pages/*` - Page objects
- `/tests/web/*` - Web tests

**REST API Testing**
- `/src/core/api_client.py` - HTTP client
- `/src/api/test_base.py` - API test base
- `/tests/api/*` - API tests

**Salesforce Automation**
- `/src/salesforce/auth.py` - OAuth2
- `/src/salesforce/api_client.py` - API client
- `/src/salesforce/base_salesforce_page.py` - UI objects
- `/tests/salesforce/*` - Salesforce tests

**Configuration & Utilities**
- `/src/utils/config.py` - Configuration
- `/src/utils/wait_utils.py` - Waits
- `/src/utils/data_generator.py` - Data generation
- `/src/utils/assertions.py` - Assertions
- `/src/utils/logging_config.py` - Logging

## Getting Started

1. **First Time?** → Read `/docs/QUICKSTART.md`
2. **Want Details?** → Read `/README.md`
3. **Understanding Design?** → Read `/docs/ARCHITECTURE.md`
4. **Building Web Tests?** → See `/src/pages` and `/tests/web`
5. **Building API Tests?** → See `/src/api` and `/tests/api`
6. **Salesforce Tests?** → See `/src/salesforce` and `/tests/salesforce`
7. **Need Advanced Patterns?** → Read `/docs/ADVANCED_GUIDE.md`

## Development Workflow

```
1. Configure → Edit .env
2. Create Page Objects → Add to /src/pages
3. Create Tests → Add to /tests/web, /tests/api, or /tests/salesforce
4. Run Tests → pytest tests/
5. View Reports → Check /reports
6. Debug → Check /logs
```

## Key Concepts

- **Page Object Model** - Each page is a class with methods
- **Fixtures** - Reusable test setup in conftest.py
- **Markers** - Categorize tests (@pytest.mark.web, .api, .salesforce)
- **Async/Await** - All operations are asynchronous
- **Configuration** - Environment-based, no hardcoding

## File Dependencies

```
tests/
  ├── conftest.py
  ├── web/ → src/pages/ → src/core/base_page.py
  ├── api/ → src/api/ → src/core/api_client.py
  └── salesforce/ → src/salesforce/ → src/core/

All → src/utils/ (config, wait_utils, data_generator, assertions)
```

---

**For complete information, visit `/docs` directory**
