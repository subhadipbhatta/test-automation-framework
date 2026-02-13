# Salesforce Automation Guide

## Salesforce Testing

This guide covers Salesforce automation using the framework.

## Overview

The framework provides comprehensive Salesforce testing capabilities:
- OAuth2 authentication
- REST API integration
- UI automation
- SOQL queries
- Metadata operations

## Setup

### Prerequisites

1. Salesforce org with API access
2. Connected App created in Salesforce
3. OAuth2 credentials

### Configuration

Add to `.env`:
```env
SALESFORCE_INSTANCE=https://login.salesforce.com
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
```

## Authentication

### OAuth2 Authentication

```python
from src.salesforce.auth import SalesforceAuth

auth = SalesforceAuth(
    instance="https://login.salesforce.com",
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_username",
    password="your_password"
)

# Authenticate
access_token = await auth.authenticate()
instance_url = auth.instance_url
```

### Get Auth Header

```python
headers = auth.get_auth_header()
# Returns: {"Authorization": "Bearer <access_token>"}
```

## REST API Integration

### Create Salesforce API Client

```python
from src.salesforce.api_client import SalesforceAPIClient

api = SalesforceAPIClient(auth.instance_url, auth.access_token)
```

### Create Record

```python
# Create Account
data = {
    "Name": "Acme Corp",
    "Industry": "Technology"
}
record_id = await api.create_record("Account", data)
```

### Get Record

```python
record = await api.get_record("Account", "001D000000IRFmaIAH")
# Returns: {"Id": "001D000000IRFmaIAH", "Name": "Acme Corp", ...}
```

### Update Record

```python
data = {"Industry": "Software"}
await api.update_record("Account", "001D000000IRFmaIAH", data)
```

### Delete Record

```python
await api.delete_record("Account", "001D000000IRFmaIAH")
```

### Query Records (SOQL)

```python
# Simple query
soql = "SELECT Id, Name, Industry FROM Account LIMIT 10"
result = await api.query(soql)

# Query with WHERE clause
soql = "SELECT Id, Name FROM Contact WHERE AccountId = '001D000000IRFmaIAH'"
result = await api.query(soql)

# Query with aggregate functions
soql = "SELECT COUNT() FROM Opportunity WHERE StageName = 'Closed Won'"
result = await api.query(soql)
```

### Get Object Metadata

```python
metadata = await api.get_metadata("Account")
# Returns: {"fields": [...], "name": "Account", ...}
```

## UI Automation

### Salesforce Page Object

```python
from src.salesforce.base_salesforce_page import SalesforcePage

page_obj = SalesforcePage(page)
```

### Login to Salesforce

```python
await page_obj.login("username@example.com", "password")
```

### Navigate to Object

```python
await page_obj.navigate_to_object("Account")
```

### Search Record

```python
await page_obj.search_record("Acme Corp")
```

### Create Record via UI

```python
field_values = {
    "Name": "New Company",
    "Industry": "Finance"
}
record_id = await page_obj.create_record("Account", field_values)
```

### Update Record via UI

```python
field_values = {"Industry": "Banking"}
await page_obj.update_record(field_values)
```

### Delete Record

```python
await page_obj.delete_record()
```

### Logout

```python
await page_obj.logout()
```

## Example Tests

### API Tests

```python
@pytest.mark.salesforce
@pytest.mark.asyncio
class TestSalesforceAPI:
    @pytest.fixture
    async def salesforce_api(self, config):
        auth = SalesforceAuth(
            config.salesforce_instance,
            config.salesforce_client_id,
            config.salesforce_client_secret,
            config.salesforce_username,
            config.salesforce_password
        )
        await auth.authenticate()
        
        client = SalesforceAPIClient(auth.instance_url, auth.access_token)
        yield client
        await client.session.close()
    
    async def test_create_account(self, salesforce_api):
        data = {"Name": "Test Account"}
        account_id = await salesforce_api.create_record("Account", data)
        assert account_id
    
    async def test_query_accounts(self, salesforce_api):
        soql = "SELECT Id, Name FROM Account LIMIT 5"
        result = await salesforce_api.query(soql)
        assert "records" in result
    
    async def test_get_account_metadata(self, salesforce_api):
        metadata = await salesforce_api.get_metadata("Account")
        assert metadata["name"] == "Account"
```

### UI Tests

```python
@pytest.mark.salesforce
@pytest.mark.asyncio
class TestSalesforceUI:
    async def test_login_and_create_account(self, page, config):
        sf_page = SalesforcePage(page)
        
        # Login
        await sf_page.login(
            config.salesforce_username,
            config.salesforce_password
        )
        
        # Navigate to Accounts
        await sf_page.navigate_to_object("Account")
        
        # Create account
        fields = {
            "Name": "UI Test Account",
            "Industry": "Technology"
        }
        account_id = await sf_page.create_record("Account", fields)
        
        assert account_id
```

## Common SOQL Queries

### Get All Accounts
```soql
SELECT Id, Name, Industry, BillingCity FROM Account
```

### Get Contacts for Account
```soql
SELECT Id, FirstName, LastName, Email 
FROM Contact 
WHERE AccountId = 'ACCOUNT_ID'
```

### Get Opportunities by Stage
```soql
SELECT Id, Name, Amount, StageName 
FROM Opportunity 
WHERE StageName = 'Closed Won'
```

### Count Records
```soql
SELECT COUNT() 
FROM Opportunity 
WHERE IsClosed = true
```

### Get Related Records
```soql
SELECT Id, Name, 
  (SELECT FirstName, LastName FROM Contacts) 
FROM Account
```

## Best Practices

1. **Use Environment Variables** - Never hardcode credentials
2. **Handle Authentication** - Store and reuse tokens
3. **Limit Query Results** - Use LIMIT in SOQL queries
4. **Batch Operations** - Use composite requests for multiple operations
5. **Test Data Cleanup** - Delete test records after tests
6. **Error Handling** - Check for API errors and handle gracefully
7. **Logging** - Enable logging for debugging
8. **Wait for UI** - Use proper waits in UI tests

## Troubleshooting

### Authentication Fails

- Verify credentials in `.env`
- Check Connected App permissions
- Ensure OAuth scope includes API access

### SOQL Query Errors

- Check field API names (case-sensitive)
- Verify object relationships
- Use field aliases for complex queries

### UI Timeout Issues

- Increase `TEST_TIMEOUT` in `.env`
- Add explicit waits before interactions
- Take screenshots for debugging
