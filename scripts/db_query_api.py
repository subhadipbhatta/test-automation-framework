"""
Database Query API
Simple interface for querying the database with natural language.
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
    
    def close(self):
        """Close the database connection."""
        self.assistant.disconnect()


# Example usage functions
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
    # Example usage
    print("🔍 Finding David Jones:")
    print(find_user_id("David Jones"))
    
    print("\n💰 Getting product price:")
    print(get_product_price("Build your own cheap computer"))
    
    print("\n🏷️ Finding deals:")
    print(find_deals())