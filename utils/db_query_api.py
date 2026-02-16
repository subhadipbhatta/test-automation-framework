"""
Database Query API
Simple interface for querying the database with natural language.
Enhanced with latest user retrieval functionality.
"""
from intelligent_db_assistant import IntelligentDatabaseAssistant


class DatabaseQueryAPI:
    """Simple API for database queries."""
    
    def __init__(self):
        self.assistant = IntelligentDatabaseAssistant()
    
    def query(self, question: str) -> dict:
        """
        Query the database with a natural language question.
        
        Args:
            question (str): Natural language question
            
        Returns:
            dict: Response with success status and message
        """
        try:
            response = self.assistant.process_user_query(question)
            return {
                "success": True,
                "message": response,
                "query": question
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error processing query: {str(e)}",
                "query": question
            }
    
    def get_latest_user(self) -> dict:
        """
        Get the latest registered user from the database.
        
        Returns:
            dict: User information or error message
        """
        try:
            if not self.assistant.connect():
                return {
                    "success": False,
                    "message": "❌ Failed to connect to database"
                }
            
            # Try to get the latest user ordered by created_at or id
            try:
                query = """
                SELECT id, uid, firstName, lastName, email, pwd, Gender, created_at 
                FROM RegistrationInfo 
                ORDER BY created_at DESC 
                LIMIT 1
                """
                results = self.assistant.mysql_server.execute_query(query)
                order_field = "created_at"
            except Exception:
                # Fallback to ordering by id
                query = """
                SELECT id, uid, firstName, lastName, email, pwd, Gender 
                FROM RegistrationInfo 
                ORDER BY id DESC 
                LIMIT 1
                """
                results = self.assistant.mysql_server.execute_query(query)
                order_field = "id"
            
            if results:
                user = results[0]
                return {
                    "success": True,
                    "user": {
                        "id": user.get('id'),
                        "uid": user.get('uid'),
                        "firstName": user.get('firstName'),
                        "lastName": user.get('lastName'),
                        "email": user.get('email'),
                        "password": user.get('pwd'),
                        "gender": user.get('Gender'),
                        "created_at": user.get('created_at', 'N/A')
                    },
                    "message": f"✅ Latest user retrieved (ordered by {order_field})",
                    "ordered_by": order_field
                }
            else:
                return {
                    "success": False,
                    "message": "❌ No users found in the database"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error retrieving latest user: {str(e)}"
            }
    
    def get_recent_users(self, limit: int = 5) -> dict:
        """
        Get the most recent registered users from the database.
        
        Args:
            limit (int): Number of users to retrieve (default: 5)
            
        Returns:
            dict: List of recent users or error message
        """
        try:
            if not self.assistant.connect():
                return {
                    "success": False,
                    "message": "❌ Failed to connect to database"
                }
            
            try:
                query = """
                SELECT id, uid, firstName, lastName, email, pwd, Gender, created_at 
                FROM RegistrationInfo 
                ORDER BY created_at DESC 
                LIMIT %s
                """
                results = self.assistant.mysql_server.execute_query(query, (limit,))
                order_field = "created_at"
            except Exception:
                query = """
                SELECT id, uid, firstName, lastName, email, pwd, Gender 
                FROM RegistrationInfo 
                ORDER BY id DESC 
                LIMIT %s
                """
                results = self.assistant.mysql_server.execute_query(query, (limit,))
                order_field = "id"
            
            if results:
                users = []
                for user in results:
                    users.append({
                        "id": user.get('id'),
                        "uid": user.get('uid'),
                        "firstName": user.get('firstName'),
                        "lastName": user.get('lastName'),
                        "email": user.get('email'),
                        "password": user.get('pwd'),
                        "gender": user.get('Gender'),
                        "created_at": user.get('created_at', 'N/A')
                    })
                
                return {
                    "success": True,
                    "users": users,
                    "count": len(users),
                    "message": f"✅ Retrieved {len(users)} recent users (ordered by {order_field})",
                    "ordered_by": order_field
                }
            else:
                return {
                    "success": False,
                    "message": "❌ No users found in the database"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error retrieving recent users: {str(e)}"
            }
    
    def close(self):
        """Close the database connection."""
        self.assistant.disconnect()


# Enhanced utility functions
def get_latest_registered_user() -> dict:
    """Get the latest registered user with formatted output."""
    api = DatabaseQueryAPI()
    try:
        result = api.get_latest_user()
        
        if result["success"]:
            user = result["user"]
            formatted_output = f"""
✅ **Latest Registered User Found:**
{'='*50}
🆔 **User ID:** {user['id']}
🏷️ **UID:** {user['uid']}
👤 **First Name:** {user['firstName']}
👤 **Last Name:** {user['lastName']}
📧 **Email:** {user['email']}
🔒 **Password:** {user['password']}
⚧️ **Gender:** {user['gender']}
📅 **Created At:** {user['created_at']}
{'='*50}
            """
            print(formatted_output)
            return result
        else:
            print(result["message"])
            return result
    finally:
        api.close()


def get_recent_registered_users(count: int = 3) -> dict:
    """Get recent registered users with formatted output."""
    api = DatabaseQueryAPI()
    try:
        result = api.get_recent_users(count)
        
        if result["success"]:
            print(f"\n✅ **Found {result['count']} Recent Users (ordered by {result['ordered_by']}):**")
            print("="*80)
            
            for i, user in enumerate(result["users"], 1):
                print(f"\n**User #{i}:**")
                print(f"  🆔 ID: {user['id']}")
                print(f"  🏷️ UID: {user['uid']}")
                print(f"  👤 Name: {user['firstName']} {user['lastName']}")
                print(f"  📧 Email: {user['email']}")
                print(f"  🔒 Password: {user['password']}")
                print(f"  ⚧️ Gender: {user['gender']}")
                print(f"  📅 Created: {user['created_at']}")
                print("-" * 40)
            
            return result
        else:
            print(result["message"])
            return result
    finally:
        api.close()


def find_test_users() -> dict:
    """Find users created by test automation."""
    api = DatabaseQueryAPI()
    try:
        if not api.assistant.connect():
            print("❌ Failed to connect to database")
            return {"success": False, "message": "Connection failed"}
        
        # Query for test users (emails containing 'test' or 'testmail.com')
        query = """
        SELECT id, uid, firstName, lastName, email, pwd, Gender, created_at 
        FROM RegistrationInfo 
        WHERE email LIKE '%test%' OR email LIKE '%testmail.com%'
        ORDER BY id DESC
        """
        
        try:
            results = api.assistant.mysql_server.execute_query(query)
        except Exception:
            # Fallback without created_at
            query = """
            SELECT id, uid, firstName, lastName, email, pwd, Gender 
            FROM RegistrationInfo 
            WHERE email LIKE '%test%' OR email LIKE '%testmail.com%'
            ORDER BY id DESC
            """
            results = api.assistant.mysql_server.execute_query(query)
        
        if results:
            print(f"\n✅ **Found {len(results)} Test Users:**")
            print("="*80)
            
            test_users = []
            for i, user in enumerate(results, 1):
                user_data = {
                    "id": user.get('id'),
                    "uid": user.get('uid'),
                    "firstName": user.get('firstName'),
                    "lastName": user.get('lastName'),
                    "email": user.get('email'),
                    "password": user.get('pwd'),
                    "gender": user.get('Gender'),
                    "created_at": user.get('created_at', 'N/A')
                }
                test_users.append(user_data)
                
                print(f"\n**Test User #{i}:**")
                print(f"  🆔 ID: {user_data['id']}")
                print(f"  🏷️ UID: {user_data['uid']}")
                print(f"  👤 Name: {user_data['firstName']} {user_data['lastName']}")
                print(f"  📧 Email: {user_data['email']}")
                print(f"  🔒 Password: {user_data['password']}")
                print(f"  ⚧️ Gender: {user_data['gender']}")
                print(f"  📅 Created: {user_data['created_at']}")
                print("-" * 40)
            
            return {
                "success": True,
                "users": test_users,
                "count": len(test_users),
                "message": f"Found {len(test_users)} test users"
            }
        else:
            print("❌ No test users found in the database")
            return {
                "success": False,
                "message": "No test users found"
            }
            
    except Exception as e:
        error_msg = f"❌ Error retrieving test users: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "message": error_msg
        }
    finally:
        api.close()


# Legacy functions (keeping for backward compatibility)
def find_user_id(name: str) -> str:
    """Find user ID by name."""
    api = DatabaseQueryAPI()
    try:
        result = api.query(f"Find user {name}")
        return result["message"]
    finally:
        api.close()


def get_product_price(product_name: str) -> str:
    """Get product price by name."""
    api = DatabaseQueryAPI()
    try:
        result = api.query(f"What is the price of {product_name}")
        return result["message"]
    finally:
        api.close()


def find_deals() -> str:
    """Find all deals."""
    api = DatabaseQueryAPI()
    try:
        result = api.query("Show me all deals in Categories table")
        return result["message"]
    finally:
        api.close()


def get_database_tables() -> str:
    """List all database tables."""
    api = DatabaseQueryAPI()
    try:
        result = api.query("List all tables")
        return result["message"]
    finally:
        api.close()


if __name__ == "__main__":
    print("🤖 **Database User Query Tool**")
    print("=" * 50)
    
    # Get the latest registered user
    print("\n📍 **LATEST REGISTERED USER:**")
    latest_result = get_latest_registered_user()
    
    # Get recent users for context
    print("\n📋 **RECENT USERS (Last 3):**")
    recent_result = get_recent_registered_users(3)
    
    # Get test users created by automation
    print("\n🧪 **TEST USERS (Created by Automation):**")
    test_result = find_test_users()
    
    # Summary
    print("\n📊 **SUMMARY:**")
    if latest_result.get("success"):
        user = latest_result["user"]
        print(f"✅ Latest User: {user['firstName']} {user['lastName']} (ID: {user['id']})")
        print(f"📧 Email: {user['email']}")
        print(f"🔒 Password: {user['password']}")
    else:
        print("❌ No latest user found")