# API Guide

## REST API Testing

This guide covers API automation using the framework.

## Overview

The framework provides comprehensive REST API testing capabilities:
- HTTP method support (GET, POST, PUT, PATCH, DELETE)
- Authentication handling
- Response validation
- Error handling
- Assertion utilities

## Basic Usage

### Creating API Client

```python
from src.core.api_client import APIClient

async with APIClient(base_url="http://api.example.com") as client:
    # Make requests
    response = await client.get("/users")
```

### Making Requests

#### GET Request
```python
response = await client.get("/users/1")
# Returns: {"status": 200, "body": {...}, "headers": {...}}
```

#### POST Request
```python
data = {"name": "John", "email": "john@example.com"}
response = await client.post("/users", data=data)
```

#### PUT Request
```python
data = {"name": "Jane"}
response = await client.put("/users/1", data=data)
```

#### PATCH Request
```python
data = {"email": "newemail@example.com"}
response = await client.patch("/users/1", data=data)
```

#### DELETE Request
```python
response = await client.delete("/users/1")
```

## Authentication

### Bearer Token
```python
client.set_auth_header("your_token")
```

### Custom Auth Type
```python
client.set_auth_header("your_token", auth_type="Bearer")
```

### Basic Auth
```python
client.set_auth_header("credentials", auth_type="Basic")
```

## Response Handling

Response structure:
```python
{
    "status": 200,
    "body": {...},  # Parsed JSON or text
    "headers": {...}
}
```

## Assertions

### Assert Status Code
```python
from src.api.test_base import APITestBase

test = APITestBase(client)

response = await client.get("/users")
await test.assert_status_code(response, 200)
```

### Assert Response Contains
```python
await test.assert_response_contains(response, "id", 1)
await test.assert_response_contains(response, "name")
```

### Assert Response Structure
```python
await test.assert_response_structure(response, ["id", "name", "email"])
```

### Assert Response is List
```python
await test.assert_response_is_list(response, min_length=5)
```

### Assert Error Response
```python
await test.assert_error_response(response, 404, "error")
```

## Example Tests

### User API Tests
```python
@pytest.mark.api
@pytest.mark.asyncio
class TestUserAPI:
    @pytest.fixture
    async def api_client(self):
        async with APIClient("http://api.example.com") as client:
            yield client
    
    async def test_get_users(self, api_client):
        response = await api_client.get("/users")
        assert response["status"] == 200
    
    async def test_create_user(self, api_client):
        data = {"name": "John", "email": "john@example.com"}
        response = await api_client.post("/users", data=data)
        assert response["status"] == 201
    
    async def test_update_user(self, api_client):
        data = {"name": "Jane"}
        response = await api_client.put("/users/1", data=data)
        assert response["status"] == 200
    
    async def test_delete_user(self, api_client):
        response = await api_client.delete("/users/1")
        assert response["status"] == 204
```

## Custom Headers

```python
headers = {
    "X-Custom-Header": "value",
    "Content-Type": "application/json"
}

response = await client.get("/users", headers=headers)
```

## Query Parameters

```python
# Using kwargs for params
response = await client.get("/users", params={"page": 1, "limit": 10})
```

## Error Handling

```python
try:
    response = await client.get("/users/999")
    if response["status"] == 404:
        print("User not found")
except Exception as e:
    print(f"Request failed: {e}")
```

## Best Practices

1. **Use Base URLs** - Set base URL in client initialization
2. **Set Headers Upfront** - Set common headers once
3. **Use Fixtures** - Create API client in fixtures
4. **Validate Responses** - Always assert response structure
5. **Handle Errors** - Check status codes and error messages
6. **Use Async Properly** - Leverage async/await for concurrency
7. **Reuse Clients** - Reuse client instances when possible
8. **Log Requests** - Enable logging for debugging
