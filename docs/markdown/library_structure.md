# Context and Prompt Library Structure

## Directory Organization

```
context_library/
├── user_management_context.md          # User registration, login, profile contexts
├── product_management_context.md       # Product search, details, catalog contexts  
├── shopping_cart_context.md           # Cart operations and persistence contexts
├── checkout_context.md                # Checkout process and payment contexts
└── general_testing_context.md         # Navigation, performance, accessibility contexts

prompt_library/
├── registration_prompts.md            # User registration test prompts
├── login_prompts.md                   # Authentication and session prompts
├── product_search_prompts.md          # Product discovery and search prompts
├── product_details_prompts.md         # Product information validation prompts
├── shopping_cart_prompts.md           # Shopping cart management prompts
├── checkout_prompts.md                # Checkout process test prompts
├── user_profile_prompts.md            # User profile management prompts
└── validation_prompts.md              # Database and data validation prompts
```

## Usage Guidelines

### Context Files
- Provide background information and testing scenarios
- Set expectations for test execution environment
- Define success criteria and validation points
- Include prerequisite information and setup requirements
- Establish testing scope and objectives

### Prompt Files  
- Contain specific step-by-step test instructions
- Include test data placeholders for dynamic value injection
- Define expected results for validation and verification
- Organized by functional area for easy navigation
- Include both positive and negative test scenarios

## Naming Conventions

### Context Files
- Format: `{functional_area}_context.md`
- Examples: `user_management_context.md`, `product_management_context.md`
- Descriptive names indicating functional coverage area

### Prompt Files
- Format: `{functional_area}_prompts.md`
- Examples: `registration_prompts.md`, `login_prompts.md`  
- Aligned with corresponding context file names

### Individual Prompts
- Format: `{AREA}_{###}_{Description}`
- Examples: `REG_001_Valid_Male_Registration`, `LOGIN_002_Invalid_Password`
- Sequential numbering within each functional area
- Descriptive names indicating test purpose

## Test Data Integration

All prompts support dynamic test data injection using standardized placeholders:

### User Data Placeholders
- `{firstName}` - User's first name
- `{lastName}` - User's last name  
- `{email}` - User's email address
- `{password}` - User's password
- `{newPassword}` - Updated password for change scenarios
- `{gender}` - User's gender (Male/Female)
- `{uid}` - Unique user identifier

### Product Data Placeholders  
- `{productName}` - Product name for testing
- `{category}` - Product category
- `{price}` - Product price information
- `{keyword}` - Search keyword
- `{minPrice}` - Minimum price for filtering
- `{maxPrice}` - Maximum price for filtering

### Address Data Placeholders
- `{address}` - Street address
- `{city}` - City name  
- `{zipCode}` - ZIP/postal code
- `{country}` - Country name
- `{phone}` - Phone number

### Order Data Placeholders
- `{orderNumber}` - Order identification number
- `{orderTotal}` - Total order amount
- `{shippingAddress}` - Complete shipping address
- `{billingAddress}` - Complete billing address

## Latest User Credentials Template

Based on database query execution, use these credential placeholders:
```json
{
  "id": "{latestUserId}",
  "uid": "{latestUserUID}", 
  "firstName": "{latestFirstName}",
  "lastName": "{latestLastName}",
  "email": "{latestEmail}",
  "password": "{latestPassword}",
  "gender": "{latestGender}",
  "created_at": "{latestCreatedAt}"
}
```

**Note:** Execute `python db_query_api.py` to retrieve actual latest user credentials before test execution.

## Implementation Workflow

### 1. Pre-Test Setup
1. Execute database query to get latest user credentials
2. Replace placeholder values in prompts with actual test data
3. Review appropriate context file for testing scenario
4. Ensure test environment prerequisites are met

### 2. Test Execution  
1. Reference context file for scenario understanding
2. Execute prompt instructions step-by-step
3. Validate expected results against actual outcomes
4. Document any deviations or issues encountered

### 3. Post-Test Validation
1. Execute relevant validation prompts
2. Verify database state matches expected changes
3. Confirm UI state reflects completed actions
4. Update test data for subsequent test runs

## Cross-Reference Matrix

| Functional Area | Context File | Prompt File | Key Test Scenarios | Validation Prompts |
|----------------|--------------|-------------|-------------------|-------------------|
| User Registration | user_management_context.md | registration_prompts.md | Valid/invalid registration, field validation | VALIDATE_001_User_Registration_Database |
| User Authentication | user_management_context.md | login_prompts.md | Login/logout, session management | VALIDATE_002_Login_Session_Validation |
| Product Discovery | product_management_context.md | product_search_prompts.md | Search, browse, filter products | VALIDATE_006_Search_Results_Accuracy |
| Product Information | product_management_context.md | product_details_prompts.md | Product details, specifications | VALIDATE_005_Product_Data_Consistency |
| Shopping Cart | shopping_cart_context.md | shopping_cart_prompts.md | Add/remove items, quantity updates | VALIDATE_003_Cart_Data_Persistence |
| Checkout Process | checkout_context.md | checkout_prompts.md | Complete purchase flow | VALIDATE_004_Order_Data_Integrity |
| User Profile | user_management_context.md | user_profile_prompts.md | Profile management, order history | VALIDATE_002_Login_Session_Validation |
| Price Calculations | general_testing_context.md | validation_prompts.md | Cart/order total accuracy | VALIDATE_007_Price_Calculation_Accuracy |

## Test Scenario Coverage

### Positive Test Scenarios
- ✅ Valid user registration (male/female)
- ✅ Successful login with valid credentials  
- ✅ Product search and browsing
- ✅ Add items to cart and checkout
- ✅ User profile management
- ✅ Order completion and confirmation

### Negative Test Scenarios  
- ❌ Invalid registration data validation
- ❌ Login failures with incorrect credentials
- ❌ Empty search results handling
- ❌ Checkout error scenarios
- ❌ Form validation testing

### Edge Case Scenarios
- 🔄 Cart persistence across sessions
- 🔄 Session timeout behavior
- 🔄 Payment method validation
- 🔄 Address format validation
- 🔄 Price calculation accuracy

## Quality Assurance Notes

### Database Integration
- All user registration tests include database validation
- Cart and order tests verify data persistence
- Price calculations validated across UI and database

### Browser Compatibility
- Prompts designed for cross-browser testing
- Responsive design validation included
- Mobile-friendly test scenarios covered

### Security Testing
- Password encryption validation
- Session security verification
- Input sanitization testing

### Performance Considerations
- Page load time validation
- Search response time testing
- Checkout process efficiency

## Maintenance Guidelines

### Regular Updates
1. **Monthly Review**: Update test data and scenarios based on application changes
2. **Quarterly Assessment**: Review prompt effectiveness and add new scenarios
3. **Version Control**: Track changes to prompts and contexts in repository

### Extension Points
1. **New Features**: Add corresponding contexts and prompts for new functionality
2. **API Testing**: Extend validation prompts for API endpoint testing
3. **Mobile Testing**: Add mobile-specific contexts and prompts

### Best Practices
- Keep prompts focused on single functional areas
- Maintain consistent formatting and structure
- Include comprehensive validation steps
- Document assumptions and prerequisites clearly
- Update placeholder examples regularly

---

**Last Updated:** February 12, 2026  
**Version:** 1.0  
**Maintainer:** Test Automation Framework Team