# Intelligent Database Assistant

## Overview

The Intelligent Database Assistant is a smart interface that processes natural language queries and asks specific questions to clarify user intent, rather than showing code execution to users.

## Features

### ✅ Natural Language Processing
- Understands user intent from plain English questions
- Asks specific clarification questions when needed
- No code shown to users - clean, user-friendly responses

### ✅ Smart Query Types

1. **User Queries**
   - "Find user David Jones"
   - "Get user ID for John Smith"

2. **Product Price Queries**
   - "What's the price of Build your own computer?"
   - "How much does Build your own cheap computer cost?"

3. **Deal Finding**
   - "Show me all deals"
   - "Find deals in Categories table"

4. **Database Information**
   - "List all tables"
   - "Show schema for Categories table"

## Usage

### Interactive Mode
```bash
python intelligent_db_assistant.py
```

### API Mode
```python
from db_query_api import DatabaseQueryAPI

api = DatabaseQueryAPI()
result = api.query("Find user David Jones")
print(result["message"])
api.close()
```

### Quick Functions
```python
from db_query_api import find_user_id, get_product_price, find_deals

# Find user
user_info = find_user_id("David Jones")

# Get price
price_info = get_product_price("Build your own computer")

# Find deals
deals = find_deals()
```

## How It Works

### 1. Intent Analysis
The assistant analyzes user input to determine what they want:
- User lookup
- Product price inquiry
- Deal search
- Database information

### 2. Smart Questions
When information is unclear, it asks specific questions:
- "Please specify the table name"
- "Which product are you looking for?"
- "Do you want to search all tables or specific table?"

### 3. Clean Responses
Users see formatted, helpful responses instead of raw database output or code.

## Example Interactions

### Finding a User
```
User: "Find David Jones"
Assistant: ✅ Found 2 user(s) for David Jones:

**User #1:**
- **ID:** 7
- **UID:** user17709227206418
- **Email:** david.jones@testdemo.com
- **Gender:** Male
```

### Product Price Query
```
User: "What's the price of Build your own cheap computer?"
Assistant: ✅ Product Found:

**Build your own cheap computer**
💰 **Price:** $800.00
📊 **Category:** Computers - Desktops
⭐ **Rating:** 4.00 stars
```

### When Clarification Needed
```
User: "Find product"
Assistant: To find product information, please specify:

🔍 **What would you like to know?**
1. Product price: "What's the price of [product name]?"
2. Product details: "Show details for [product name]"
3. Search products: "Find products containing [keyword]"
```

## Key Benefits

1. **User-Friendly**: No code or technical details shown
2. **Intelligent**: Understands context and asks smart questions
3. **Flexible**: Handles various query formats
4. **Safe**: Only executes safe SELECT queries
5. **Fast**: Direct database access with optimized queries

## Integration

### With Test Automation
```python
from db_query_api import find_user_id

# In your test
user_info = find_user_id("David Jones")
user_id = extract_id_from_response(user_info)  # Custom parser
```

### With Web Applications
```python
from intelligent_db_assistant import ask_database_question

@app.route('/api/query', methods=['POST'])
def query_database():
    question = request.json.get('question')
    response = ask_database_question(question)
    return {"response": response}
```

## Error Handling

The system gracefully handles:
- Connection failures
- Invalid queries
- Missing data
- Ambiguous requests

## Security

- Only SELECT queries allowed
- No direct SQL injection possible
- Parameterized queries used
- Encrypted credentials support