"""
MySQL database test examples.
"""
import pytest
from src.mcp_server.mysql_server import MySQLMCPServer, MySQLTestDataManager
from src.utils.config import Config


@pytest.fixture(scope="session")
def mysql_server():
    """Create MySQL server instance."""
    config = Config()
    server = MySQLMCPServer(
        host=config.get("MYSQL_HOST", "localhost"),
        port=int(config.get("MYSQL_PORT", 3306)),
        user=config.get("MYSQL_USER", "root"),
        password=config.get("MYSQL_PASSWORD", "Subh@1982"),
        database=config.get("MYSQL_DATABASE", "WebTestingDemo"),
        use_pymysql=config.get("MYSQL_USE_PYMYSQL", "false").lower() == "true"
    )
    
    # Connect to database
    if server.connect():
        yield server
        server.disconnect()
    else:
        pytest.skip("MySQL database not available")


@pytest.fixture(scope="function")
def test_data_manager(mysql_server):
    """Create test data manager."""
    return MySQLTestDataManager(mysql_server)


class TestMySQLConnection:
    """Test MySQL database connection."""
    
    def test_database_connection(self, mysql_server):
        """Test database connection is successful."""
        assert mysql_server.connection is not None
        assert mysql_server.connection.is_connected()
    
    def test_get_database_info(self, mysql_server):
        """Test getting database information."""
        info = mysql_server.get_database_info()
        
        assert info['host'] is not None
        assert info['database'] is not None
        assert info['version'] is not None
        assert isinstance(info['tables'], list)


class TestMySQLQueries:
    """Test MySQL query operations."""
    
    @pytest.fixture(autouse=True)
    def setup_test_table(self, mysql_server):
        """Setup test table before each test."""
        # Create test table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        mysql_server.execute_update(create_table_query)
        
        yield
        
        # Cleanup after test
        mysql_server.execute_update("DROP TABLE IF EXISTS test_users")
    
    def test_insert_and_query_data(self, mysql_server):
        """Test inserting and querying data."""
        # Insert test data
        test_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'age': 25
        }
        user_id = mysql_server.insert_test_data('test_users', test_data)
        
        assert user_id > 0
        
        # Query the data
        query = "SELECT * FROM test_users WHERE id = %s"
        results = mysql_server.execute_query(query, (user_id,))
        
        assert len(results) == 1
        assert results[0]['username'] == 'testuser'
        assert results[0]['email'] == 'test@example.com'
        assert results[0]['age'] == 25
    
    def test_update_data(self, mysql_server):
        """Test updating data."""
        # Insert test data
        test_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'age': 25
        }
        user_id = mysql_server.insert_test_data('test_users', test_data)
        
        # Update the data
        update_query = "UPDATE test_users SET age = %s WHERE id = %s"
        affected_rows = mysql_server.execute_update(update_query, (30, user_id))
        
        assert affected_rows == 1
        
        # Verify update
        query = "SELECT age FROM test_users WHERE id = %s"
        results = mysql_server.execute_query(query, (user_id,))
        assert results[0]['age'] == 30
    
    def test_delete_data(self, mysql_server):
        """Test deleting data."""
        # Insert test data
        test_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'age': 25
        }
        user_id = mysql_server.insert_test_data('test_users', test_data)
        
        # Delete the data
        mysql_server.cleanup_test_data('test_users', 'id = %s', (user_id,))
        
        # Verify deletion
        query = "SELECT * FROM test_users WHERE id = %s"
        results = mysql_server.execute_query(query, (user_id,))
        assert len(results) == 0
    
    def test_batch_insert(self, mysql_server):
        """Test batch insert using execute_many."""
        # Prepare batch data
        insert_query = "INSERT INTO test_users (username, email, age) VALUES (%s, %s, %s)"
        data = [
            ('user1', 'user1@example.com', 20),
            ('user2', 'user2@example.com', 25),
            ('user3', 'user3@example.com', 30)
        ]
        
        # Execute batch insert
        affected_rows = mysql_server.execute_many(insert_query, data)
        assert affected_rows == 3
        
        # Verify inserts
        count = mysql_server.get_row_count('test_users')
        assert count == 3


class TestMySQLTableOperations:
    """Test MySQL table operations."""
    
    @pytest.fixture(autouse=True)
    def setup_test_table(self, mysql_server):
        """Setup test table before each test."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2),
            stock INT DEFAULT 0
        )
        """
        mysql_server.execute_update(create_table_query)
        
        yield
        
        mysql_server.execute_update("DROP TABLE IF EXISTS test_products")
    
    def test_table_exists(self, mysql_server):
        """Test checking if table exists."""
        assert mysql_server.table_exists('test_products') is True
        assert mysql_server.table_exists('non_existent_table') is False
    
    def test_get_table_schema(self, mysql_server):
        """Test getting table schema."""
        schema = mysql_server.get_table_schema('test_products')
        
        assert len(schema) == 4
        column_names = [col['Field'] for col in schema]
        assert 'id' in column_names
        assert 'name' in column_names
        assert 'price' in column_names
        assert 'stock' in column_names
    
    def test_get_row_count(self, mysql_server):
        """Test getting row count."""
        # Insert some test data
        data = [
            ('Product 1', 10.99, 100),
            ('Product 2', 20.99, 50),
            ('Product 3', 30.99, 25)
        ]
        insert_query = "INSERT INTO test_products (name, price, stock) VALUES (%s, %s, %s)"
        mysql_server.execute_many(insert_query, data)
        
        # Get total count
        total_count = mysql_server.get_row_count('test_products')
        assert total_count == 3
        
        # Get count with condition
        count_with_condition = mysql_server.get_row_count('test_products', 'stock > 30')
        assert count_with_condition == 2
    
    def test_truncate_table(self, mysql_server):
        """Test truncating table."""
        # Insert test data
        data = [
            ('Product 1', 10.99, 100),
            ('Product 2', 20.99, 50)
        ]
        insert_query = "INSERT INTO test_products (name, price, stock) VALUES (%s, %s, %s)"
        mysql_server.execute_many(insert_query, data)
        
        # Verify data exists
        assert mysql_server.get_row_count('test_products') == 2
        
        # Truncate table
        mysql_server.truncate_table('test_products')
        
        # Verify table is empty
        assert mysql_server.get_row_count('test_products') == 0


class TestMySQLTestDataManager:
    """Test MySQL test data manager."""
    
    @pytest.fixture(autouse=True)
    def setup_test_table(self, mysql_server):
        """Setup test table before each test."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_number VARCHAR(50) NOT NULL,
            amount DECIMAL(10, 2),
            status VARCHAR(20)
        )
        """
        mysql_server.execute_update(create_table_query)
        
        yield
        
        mysql_server.execute_update("DROP TABLE IF EXISTS test_orders")
    
    def test_save_and_restore_snapshot(self, mysql_server, test_data_manager):
        """Test saving and restoring data snapshots."""
        # Insert initial data
        data = [
            ('ORD001', 100.00, 'pending'),
            ('ORD002', 200.00, 'completed')
        ]
        insert_query = "INSERT INTO test_orders (order_number, amount, status) VALUES (%s, %s, %s)"
        mysql_server.execute_many(insert_query, data)
        
        # Save snapshot
        test_data_manager.save_snapshot('initial_state', ['test_orders'])
        
        # Modify data
        mysql_server.execute_update("UPDATE test_orders SET status = 'cancelled'")
        
        # Verify modification
        results = mysql_server.execute_query("SELECT status FROM test_orders")
        assert all(row['status'] == 'cancelled' for row in results)
        
        # Restore snapshot
        test_data_manager.restore_snapshot('initial_state')
        
        # Verify restoration
        results = mysql_server.execute_query("SELECT * FROM test_orders ORDER BY id")
        assert len(results) == 2
        assert results[0]['status'] == 'pending'
        assert results[1]['status'] == 'completed'
    
    def test_cleanup_all_test_data(self, mysql_server, test_data_manager):
        """Test cleaning up all test data."""
        # Insert test data
        data = [
            ('ORD001', 100.00, 'pending'),
            ('ORD002', 200.00, 'completed'),
            ('ORD003', 300.00, 'pending')
        ]
        insert_query = "INSERT INTO test_orders (order_number, amount, status) VALUES (%s, %s, %s)"
        mysql_server.execute_many(insert_query, data)
        
        # Verify data exists
        assert mysql_server.get_row_count('test_orders') == 3
        
        # Cleanup all test data
        test_data_manager.cleanup_all_test_data(['test_orders'])
        
        # Verify cleanup
        assert mysql_server.get_row_count('test_orders') == 0


@pytest.mark.integration
class TestMySQLIntegration:
    """Integration tests for MySQL database operations."""
    
    def test_end_to_end_workflow(self, mysql_server, test_data_manager):
        """Test complete workflow with database operations."""
        # Create test table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            country VARCHAR(50)
        )
        """
        mysql_server.execute_update(create_table_query)
        
        try:
            # Save initial empty state
            test_data_manager.save_snapshot('empty_state', ['test_customers'])
            
            # Insert test customers
            customers = [
                ('John Doe', 'john@example.com', 'USA'),
                ('Jane Smith', 'jane@example.com', 'UK'),
                ('Bob Johnson', 'bob@example.com', 'Canada')
            ]
            insert_query = "INSERT INTO test_customers (name, email, country) VALUES (%s, %s, %s)"
            mysql_server.execute_many(insert_query, customers)
            
            # Query and verify
            results = mysql_server.execute_query("SELECT * FROM test_customers WHERE country = %s", ('USA',))
            assert len(results) == 1
            assert results[0]['name'] == 'John Doe'
            
            # Update customer
            mysql_server.execute_update("UPDATE test_customers SET country = %s WHERE email = %s", ('Australia', 'john@example.com'))
            
            # Verify update
            results = mysql_server.execute_query("SELECT country FROM test_customers WHERE email = %s", ('john@example.com',))
            assert results[0]['country'] == 'Australia'
            
            # Restore to empty state
            test_data_manager.restore_snapshot('empty_state')
            assert mysql_server.get_row_count('test_customers') == 0
            
        finally:
            # Cleanup
            mysql_server.execute_update("DROP TABLE IF EXISTS test_customers")
