"""
MySQL MCP Server for database operations and test data management.
"""
import logging
from typing import Any, Dict, List, Optional
import mysql.connector
from mysql.connector import Error
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from src.utils.encryption import EncryptionManager

logger = logging.getLogger(__name__)


class MySQLMCPServer:
    """MySQL MCP Server for database operations."""
    
    def __init__(
        self,
        host: str,
        port: int = 3306,
        user: str = "",
        password: str = "",
        database: str = "",
        use_pymysql: bool = False,
        encryption_key: str = None
    ):
        """
        Initialize MySQL MCP Server.
        
        Args:
            host: Database host
            port: Database port (default: 3306)
            user: Database user
            password: Database password (can be encrypted)
            database: Database name
            use_pymysql: Use PyMySQL instead of mysql-connector (default: False)
            encryption_key: Key for decrypting password (optional)
        """
        self.host = host
        self.port = port
        self.user = user
        
        # Decrypt password if needed
        encryption_manager = EncryptionManager(encryption_key)
        self.password = encryption_manager.decrypt_if_needed(password)
        
        self.database = database
        self.use_pymysql = use_pymysql
        self.connection = None
        self.engine = None
        self.Session = None
        
    def connect(self) -> bool:
        """
        Establish connection to MySQL database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            if self.use_pymysql:
                self.connection = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    cursorclass=pymysql.cursors.DictCursor
                )
            else:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            
            # Create SQLAlchemy engine
            if self.use_pymysql:
                connection_string = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            else:
                connection_string = f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            
            self.engine = create_engine(connection_string, echo=False)
            self.Session = sessionmaker(bind=self.engine)
            
            logger.info(f"Connected to MySQL database: {self.database}")
            return True
            
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")
    
    @contextmanager
    def get_session(self):
        """
        Context manager for SQLAlchemy session.
        
        Yields:
            Session: SQLAlchemy session
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute SELECT query and return results.
        
        Args:
            query: SQL query
            params: Query parameters (optional)
            
        Returns:
            List of dictionaries containing query results
        """
        try:
            cursor = self.connection.cursor(dictionary=True) if not self.use_pymysql else self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            cursor.close()
            
            logger.info(f"Query executed successfully: {query[:50]}...")
            return results
            
        except Error as e:
            logger.error(f"Error executing query: {e}")
            return []
    
    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query
            params: Query parameters (optional)
            
        Returns:
            Number of affected rows
        """
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            logger.info(f"Update executed: {affected_rows} rows affected")
            return affected_rows
            
        except Error as e:
            logger.error(f"Error executing update: {e}")
            self.connection.rollback()
            return 0
    
    def execute_many(self, query: str, data: List[tuple]) -> int:
        """
        Execute query with multiple data sets.
        
        Args:
            query: SQL query
            data: List of tuples containing query parameters
            
        Returns:
            Number of affected rows
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, data)
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            logger.info(f"Batch insert: {affected_rows} rows affected")
            return affected_rows
            
        except Error as e:
            logger.error(f"Error executing batch query: {e}")
            self.connection.rollback()
            return 0
    
    def insert_test_data(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert test data into a table.
        
        Args:
            table: Table name
            data: Dictionary of column-value pairs
            
        Returns:
            ID of inserted row
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            
            logger.info(f"Test data inserted into {table}: ID {last_id}")
            return last_id
            
        except Error as e:
            logger.error(f"Error inserting test data: {e}")
            self.connection.rollback()
            return 0
    
    def cleanup_test_data(self, table: str, condition: str = "", params: Optional[tuple] = None):
        """
        Clean up test data from a table.
        
        Args:
            table: Table name
            condition: WHERE clause (optional)
            params: Query parameters (optional)
        """
        query = f"DELETE FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        
        self.execute_update(query, params)
        logger.info(f"Test data cleaned from {table}")
    
    def get_table_schema(self, table: str) -> List[Dict[str, Any]]:
        """
        Get schema information for a table.
        
        Args:
            table: Table name
            
        Returns:
            List of column information
        """
        query = f"DESCRIBE {table}"
        return self.execute_query(query)
    
    def table_exists(self, table: str) -> bool:
        """
        Check if a table exists.
        
        Args:
            table: Table name
            
        Returns:
            True if table exists, False otherwise
        """
        query = """
        SELECT COUNT(*)
        FROM information_schema.tables 
        WHERE table_schema = %s 
        AND table_name = %s
        """
        result = self.execute_query(query, (self.database, table))
        return result[0]['COUNT(*)'] > 0 if result else False
    
    def get_row_count(self, table: str, condition: str = "") -> int:
        """
        Get row count from a table.
        
        Args:
            table: Table name
            condition: WHERE clause (optional)
            
        Returns:
            Number of rows
        """
        query = f"SELECT COUNT(*) as count FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def truncate_table(self, table: str):
        """
        Truncate a table (remove all rows).
        
        Args:
            table: Table name
        """
        query = f"TRUNCATE TABLE {table}"
        self.execute_update(query)
        logger.info(f"Table truncated: {table}")
    
    def execute_sql_file(self, file_path: str) -> bool:
        """
        Execute SQL statements from a file.
        
        Args:
            file_path: Path to SQL file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r') as file:
                sql_script = file.read()
            
            # Split by semicolon and execute each statement
            statements = sql_script.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    self.execute_update(statement)
            
            logger.info(f"SQL file executed: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing SQL file: {e}")
            return False
    
    def create_test_snapshot(self, tables: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Create a snapshot of test data from specified tables.
        
        Args:
            tables: List of table names
            
        Returns:
            Dictionary mapping table names to their data
        """
        snapshot = {}
        for table in tables:
            query = f"SELECT * FROM {table}"
            snapshot[table] = self.execute_query(query)
        
        logger.info(f"Test snapshot created for {len(tables)} tables")
        return snapshot
    
    def restore_test_snapshot(self, snapshot: Dict[str, List[Dict[str, Any]]]):
        """
        Restore test data from a snapshot.
        
        Args:
            snapshot: Dictionary mapping table names to their data
        """
        for table, rows in snapshot.items():
            # Truncate table first
            self.truncate_table(table)
            
            # Insert rows
            if rows:
                columns = list(rows[0].keys())
                column_names = ", ".join(columns)
                placeholders = ", ".join(["%s"] * len(columns))
                query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
                
                data = [tuple(row[col] for col in columns) for row in rows]
                self.execute_many(query, data)
        
        logger.info(f"Test snapshot restored for {len(snapshot)} tables")
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get database information.
        
        Returns:
            Dictionary containing database info
        """
        info = {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'version': None,
            'tables': []
        }
        
        # Get MySQL version
        version_query = "SELECT VERSION() as version"
        version_result = self.execute_query(version_query)
        if version_result:
            info['version'] = version_result[0]['version']
        
        # Get list of tables
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = %s
        """
        tables_result = self.execute_query(tables_query, (self.database,))
        # Handle both 'table_name' and 'TABLE_NAME' keys
        if tables_result:
            first_row = tables_result[0]
            key = 'table_name' if 'table_name' in first_row else 'TABLE_NAME'
            info['tables'] = [row[key] for row in tables_result]
        
        return info


class MySQLTestDataManager:
    """Manages test data for MySQL database tests."""
    
    def __init__(self, mysql_server: MySQLMCPServer):
        """
        Initialize test data manager.
        
        Args:
            mysql_server: MySQLMCPServer instance
        """
        self.db = mysql_server
        self.snapshots = {}
    
    def save_snapshot(self, name: str, tables: List[str]):
        """
        Save a snapshot of test data.
        
        Args:
            name: Snapshot name
            tables: List of tables to snapshot
        """
        self.snapshots[name] = self.db.create_test_snapshot(tables)
        logger.info(f"Snapshot '{name}' saved")
    
    def restore_snapshot(self, name: str):
        """
        Restore a saved snapshot.
        
        Args:
            name: Snapshot name
        """
        if name in self.snapshots:
            self.db.restore_test_snapshot(self.snapshots[name])
            logger.info(f"Snapshot '{name}' restored")
        else:
            logger.warning(f"Snapshot '{name}' not found")
    
    def cleanup_all_test_data(self, tables: List[str]):
        """
        Clean up test data from all specified tables.
        
        Args:
            tables: List of table names
        """
        for table in tables:
            self.db.cleanup_test_data(table)
        logger.info(f"Test data cleaned from {len(tables)} tables")
