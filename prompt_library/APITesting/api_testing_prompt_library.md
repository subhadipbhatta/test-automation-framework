# API Testing Standard Prompt Library

This comprehensive prompt library provides standardized prompts for testing all common API request types and scenarios. Use these prompts to generate consistent, thorough API tests across different projects and frameworks.

## Table of Contents
- [CRUD Operations](#crud-operations)
- [Authentication & Authorization](#authentication--authorization)
- [Validation & Error Handling](#validation--error-handling)
- [Performance & Load Testing](#performance--load-testing)
- [Security Testing](#security-testing)
- [Integration & End-to-End Testing](#integration--end-to-end-testing)
- [API Documentation & Contract Testing](#api-documentation--contract-testing)

---

## CRUD Operations

### GET Requests

#### Get All Resources
```
Generate comprehensive API tests for GET all [RESOURCE_NAME] endpoint:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]
- Authentication: [AUTH_TYPE]
- Expected response: JSON array of [RESOURCE_NAME] objects
- Required fields in response: [FIELD_LIST]
- Test cases should include:
  * Successful retrieval with 200 status code
  * Response structure validation
  * Field type validation
  * Empty result handling
  * Response time validation (< 5 seconds)
  * Pagination testing if applicable
  * Sorting and filtering parameter testing
- Generate tests for Python requests library and Postman collection
```

#### Get Resource by ID
```
Generate API tests for GET [RESOURCE_NAME] by ID endpoint:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]/{id}
- Authentication: [AUTH_TYPE]
- Valid ID source: [ID_SOURCE]
- Test cases should include:
  * Successful retrieval with valid ID (200)
  * Response structure validation
  * ID matching validation
  * Non-existent ID handling (404)
  * Invalid ID format handling (400)
  * Unauthorized access (401)
  * Response time validation (< 3 seconds)
- Include dependency on GET all resources for ID capture
```

#### Get Resources with Query Parameters
```
Generate API tests for GET [RESOURCE_NAME] with query parameters:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]
- Supported parameters: [PARAMETER_LIST]
- Test cases should include:
  * Valid single parameter filtering
  * Multiple parameter combinations
  * Invalid parameter names
  * Invalid parameter values
  * Special characters in parameters
  * SQL injection attempts in parameters
  * Case sensitivity testing
  * Boundary value testing
- Generate parameterized tests with data-driven approach
```

### POST Requests

#### Create New Resource
```
Generate comprehensive API tests for POST create [RESOURCE_NAME]:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]
- Authentication: [AUTH_TYPE]
- Request body schema: [JSON_SCHEMA]
- Required fields: [REQUIRED_FIELDS]
- Optional fields: [OPTIONAL_FIELDS]
- Test cases should include:
  * Successful creation with all fields (201 or 200)
  * Successful creation with required fields only
  * Missing required field validation (400)
  * Invalid field type validation (400)
  * Duplicate resource handling
  * Field length validation
  * Special characters in fields
  * Empty request body handling
  * Oversized payload handling
  * Created resource ID capture for subsequent tests
- Include response structure validation
```

#### Create Multiple Resources (Bulk)
```
Generate API tests for bulk POST create [RESOURCE_NAME]:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]/bulk
- Authentication: [AUTH_TYPE]
- Request body: Array of [RESOURCE_NAME] objects
- Test cases should include:
  * Successful bulk creation
  * Partial success handling
  * Complete failure handling
  * Mixed valid/invalid data
  * Empty array handling
  * Single item in array
  * Maximum batch size testing
  * Transaction rollback testing
  * Performance testing with large batches
```

### PUT Requests

#### Update Existing Resource
```
Generate API tests for PUT update [RESOURCE_NAME]:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]/{id}
- Authentication: [AUTH_TYPE]
- Request body schema: [JSON_SCHEMA]
- Test cases should include:
  * Successful full update (200 or 204)
  * Partial field update
  * Non-existent ID handling (404)
  * Invalid ID format (400)
  * Missing required fields (400)
  * Invalid field types (400)
  * Unauthorized access (401/403)
  * Concurrent update handling
  * Update with same data (idempotency)
  * Field validation after update
- Include before/after state verification
```

#### Replace Resource (Full Update)
```
Generate API tests for PUT replace [RESOURCE_NAME]:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]/{id}
- Authentication: [AUTH_TYPE]
- Behavior: Complete resource replacement
- Test cases should include:
  * Full resource replacement
  * Clearing optional fields
  * Maintaining required fields
  * Version conflict handling
  * Resource state verification
  * Idempotency testing
  * Performance impact assessment
```

### PATCH Requests

#### Partial Update Resource
```
Generate API tests for PATCH partial update [RESOURCE_NAME]:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]/{id}
- Authentication: [AUTH_TYPE]
- Patch format: [JSON_PATCH/MERGE_PATCH]
- Test cases should include:
  * Single field update (200)
  * Multiple field update
  * Non-existent field handling
  * Read-only field update attempt
  * Invalid patch format (400)
  * Non-existent ID (404)
  * Patch operation validation
  * Atomic operation testing
  * Partial update rollback
```

### DELETE Requests

#### Delete Single Resource
```
Generate API tests for DELETE [RESOURCE_NAME]:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]/{id}
- Authentication: [AUTH_TYPE]
- Test cases should include:
  * Successful deletion (200, 202, or 204)
  * Non-existent ID handling (404)
  * Unauthorized deletion (401/403)
  * Deletion verification (subsequent GET returns 404)
  * Cascade deletion testing
  * Soft delete vs hard delete
  * Deletion with dependencies
  * Idempotency testing (multiple DELETE calls)
  * Recovery/undelete testing if supported
```

#### Bulk Delete Resources
```
Generate API tests for bulk DELETE [RESOURCE_NAME]:
- Base URL: [API_BASE_URL]
- Endpoint: [ENDPOINT_PATH]/bulk
- Request method: [DELETE/POST]
- Test cases should include:
  * Successful bulk deletion
  * Partial deletion handling
  * Non-existent IDs in batch
  * Mixed permissions in batch
  * Empty ID list handling
  * Maximum batch size testing
  * Transaction integrity
  * Rollback on failure
```

---

## Authentication & Authorization

### API Key Authentication
```
Generate authentication tests for API key-based authentication:
- Authentication header: [HEADER_NAME]
- API key format: [KEY_FORMAT]
- Test scenarios:
  * Valid API key (200/success)
  * Missing API key (401)
  * Invalid API key format (401)
  * Expired API key (401)
  * Revoked API key (401)
  * API key in wrong header (401)
  * Case sensitivity testing
  * Rate limiting with API key
  * Different permission levels per key
```

### JWT Token Authentication
```
Generate JWT authentication tests:
- Token header: Authorization: Bearer [TOKEN]
- Token endpoint: [TOKEN_ENDPOINT]
- Test scenarios:
  * Valid token access (200)
  * Missing token (401)
  * Malformed token (401)
  * Expired token (401)
  * Invalid signature (401)
  * Token refresh testing
  * Different user roles/permissions
  * Token blacklist testing
  * Token payload validation
```

### OAuth 2.0 Authentication
```
Generate OAuth 2.0 authentication flow tests:
- Authorization endpoint: [AUTH_ENDPOINT]
- Token endpoint: [TOKEN_ENDPOINT]
- Grant types: [GRANT_TYPES]
- Test scenarios:
  * Authorization code flow
  * Client credentials flow
  * Refresh token flow
  * Invalid client ID/secret
  * Scope validation
  * State parameter validation
  * PKCE implementation testing
  * Token expiration handling
```

### Role-Based Access Control
```
Generate RBAC tests for [RESOURCE_NAME] API:
- Roles: [ROLE_LIST]
- Permissions matrix: [PERMISSION_MATRIX]
- Test scenarios:
  * Admin full access (CRUD)
  * User read-only access
  * Manager partial access
  * Unauthorized role access (403)
  * Cross-tenant access prevention
  * Permission inheritance testing
  * Dynamic permission changes
  * Role escalation prevention
```

---

## Validation & Error Handling

### Input Validation Testing
```
Generate comprehensive input validation tests for [ENDPOINT]:
- Request body schema: [JSON_SCHEMA]
- Validation rules: [VALIDATION_RULES]
- Test cases:
  * Valid input formats
  * Invalid data types (400)
  * Missing required fields (400)
  * Field length violations (400)
  * Pattern/regex violations (400)
  * Numeric range violations (400)
  * Date format violations (400)
  * Email format validation
  * URL format validation
  * Enum value validation
  * Custom business rule validation
```

### Error Response Testing
```
Generate error response standardization tests:
- Error response format: [ERROR_FORMAT]
- Expected error fields: [ERROR_FIELDS]
- Test scenarios:
  * 400 Bad Request format consistency
  * 401 Unauthorized format consistency
  * 403 Forbidden format consistency
  * 404 Not Found format consistency
  * 409 Conflict format consistency
  * 422 Validation Error details
  * 500 Internal Server Error handling
  * Error message localization
  * Error correlation IDs
  * Stack trace exposure prevention
```

### Edge Case Testing
```
Generate edge case tests for [RESOURCE_NAME] API:
- Resource limits: [LIMITS]
- Boundary conditions: [BOUNDARIES]
- Test scenarios:
  * Minimum value boundaries
  * Maximum value boundaries
  * Zero values handling
  * Negative values handling
  * Null/undefined values
  * Empty string handling
  * Very long strings (1MB+)
  * Unicode character handling
  * Special character injection
  * Binary data handling
```

---

## Performance & Load Testing

### Response Time Testing
```
Generate performance tests for [ENDPOINT]:
- Expected response times: [TIME_LIMITS]
- Load conditions: [LOAD_CONDITIONS]
- Test scenarios:
  * Baseline response time measurement
  * Response time under normal load
  * Response time degradation points
  * Timeout handling (> [TIMEOUT]s)
  * Large payload response times
  * Database query optimization impact
  * Caching effectiveness testing
  * CDN performance impact
```

### Throughput Testing
```
Generate throughput tests for [API_NAME]:
- Expected TPS: [TRANSACTIONS_PER_SECOND]
- Test duration: [DURATION]
- Test scenarios:
  * Maximum sustained throughput
  * Throughput with increasing load
  * Concurrent user simulation
  * Resource utilization monitoring
  * Memory leak detection
  * Connection pool exhaustion
  * Rate limiting behavior
  * Auto-scaling trigger points
```

### Stress Testing
```
Generate stress tests for [API_ENDPOINTS]:
- Breaking point discovery
- Recovery testing
- Test scenarios:
  * Gradual load increase until failure
  * Sudden load spike handling
  * Resource exhaustion testing
  * Memory pressure testing
  * Database connection limits
  * File handle exhaustion
  * Network bandwidth limits
  * Graceful degradation testing
  * Circuit breaker activation
```

---

## Security Testing

### Input Sanitization
```
Generate security tests for input sanitization:
- Target endpoints: [ENDPOINT_LIST]
- Input fields: [INPUT_FIELDS]
- Test cases:
  * SQL injection attempts
  * XSS payload injection
  * Command injection attempts
  * LDAP injection testing
  * XML/JSON bomb attacks
  * Path traversal attempts
  * Script injection in all fields
  * HTML entity encoding validation
  * Input length overflow attacks
```

### Authentication Security
```
Generate authentication security tests:
- Authentication methods: [AUTH_METHODS]
- Security test cases:
  * Brute force attack protection
  * Account lockout mechanisms
  * Password complexity enforcement
  * Session hijacking prevention
  * Token replay attacks
  * Credential stuffing protection
  * Multi-factor authentication bypass
  * Session timeout enforcement
  * Concurrent session limits
```

### Authorization Security
```
Generate authorization security tests:
- Permission model: [PERMISSION_MODEL]
- Test scenarios:
  * Horizontal privilege escalation
  * Vertical privilege escalation
  * Direct object reference attacks
  * Parameter pollution attacks
  * Method tampering (GET to POST)
  * Resource enumeration attacks
  * Cross-tenant data access
  * API endpoint discovery
  * Hidden endpoint exposure
```

---

## Integration & End-to-End Testing

### Workflow Testing
```
Generate end-to-end workflow tests for [BUSINESS_PROCESS]:
- Workflow steps: [WORKFLOW_STEPS]
- Integration points: [INTEGRATION_POINTS]
- Test scenarios:
  * Complete happy path workflow
  * Workflow with error recovery
  * Partial workflow completion
  * Workflow rollback testing
  * Cross-service data consistency
  * Asynchronous operation handling
  * Event-driven workflow testing
  * Workflow state persistence
  * Concurrent workflow execution
```

### Third-Party Integration
```
Generate third-party integration tests:
- External services: [SERVICE_LIST]
- Integration methods: [INTEGRATION_METHODS]
- Test cases:
  * Successful integration calls
  * External service unavailability
  * Timeout handling
  * Rate limit handling
  * Data format compatibility
  * Authentication with external services
  * Fallback mechanism testing
  * Circuit breaker implementation
  * Retry logic validation
```

### Database Integration
```
Generate database integration tests for [API_NAME]:
- Database type: [DB_TYPE]
- Operations: [DB_OPERATIONS]
- Test scenarios:
  * CRUD operation data consistency
  * Transaction rollback testing
  * Connection pool management
  * Database failover handling
  * Read replica consistency
  * Bulk operation performance
  * Concurrent access handling
  * Data integrity constraints
  * Database migration compatibility
```

---

## API Documentation & Contract Testing

### OpenAPI/Swagger Validation
```
Generate OpenAPI specification validation tests:
- OpenAPI spec file: [SPEC_FILE_PATH]
- Validation scope: [VALIDATION_SCOPE]
- Test cases:
  * Request schema validation
  * Response schema validation
  * Path parameter validation
  * Query parameter validation
  * Header parameter validation
  * Content type validation
  * Status code coverage
  * Example data validation
  * Documentation completeness
```

### Contract Testing
```
Generate API contract tests using [CONTRACT_FRAMEWORK]:
- Provider: [PROVIDER_API]
- Consumer: [CONSUMER_API]
- Contract file: [CONTRACT_FILE]
- Test scenarios:
  * Provider contract fulfillment
  * Consumer expectation validation
  * Breaking change detection
  * Version compatibility testing
  * Contract evolution testing
  * Mock service validation
  * Backward compatibility
  * Forward compatibility
```

### API Versioning Testing
```
Generate API versioning tests:
- Versioning strategy: [VERSION_STRATEGY]
- Supported versions: [VERSION_LIST]
- Test cases:
  * Version header validation
  * URL path version validation
  * Default version behavior
  * Deprecated version warnings
  * Version-specific feature testing
  * Cross-version compatibility
  * Version migration testing
  * Sunset policy enforcement
```

---

## Usage Examples

### Basic CRUD Test Generation
```bash
# Example: Generate tests for User API
Use prompt: "Generate comprehensive API tests for GET all users endpoint"
Replace placeholders:
- [RESOURCE_NAME] → "users"
- [API_BASE_URL] → "https://api.example.com"
- [ENDPOINT_PATH] → "/v1/users"
- [AUTH_TYPE] → "Bearer JWT"
- [FIELD_LIST] → "id, username, email, created_at"
```

### Security Test Generation
```bash
# Example: Generate security tests for Payment API
Use prompt: "Generate security tests for input sanitization"
Replace placeholders:
- [ENDPOINT_LIST] → "/v1/payments, /v1/payments/{id}"
- [INPUT_FIELDS] → "amount, currency, card_number, cvv"
```

### Performance Test Generation
```bash
# Example: Generate performance tests for Order API
Use prompt: "Generate performance tests for [ENDPOINT]"
Replace placeholders:
- [ENDPOINT] → "/v1/orders"
- [TIME_LIMITS] → "GET: 2s, POST: 5s, PUT: 3s"
- [LOAD_CONDITIONS] → "100 concurrent users, 1000 requests/minute"
```

---

## Framework-Specific Adaptations

### Python Requests + Pytest
When generating tests for Python, include:
- pytest fixtures for setup/teardown
- parametrized tests for data-driven testing
- assertion libraries (pytest-assert, assertpy)
- HTTP client configuration (timeouts, retries)
- Environment variable handling
- Test report generation

### Postman Collections
When generating Postman tests, include:
- Collection variables for configuration
- Pre-request scripts for setup
- Test scripts for validation
- Dynamic variable extraction
- Environment management
- Newman CLI execution scripts

### REST Assured (Java)
When generating REST Assured tests, include:
- Given-When-Then structure
- JSON schema validation
- Response specification reuse
- Request/response logging
- TestNG/JUnit integration
- Maven/Gradle build configuration

### JavaScript/Node.js
When generating Node.js tests, include:
- Mocha/Jest test framework setup
- Axios/Fetch API configuration
- Async/await patterns
- Environment configuration
- Mock server setup
- Test data management

---

## Best Practices Reminders

1. **Always include negative test cases** alongside positive scenarios
2. **Test boundary conditions** and edge cases thoroughly
3. **Validate both request and response** structures
4. **Include performance benchmarks** in all test suites
5. **Test error handling** comprehensively
6. **Consider security implications** in every test
7. **Use data-driven testing** for comprehensive coverage
8. **Include cleanup procedures** to maintain test independence
9. **Document assumptions** and dependencies clearly
10. **Regular test maintenance** to keep pace with API evolution

---

*This prompt library is designed to be comprehensive and adaptable. Customize the placeholders and adjust the scope based on your specific API testing requirements.*