"""
Intelligent Database Assistant
This assistant asks specific questions before executing queries to provide a better user experience.
"""
import os
import re
from dotenv import load_dotenv
from src.mcp_server.mysql_server import MySQLMCPServer


class IntelligentDatabaseAssistant:
    """Smart database assistant that asks specific questions."""
    
    def __init__(self):
        """Initialize the assistant."""
        load_dotenv()
        self.mysql_server = None
        self.tables = []
        self.connected = False
        self.current_context = {}
    
    def connect(self):
        """Connect to MySQL database silently."""
        try:
            self.mysql_server = MySQLMCPServer(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                port=int(os.getenv('MYSQL_PORT', 3306)),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', ''),
                database=os.getenv('MYSQL_DATABASE', 'WebTestingDemo'),
                encryption_key=os.getenv('ENCRYPTION_KEY')
            )
            
            if self.mysql_server.connect():
                info = self.mysql_server.get_database_info()
                self.tables = info['tables']
                self.connected = True
                return True
            return False
        except Exception:
            return False
    
    def disconnect(self):
        """Disconnect from database."""
        if self.mysql_server:
            self.mysql_server.disconnect()
    
    def process_user_query(self, user_input):
        """Process user query and ask specific questions if needed."""
        if not self.connected:
            if not self.connect():
                return "❌ Unable to connect to database. Please check your connection settings."
        
        # Analyze the user input to determine intent
        intent = self._analyze_intent(user_input)
        
        if intent == 'find_user':
            return self._handle_find_user(user_input)
        elif intent == 'find_product_price':
            return self._handle_find_product_price(user_input)
        elif intent == 'find_product':
            return self._handle_find_product(user_input)
        elif intent == 'find_deals':
            return self._handle_find_deals(user_input)
        elif intent == 'list_tables':
            return self._handle_list_tables()
        elif intent == 'table_schema':
            return self._handle_table_schema(user_input)
        elif intent == 'general_search':
            return self._handle_general_search(user_input)
        else:
            return self._provide_help()
    
    def _analyze_intent(self, user_input):
        """Analyze user input to determine intent."""
        lower_input = user_input.lower()
        
        if any(word in lower_input for word in ['user', 'customer', 'person', 'account']):
            return 'find_user'
        elif any(word in lower_input for word in ['price', 'cost', 'how much']):
            return 'find_product_price'
        elif any(word in lower_input for word in ['product', 'item']):
            return 'find_product'
        elif any(word in lower_input for word in ['deal', 'sale', 'discount', 'offer']):
            return 'find_deals'
        elif any(word in lower_input for word in ['tables', 'list', 'show all']):
            return 'list_tables'
        elif any(word in lower_input for word in ['schema', 'structure', 'columns']):
            return 'table_schema'
        elif any(word in lower_input for word in ['search', 'find', 'look']):
            return 'general_search'
        else:
            return 'unknown'
    
    def _handle_find_user(self, user_input):
        """Handle finding user information."""
        # Extract potential names from input (more flexible matching)
        name_patterns = [
            r'(?:find|get|search)\s+(?:user\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)',  # Simple "FirstName LastName" pattern
            r'user\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        name_match = None
        for pattern in name_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                name_match = match.group(1)
                break
        
        if name_match:
            names = name_match.split()
            if len(names) >= 2:
                first_name, last_name = names[0], names[-1]
                return self._search_user_by_name(first_name, last_name)
            elif len(names) == 1:
                return self._search_user_by_single_name(names[0])
        
        # If no names found, ask for clarification
        return """To find a user, I need more specific information:
        
🔍 **Please provide:**
- Full name (e.g., "David Jones")
- Or just first name or last name
- Or user ID if you have it

**Example:** "Find user David Jones" or "Find user with ID 123\""""
    
    def _handle_find_product_price(self, user_input):
        """Handle finding product price."""
        # Extract potential product names with improved patterns
        product_patterns = [
            r'"([^"]+)"',  # Quoted text
            r'price.*?(?:for|of)\s+([^.?!\n]+)',  # "price for/of X"
            r'cost.*?of\s+([^.?!\n]+)',   # "cost of X"
            r'how much.*?(?:is|for)\s+([^.?!\n]+)', # "how much is/for X"
            r'what.*?price.*?([A-Za-z][A-Za-z\s]+[A-Za-z])', # "what's the price of X"
        ]
        
        product_name = None
        for pattern in product_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                product_name = match.group(1).strip()
                # Clean up common words
                product_name = re.sub(r'^(the|a|an)\s+', '', product_name, flags=re.IGNORECASE)
                break
        
        if product_name:
            return self._search_product_price(product_name)
        
        return """To find a product price, I need the product name:
        
🔍 **Please specify:**
- Exact product name: "Build your own computer"
- Or provide a partial name and I'll search for matches

**Example:** "What's the price for Build your own computer?\""""
    
    def _handle_find_product(self, user_input):
        """Handle finding product information."""
        return """To find product information, please specify:
        
🔍 **What would you like to know?**
1. Product price: "What's the price of [product name]?"
2. Product details: "Show details for [product name]"
3. Search products: "Find products containing [keyword]"

**Please be more specific about what information you need.**"""
    
    def _handle_find_deals(self, user_input):
        """Handle finding deals."""
        table_specified = self._extract_table_from_input(user_input)
        
        if table_specified:
            return self._search_deals_in_table(table_specified)
        
        # Ask if user wants to specify a table
        return """To find deals, I can search in different ways:
        
🔍 **Please choose:**
1. Search in a specific table (faster)
2. Search all tables (comprehensive)

**If you know the table name, please specify it. Otherwise, I'll search everywhere.**

Available tables: Categories, RegistrationInfo"""
    
    def _handle_list_tables(self):
        """Handle listing tables."""
        if not self.tables:
            return "❌ No tables found in the database."
        
        result = "📋 **Available Tables:**\n\n"
        for i, table in enumerate(self.tables, 1):
            try:
                count = self.mysql_server.get_row_count(table)
                result += f"{i}. **{table}** ({count:,} rows)\n"
            except:
                result += f"{i}. **{table}** (unable to get count)\n"
        
        return result
    
    def _handle_table_schema(self, user_input):
        """Handle table schema requests."""
        table_name = self._extract_table_from_input(user_input)
        
        if table_name and table_name in self.tables:
            return self._show_table_schema(table_name)
        
        return f"""To show table schema, please specify the table name:
        
🔍 **Available tables:**
{', '.join(self.tables)}

**Example:** "Show schema for Categories table\""""
    
    def _handle_general_search(self, user_input):
        """Handle general search requests."""
        return """For a general search, please be more specific:
        
🔍 **Search options:**
1. **Find user:** "Find user David Jones"
2. **Product price:** "What's the price of [product]?"
3. **Find deals:** "Show me all deals"
4. **Table info:** "List all tables" or "Show schema for [table]"

**What specifically would you like to search for?**"""
    
    def _provide_help(self):
        """Provide help information."""
        return """🤖 **Intelligent Database Assistant**

I can help you with:

🔍 **User Queries:**
- "Find user David Jones"
- "Get user ID for John Smith"

💰 **Product Queries:**
- "What's the price of Build your own computer?"
- "Show me all deals"

📊 **Database Info:**
- "List all tables"
- "Show schema for Categories table"

🔎 **General Search:**
- "Search for keyword in all tables"

**Just ask me a question in plain English!**"""
    
    def _extract_table_from_input(self, user_input):
        """Extract table name from user input."""
        lower_input = user_input.lower()
        for table in self.tables:
            if table.lower() in lower_input:
                return table
        return None
    
    def _search_user_by_name(self, first_name, last_name):
        """Search for user by first and last name."""
        try:
            query = "SELECT * FROM RegistrationInfo WHERE firstName = %s AND lastName = %s"
            results = self.mysql_server.execute_query(query, (first_name, last_name))
            
            if results:
                result_text = f"✅ **Found {len(results)} user(s) for {first_name} {last_name}:**\n\n"
                for i, record in enumerate(results, 1):
                    result_text += f"**User #{i}:**\n"
                    result_text += f"- **ID:** {record.get('id')}\n"
                    result_text += f"- **UID:** {record.get('uid')}\n"
                    result_text += f"- **Email:** {record.get('email')}\n"
                    result_text += f"- **Gender:** {record.get('Gender')}\n"
                    result_text += f"- **Created:** {record.get('created_at')}\n\n"
                return result_text
            else:
                # Try fuzzy search
                return self._fuzzy_search_user(first_name, last_name)
        except Exception as e:
            return f"❌ Error searching for user: {str(e)}"
    
    def _search_user_by_single_name(self, name):
        """Search for user by single name (first or last)."""
        try:
            query = "SELECT * FROM RegistrationInfo WHERE firstName LIKE %s OR lastName LIKE %s"
            results = self.mysql_server.execute_query(query, (f'%{name}%', f'%{name}%'))
            
            if results:
                result_text = f"✅ **Found {len(results)} user(s) matching '{name}':**\n\n"
                for i, record in enumerate(results[:5], 1):  # Limit to 5 results
                    result_text += f"**User #{i}:**\n"
                    result_text += f"- **Name:** {record.get('firstName')} {record.get('lastName')}\n"
                    result_text += f"- **ID:** {record.get('id')}\n"
                    result_text += f"- **Email:** {record.get('email')}\n\n"
                
                if len(results) > 5:
                    result_text += f"... and {len(results) - 5} more results\n"
                
                return result_text
            else:
                return f"❌ No users found matching '{name}'"
        except Exception as e:
            return f"❌ Error searching for user: {str(e)}"
    
    def _fuzzy_search_user(self, first_name, last_name):
        """Perform fuzzy search for user."""
        try:
            query = "SELECT * FROM RegistrationInfo WHERE firstName LIKE %s OR lastName LIKE %s"
            results = self.mysql_server.execute_query(query, (f'%{first_name}%', f'%{last_name}%'))
            
            if results:
                result_text = f"❌ No exact match for '{first_name} {last_name}'\n"
                result_text += f"✅ **Found {len(results)} similar user(s):**\n\n"
                for i, record in enumerate(results[:3], 1):
                    result_text += f"**User #{i}:**\n"
                    result_text += f"- **Name:** {record.get('firstName')} {record.get('lastName')}\n"
                    result_text += f"- **ID:** {record.get('id')}\n"
                    result_text += f"- **Email:** {record.get('email')}\n\n"
                return result_text
            else:
                return f"❌ No users found matching '{first_name}' or '{last_name}'"
        except Exception as e:
            return f"❌ Error in fuzzy search: {str(e)}"
    
    def _search_product_price(self, product_name):
        """Search for product price."""
        try:
            # Try exact match first
            query = "SELECT * FROM Categories WHERE Product_title = %s"
            results = self.mysql_server.execute_query(query, (product_name,))
            
            if not results:
                # Try partial match
                query = "SELECT * FROM Categories WHERE Product_title LIKE %s"
                results = self.mysql_server.execute_query(query, (f'%{product_name}%',))
            
            if results:
                if len(results) == 1:
                    product = results[0]
                    result_text = f"✅ **Product Found:**\n\n"
                    result_text += f"**{product.get('Product_title')}**\n"
                    result_text += f"💰 **Price:** ${product.get('Product_price')}\n"
                    result_text += f"📊 **Category:** {product.get('category_type')}\n"
                    result_text += f"⭐ **Rating:** {product.get('Product_Star')} stars\n"
                    result_text += f"📝 **Reviews:** {product.get('Product_noOfReviews')}\n"
                    result_text += f"🏷️ **Deal:** {product.get('Product_deal')}\n"
                    return result_text
                else:
                    result_text = f"✅ **Found {len(results)} products matching '{product_name}':**\n\n"
                    for i, product in enumerate(results[:5], 1):
                        result_text += f"**{i}. {product.get('Product_title')}** - ${product.get('Product_price')}\n"
                    
                    if len(results) > 5:
                        result_text += f"\n... and {len(results) - 5} more results\n"
                    result_text += "\n**Please be more specific for detailed information.**"
                    return result_text
            else:
                return f"❌ No products found matching '{product_name}'"
        except Exception as e:
            return f"❌ Error searching for product: {str(e)}"
    
    def _search_deals_in_table(self, table_name):
        """Search for deals in specific table."""
        if table_name not in self.tables:
            return f"❌ Table '{table_name}' not found. Available tables: {', '.join(self.tables)}"
        
        try:
            if table_name == 'Categories':
                query = "SELECT * FROM Categories WHERE Product_deal = 'Sale'"
                results = self.mysql_server.execute_query(query)
                
                if results:
                    result_text = f"✅ **Found {len(results)} products with deals:**\n\n"
                    for i, product in enumerate(results[:10], 1):
                        result_text += f"**{i}. {product.get('Product_title')}**\n"
                        result_text += f"   💰 Price: ${product.get('Product_price')}\n"
                        result_text += f"   📊 Category: {product.get('category_type')}\n\n"
                    
                    if len(results) > 10:
                        result_text += f"... and {len(results) - 10} more deals\n"
                    
                    return result_text
                else:
                    return f"❌ No deals found in {table_name} table"
            else:
                return f"❌ Deal information not available in {table_name} table"
        except Exception as e:
            return f"❌ Error searching for deals: {str(e)}"
    
    def _show_table_schema(self, table_name):
        """Show table schema."""
        try:
            schema = self.mysql_server.get_table_schema(table_name)
            count = self.mysql_server.get_row_count(table_name)
            
            result_text = f"📊 **Schema for table: {table_name}**\n"
            result_text += f"📈 **Total rows:** {count:,}\n\n"
            
            result_text += "**Columns:**\n"
            for col in schema:
                result_text += f"- **{col['Field']}** ({col['Type']}) "
                if col['Null'] == 'NO':
                    result_text += "- Required"
                if col['Key'] == 'PRI':
                    result_text += "- Primary Key"
                result_text += "\n"
            
            return result_text
        except Exception as e:
            return f"❌ Error getting schema: {str(e)}"


def main():
    """Main function for command-line usage."""
    assistant = IntelligentDatabaseAssistant()
    
    print("🤖 Intelligent Database Assistant")
    print("=" * 50)
    print("Ask me questions about the database in plain English!")
    print("Type 'exit' or 'quit' to stop.\n")
    
    try:
        while True:
            user_input = input("💭 Your question: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                print("Please enter a question.")
                continue
            
            print("\n🔍 Processing...")
            response = assistant.process_user_query(user_input)
            print(f"\n{response}\n")
            print("-" * 50)
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    finally:
        assistant.disconnect()


# Function to be called by other modules
def ask_database_question(question):
    """Function to ask a database question programmatically."""
    assistant = IntelligentDatabaseAssistant()
    try:
        response = assistant.process_user_query(question)
        return response
    finally:
        assistant.disconnect()


if __name__ == '__main__':
    main()