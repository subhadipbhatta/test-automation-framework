# Test Automation Framework

A comprehensive test automation framework supporting both API and Web testing with organized structure and comprehensive test libraries.

## Project Structure

```
Test-Automation-Framework/
├── config/                     # Configuration files
├── context_library/            # Test context and scenario libraries
├── docs/
│   └── markdown/              # All documentation files
├── prompt_library/            # Prompt engineering libraries
├── src/                       # Source code and page objects
├── test-runners/              # Test execution utilities
├── tests/
│   ├── api/                   # API test suites
│   │   ├── CoffeeAPI-TOSCA/   # Coffee API tests
│   │   └── PayPalAPI/         # PayPal API tests
│   └── web/
│       └── TricentisWeb/      # Web automation tests
├── utils/                     # Utility functions and helpers
└── venv/                      # Python virtual environment
```

## Key Features

### API Testing
- **Coffee API (TOSCA)**: Complete test suite with Python automation and Postman collections
- **PayPal API**: Comprehensive test cases with detailed assertion framework
- **API Testing Prompt Library**: Standardized testing patterns and templates

### Web Testing
- **Tricentis Web Application**: 15 E2E registration test scenarios
- **Playwright Integration**: Python-based web automation
- **JSON-driven Configuration**: Test data and configuration management

### Framework Components
- **Context Libraries**: Pre-built test scenarios and contexts
- **Prompt Libraries**: Standardized prompt templates for test generation
- **Test Runners**: Multiple execution utilities for different test scenarios
- **Comprehensive Documentation**: Organized in markdown format

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for Playwright)
- Virtual environment activated

### Setup
1. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. Run Playwright install:
   ```bash
   npx playwright install
   ```

### Running Tests

#### API Tests
```bash
# Coffee API Tests
python tests/api/CoffeeAPI-TOSCA/coffee_api.py

# PayPal API Tests (requires API credentials)
# Check PayPal_API_Test_Cases.json for test specifications
```

#### Web Tests
```bash
# Individual registration test
python tests/web/TricentisWeb/TricentisWeb_E2E_REG-01.py

# Using test runners
python test-runners/run_e2e_test.py
```

## Documentation

All documentation is organized in `docs/markdown/`:
- `README.md` - Main project documentation
- `QUICK_REFERENCE.md` - Quick reference guide
- `PROJECT_SUMMARY.md` - Project overview and features
- `FRAMEWORK_COMPLETE.md` - Comprehensive framework documentation

## Libraries and Resources

### Context Library
- Web testing contexts for different scenarios
- Pre-built test data and configurations

### Prompt Library
- API testing prompt templates
- Web testing scenario prompts
- Standardized test case generation patterns

## Contributing

See `docs/markdown/CONTRIBUTING.md` for contribution guidelines.

## License

See `LICENSE` file for license information.