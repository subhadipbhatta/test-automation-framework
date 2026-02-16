# Coffee API Testing Framework - Execution Guide

## Quick Start Instructions

### 1. **Generate Service Access Key**
```bash
# Open in browser:
https://webservice.toscacloud.com/training/
# Click "Generate New Key" button
# Copy the Service Access Key
```

### 2. **Run the Complete Test Suite**
```bash
# Option A: Step-by-step execution with interactive prompts
python tests/api/CoffeeAPI-TOSCA/coffee_api_step_by_step.py

# Option B: Run comprehensive pytest suite
pytest tests/api/CoffeeAPI-TOSCA/coffee_api_tests.py -v

# Option C: Run with specific service key
python -c "
from coffee_api_tests import CoffeeApiTester
tester = CoffeeApiTester('YOUR_SERVICE_KEY_HERE')
tester.run_complete_test_suite()
"
```

### 3. **Framework Features**

#### **📁 Generated Files:**
- `coffee_api_tests.py` - Complete Python API test automation framework
- `coffee_api_step_by_step.py` - Interactive step-by-step execution
- `CoffeAPI.json` - JSON test specification with all test cases

#### **🔧 Test Capabilities:**
- ✅ **GET Operations** - Retrieve all coffees and specific coffee by ID
- ✅ **POST Operations** - Create new coffee entries with validation
- ✅ **PUT Operations** - Update existing coffee information
- ✅ **DELETE Operations** - Remove coffee entries and verify deletion
- ✅ **Error Handling** - Test invalid requests and error responses
- ✅ **Data Validation** - Verify response structure and content
- ✅ **Comprehensive Logging** - Detailed execution logs and reports

#### **📊 Test Coverage:**
- **7 Positive Test Cases** - Valid operations across all HTTP methods
- **3 Negative Test Cases** - Error scenarios and edge cases
- **Full CRUD Workflow** - Complete Create, Read, Update, Delete cycle
- **Response Validation** - Structure, status codes, and data integrity

### 4. **Execution Examples**

#### **Interactive Step-by-Step Mode:**
```python
from coffee_api_step_by_step import StepByStepExecutor

# Initialize executor
executor = StepByStepExecutor()

# Run complete workflow (will prompt for service key)
results = executor.execute_complete_workflow()

# Run individual steps
executor.step_1_generate_service_key()
coffees = executor.step_3_get_all_coffees()
created_id = executor.step_6_create_coffee({
    "name": "Test Coffee",
    "description": "Created via API testing"
})
```

#### **Automated Test Suite:**
```python
from coffee_api_tests import CoffeeApiTester

# Initialize with service key
tester = CoffeeApiTester("YOUR_SERVICE_KEY_HERE")

# Run all tests
tester.run_complete_test_suite()

# Run specific test categories
tester.run_positive_tests()
tester.run_negative_tests()

# Generate detailed report
report = tester.generate_test_report()
print(report)
```

### 5. **Sample Output**

```
☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕
COFFEE API STEP-BY-STEP TESTING FRAMEWORK
☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕☕

================================================================================
STEP 1: GENERATE SERVICE ACCESS KEY
================================================================================
🌐 Please open: https://webservice.toscacloud.com/training/
👆 Click on 'Generate New Key' button
📋 Copy the generated Service Access Key

🔑 Please paste the Service Access Key here: [INPUT]

================================================================================
STEP 3: GET ALL COFFEES
================================================================================
[2024-01-15 10:30:15] Executing GET /api/Coffees
[2024-01-15 10:30:15] GET request completed
                      Data: Status: 200
✅ Response structure validation: PASSED

📋 Sample Coffee Data:
   1. ID: 1, Name: Ethiopian Blend
      Description: Rich and flavorful coffee from the highlands of Ethiopia...
   2. ID: 2, Name: Colombian Supreme
      Description: Smooth medium roast with chocolate undertones...

================================================================================
WORKFLOW EXECUTION SUMMARY
================================================================================
🕒 Total Execution Time: 12.34 seconds
✅ Steps Completed: 8
❌ Steps Failed: 0
🎯 Overall Status: SUCCESS

📊 Data Captured:
   Existing Coffee IDs: 5
   Created Coffee IDs: 2
   Updated Coffee IDs: 1
   Deleted Coffee IDs: 1

💾 Execution log saved to: coffee_api_execution_log_1705312215.json
🎉 All API operations completed successfully!
```

### 6. **Configuration Options**

The framework supports various configuration options through the `CoffeeApiConfig` class:

```python
class CoffeeApiConfig:
    BASE_URL = "https://webservice.toscacloud.com/training"
    REQUEST_TIMEOUT = 30
    REQUIRED_FIELDS = ["id", "name", "description"]
    
    # Customize test data
    COFFEE_TEST_DATA = [
        {
            "name": "Custom Coffee Name",
            "description": "Custom coffee description"
        }
    ]
```

### 7. **Integration with CI/CD**

The framework can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Coffee API Tests
on: [push, pull_request]
jobs:
  api_tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install requests pytest
      - name: Run API Tests
        env:
          SERVICE_KEY: ${{ secrets.TOSCA_SERVICE_KEY }}
        run: |
          python -c "
          from coffee_api_tests import CoffeeApiTester
          import os
          tester = CoffeeApiTester(os.environ['SERVICE_KEY'])
          results = tester.run_complete_test_suite()
          exit(0 if results['success'] else 1)
          "
```

---

## 🚀 Ready to Execute!

Your Coffee API testing framework is complete and ready for execution. Simply:

1. **Get your service key** from the TOSCA training endpoint
2. **Run the step-by-step executor** for interactive testing
3. **Use pytest integration** for automated test execution
4. **Review the generated logs** for detailed test results

The framework provides comprehensive coverage of the Coffee API with robust error handling, detailed logging, and both interactive and automated execution modes.