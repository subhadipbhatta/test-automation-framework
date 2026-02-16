"""
Script to query MySQL for products with deals
"""
import os
from dotenv import load_dotenv
from src.mcp_server.mysql_server import MySQLMCPServer

def main():
    # Load environment variables
    load_dotenv()
    
    # Create MySQL server instance
    mysql_server = MySQLMCPServer(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'test_automation'),
        encryption_key=os.getenv('ENCRYPTION_KEY')
    )
    
    # Connect to database
    if not mysql_server.connect():
        print('❌ Failed to connect to MySQL database')
        print('Please check your credentials in .env file')
        return
    
    print('✅ Connected to MySQL database successfully!')
    print(f'📊 Database: {mysql_server.database}')
    print()
    
    # Get database info
    info = mysql_server.get_database_info()
    print(f'🔧 MySQL Version: {info["version"]}')
    print(f'📋 Available Tables: {len(info["tables"])}')
    print()
    
    # List all tables
    print('📋 Tables in database:')
    for table in info['tables']:
        row_count = mysql_server.get_row_count(table)
        print(f'  - {table} ({row_count} rows)')
    print()
    
    # Look for products or deals tables
    product_tables = [t for t in info['tables'] if 'product' in t.lower()]
    deal_tables = [t for t in info['tables'] if 'deal' in t.lower()]
    
    print(f'🔍 Found {len(product_tables)} product table(s)')
    print(f'🔍 Found {len(deal_tables)} deal table(s)')
    print()
    
    # Explore product tables
    for table in product_tables:
        print(f'\\n📊 Exploring table: {table}')
        print('=' * 60)
        
        # Get table schema
        schema = mysql_server.get_table_schema(table)
        print('\\nColumns:')
        deal_columns = []
        for col in schema:
            print(f'  - {col["Field"]}: {col["Type"]}')
            if 'deal' in col['Field'].lower() or 'discount' in col['Field'].lower():
                deal_columns.append(col['Field'])
        
        print(f'\\n💰 Deal-related columns found: {deal_columns if deal_columns else "None"}')
        
        # Get row count
        count = mysql_server.get_row_count(table)
        print(f'\\n📈 Total rows: {count}')
        
        if count > 0:
            # Try to find products with deals
            print('\\n🎯 Searching for products with deals...')
            
            # Build dynamic query based on available columns
            queries = []
            if deal_columns:
                for col in deal_columns:
                    if 'price' in col.lower():
                        queries.append(f"SELECT * FROM {table} WHERE {col} IS NOT NULL AND {col} > 0 LIMIT 10")
                    else:
                        queries.append(f"SELECT * FROM {table} WHERE {col} = 1 OR {col} = TRUE LIMIT 10")
            
            # Also try generic queries
            queries.extend([
                f"SELECT * FROM {table} WHERE deal = 1 LIMIT 10",
                f"SELECT * FROM {table} WHERE has_deal = 1 LIMIT 10",
                f"SELECT * FROM {table} WHERE deal_price IS NOT NULL LIMIT 10",
                f"SELECT * FROM {table} WHERE discount > 0 LIMIT 10",
                f"SELECT * FROM {table} LIMIT 10",  # Fallback: show all products
            ])
            
            found = False
            for query in queries:
                try:
                    results = mysql_server.execute_query(query)
                    if results:
                        print(f'\\n✅ Found {len(results)} product(s) using query:')
                        print(f'   {query}')
                        print()
                        
                        for i, product in enumerate(results, 1):
                            print(f'\\n🛍️  Product {i}:')
                            print('-' * 50)
                            for key, value in product.items():
                                print(f'  {key}: {value}')
                        
                        found = True
                        break
                except Exception as e:
                    continue
            
            if not found:
                print('⚠️  Could not find products with deals using standard queries')
    
    # Check deal tables if any
    for table in deal_tables:
        print(f'\\n📊 Exploring deals table: {table}')
        print('=' * 60)
        
        schema = mysql_server.get_table_schema(table)
        print('\\nColumns:')
        for col in schema:
            print(f'  - {col["Field"]}: {col["Type"]}')
        
        count = mysql_server.get_row_count(table)
        print(f'\\n📈 Total rows: {count}')
        
        if count > 0:
            results = mysql_server.execute_query(f"SELECT * FROM {table} LIMIT 10")
            if results:
                print(f'\\n✅ First {len(results)} deals:')
                for i, deal in enumerate(results, 1):
                    print(f'\\n💰 Deal {i}:')
                    print('-' * 50)
                    for key, value in deal.items():
                        print(f'  {key}: {value}')
    
    # Disconnect
    mysql_server.disconnect()
    print('\\n✅ Disconnected from database')

if __name__ == '__main__':
    main()
