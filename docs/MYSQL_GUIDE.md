# MySQL MCP Server Guide

## Overview

The MySQL MCP Server provides comprehensive database testing capabilities for your test automation framework. It supports connection management, query execution, test data management, and snapshot/restore functionality.

## Features

✅ **Connection Management**
- MySQL Connector support
- PyMySQL support
- SQLAlchemy integration
- Connection pooling

✅ **Query Operations**
- SELECT queries with parameters
- INSERT/UPDATE/DELETE operations
- Batch operations
- Transaction support

✅ **Test Data Management**
- Insert test data
- Cleanup test data
- Data snapshots
- Snapshot restore

✅ **Table Operations**
- Table existence checks
- Schema inspection
- Row counting
- Table truncation

## Configuration

### 1. Environment Variables

Add MySQL configuration to your `.env` file:

```env
# MySQL Database Settings
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=test_automation
MYSQL_USE_PYMYSQL=false
```

### 2. Initialize MySQL Server

```python
from src.mcp_server.mysql_server import MySQLMCPServer

# Create server instance
mysql_server = MySQLMCPServer(
    host="localhost",
    port=3306,
    user="root",
    password="password",
    database="test_automation",
    use_pymysql=False  # Use mysql-connector by default
)

# Connect to database
if mysql_server.connect():
    print("Connected successfully!")
else:
    print("Connection failed")
```

## Basic Usage

### Execute SELECT Queries

```python
# Simple query
results = mysql_server.execute_query("SELECT * FROM users")

# Query with parameters
results = mysql_server.execute_query(
    "SELECT * FROM users WHERE age > %s",
    (25,)
)

for row in results:
    print(f"User: {row['username']}, Email: {row['email']}")
```

### Execute INSERT/UPDATE/DELETE

```python
# Insert data
affected_rows = mysql_server.execute_update(
    "INSERT INTO users (username, email) VALUES (%s, %s)",
    ('testuser', 'test@example.com')
)

# Update data
affected_rows = mysql_server.execute_update(
    "UPDATE users SET email = %s WHERE username = %s",
    ('newemail@example.com', 'testuser')
)

# Delete data
affected_rows = mysql_server.execute_update(
    "DELETE FROM users WHERE username = %s",
    ('testuser',)
)
```

### Batch Operations

```python
# Insert multiple rows
data = [
    ('user1', 'user1@example.com', 25),
    ('user2', 'user2@example.com', 30),
    ('user3', 'user3@example.com', 35)
]

affected_rows = mysql_server.execute_many(
    "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
    data
)
print(f"Inserted {affected_rows} rows")
```

## Test Data Management

### Insert Test Data

```python
# Insert test data with dictionary
test_data = {
    'username': 'testuser',
    'email': 'test@example.com',
    'age': 25
}
user_id = mysql_server.insert_test_data('users', test_data)
print(f"Inserted user with ID: {user_id}")
```

### Cleanup Test Data

```python
# Delete specific test data
mysql_server.cleanup_test_data('users', 'username = %s', ('testuser',))

# Delete all test data
mysql_server.cleanup_test_data('users')

# Truncate table (faster for large datasets)
mysql_server.truncate_table('users')
```

### Data Snapshots

```python
from src.mcp_server.mysql_server import MySQLTestDataManager

# Create test data manager
manager = MySQLTestDataManager(mysql_server)

# Save snapshot
manager.save_snapshot('initial_state', ['users', 'orders'])

# ... perform tests that modify data ...

# Restore snapshot
manager.restore_snapshot('initial_state')
```

## Table Operations

### Check Table Existence

```python
if mysql_server.table_exists('users'):
    print("Table exists!")
```

### Get Table Schema

```python
schema = mysql_server.get_table_schema('users')
for column in schema:
    print(f"Column: {column['Field']}, Type: {column['Type']}")
```

### Get Row Count

```python
# Total rows
total = mysql_server.get_row_count('users')

# Conditional count
active_users = mysql_server.get_row_count('users', 'status = "active"')
```

## Pytest Integration

### Fixtures

```python
import pytest
from src.mcp_server.mysql_server import MySQLMCPServer, MySQLTestDataManager
from src.utils.config import Config

@pytest.fixture(scope="session")
def mysql_server():
    """Create MySQL server instance."""
    config = Config()
    server = MySQLMCPServer(
        host=config.get("MYSQL_HOST"),
        port=int(config.get("MYSQL_PORT")),
        user=config.get("MYSQL_USER"),
        password=config.get("MYSQL_PASSWORD"),
        database=config.get("MYSQL_DATABASE")
    )
    
    if server.connect():
        yield server
        server.disconnect()
    else:
        pytest.skip("MySQL database not available")

@pytest.fixture
def test_data_manager(mysql_server):
    """Create test data manager."""
    return MySQLTestDataManager(mysql_server)
```

### Test Example

```python
class TestUserDatabase:
    """Test user database operations."""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mysql_server):
        """Setup and teardown for each test."""
        # Setup
        mysql_server.execute_update("""
            CREATE TABLE IF NOT EXISTS test_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
        """)
        
        yield
        
        # Teardown
        mysql_server.execute_update("DROP TABLE IF EXISTS test_users")
    
    def test_insert_user(self, mysql_server):
        """Test inserting a user."""
        test_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        user_id = mysql_server.insert_test_data('test_users', test_data)
        
        assert user_id > 0
        
        # Verify
        results = mysql_server.execute_query(
            "SELECT * FROM test_users WHERE id = %s",
            (user_id,)
        )
        assert len(results) == 1
        assert results[0]['username'] == 'testuser'
```

## Advanced Usage

### Execute SQL File

```python
# Execute SQL script from file
success = mysql_server.execute_sql_file('scripts/setup_database.sql')
if success:
    print("SQL file executed successfully")
```

### Database Information

```python
# Get database info
info = mysql_server.get_database_info()
print(f"Host: {info['host']}")
print(f"Database: {info['database']}")
print(f"Version: {info['version']}")
print(f"Tables: {', '.join(info['tables'])}")
```

### SQLAlchemy Session

```python
# Use SQLAlchemy session for ORM operations
with mysql_server.get_session() as session:
    # Perform ORM operations
    result = session.execute(text("SELECT * FROM users"))
    users = result.fetchall()
```

## Best Practices

### 1. Connection Management
```python
# Always disconnect when done
try:
    mysql_server.connect()
    # ... perform operations ...
finally:
    mysql_server.disconnect()
```

### 2. Test Isolation
```python
# Use snapshots for test isolation
@pytest.fixture(autouse=True)
def isolate_test(test_data_manager):
    # Save state before test
    test_data_manager.save_snapshot('before_test', ['users'])
    
    yield
    
    # Restore state after test
    test_data_manager.restore_snapshot('before_test')
```

### 3. Parameterized Queries
```python
# Always use parameters to prevent SQL injection
# ❌ BAD
query = f"SELECT * FROM users WHERE username = '{username}'"

# ✅ GOOD
query = "SELECT * FROM users WHERE username = %s"
results = mysql_server.execute_query(query, (username,))
```

### 4. Batch Operations
```python
# Use batch operations for better performance
# ❌ BAD
for user in users:
    mysql_server.insert_test_data('users', user)

# ✅ GOOD
data = [(u['name'], u['email']) for u in users]
mysql_server.execute_many(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    data
)
```

## Running Tests

```bash
# Run all database tests
pytest tests/database/ -v

# Run specific test file
pytest tests/database/test_mysql.py -v

# Run with specific marker
pytest tests/database/ -m integration -v

# Run with coverage
pytest tests/database/ --cov=src/mcp_server/mysql_server
```

## Troubleshooting

### Connection Issues

**Problem:** Cannot connect to MySQL database

**Solutions:**
1. Check MySQL service is running: `sudo systemctl status mysql`
2. Verify credentials in `.env` file
3. Check firewall settings
4. Ensure database exists: `CREATE DATABASE test_automation;`

### Permission Errors

**Problem:** Access denied for user

**Solutions:**
```sql
-- Grant permissions
GRANT ALL PRIVILEGES ON test_automation.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Import Errors

**Problem:** Module not found

**Solutions:**
```bash
# Install dependencies
pip install mysql-connector-python pymysql sqlalchemy

# Or use requirements.txt
pip install -r requirements.txt
```

## Examples

See complete examples in:
- `tests/database/test_mysql.py` - Comprehensive test examples
- `src/mcp_server/mysql_server.py` - Implementation details

## Next Steps

1. Configure MySQL connection in `.env`
2. Create database and tables
3. Write your first database test
4. Explore snapshot functionality
5. Integrate with CI/CD pipeline
