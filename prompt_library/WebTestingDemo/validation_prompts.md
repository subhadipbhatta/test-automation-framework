# Validation Prompts Library

## Database Validation Prompts

### Prompt: VALIDATE_001_User_Registration_Database
```
Validate that user registration data is correctly stored in database.

**Prerequisites:**
- User registration completed successfully
- Database connection available
- User credentials: {email}, {password}

**Database Validation Steps:**
1. Connect to database using intelligent database assistant
2. Query database for user by email: {email}
3. Verify user record exists in RegistrationInfo table
4. Validate stored data matches registration input:
   - First Name: {firstName}
   - Last Name: {lastName}
   - Email: {email}
   - Gender: {gender}
5. Verify password is encrypted (not stored as plain text)
6. Verify unique UID assigned to user
7. Check created_at timestamp reflects registration time

**Database Query Example:**
```sql
SELECT * FROM RegistrationInfo WHERE email = '{email}'
```

**Expected Results:**
- User record found in database
- All registration fields match input data exactly
- Password field contains encrypted value, not plain text
- Unique UID generated and stored
- Timestamp shows recent registration time
- No duplicate records for same email
```

### Prompt: VALIDATE_002_Login_Session_Validation
```
Validate user session establishment and maintenance after successful login.

**Prerequisites:**
- User successfully logged in with: {email}, {password}

**Session Validation Steps:**
1. Verify user session is established after login
2. Check user authentication status in browser
3. Navigate to different pages and verify session persistence
4. Check user-specific content display (user menu, account links)
5. Verify protected features are accessible
6. Test session timeout behavior (if applicable)
7. Validate logout functionality terminates session

**Session Indicators to Check:**
- User menu shows logged-in state
- "Login" link changes to user account link
- Cart persistence for logged-in user
- Access to profile/account features
- Checkout shows user information

**Expected Results:**
- Session established immediately after login
- Session maintained during site navigation
- User-specific features accessible
- Session persists appropriate duration
- Session terminates properly on logout
```

### Prompt: VALIDATE_003_Cart_Data_Persistence
```
Validate shopping cart data accuracy and persistence.

**Prerequisites:**
- Items added to shopping cart
- Cart contains multiple items with different quantities

**Cart Validation Steps:**
1. Add multiple items to cart with varying quantities
2. Navigate away from cart page to other site areas
3. Return to cart page and verify all items present
4. Validate item details accuracy:
   - Product names match selected products
   - Quantities match user selections
   - Individual prices match product page prices
   - Line totals calculated correctly (price × quantity)
5. Verify cart subtotal calculation
6. Test cart persistence across browser refresh
7. For logged-in users: test cart persistence across sessions

**Cart Data to Validate:**
- Item names and descriptions
- Individual product prices
- Selected quantities
- Line item totals
- Cart subtotal
- Item count in cart badge/counter

**Expected Results:**
- All cart items persist during navigation
- Item details remain accurate
- Quantities and prices correct
- Calculations accurate at all levels
- Cart state maintained across page refreshes
- Cart persistence behavior matches user type (guest vs logged-in)
```

### Prompt: VALIDATE_004_Order_Data_Integrity
```
Validate order data integrity after successful checkout completion.

**Prerequisites:**
- Order successfully placed through checkout
- Order confirmation received with order number

**Order Validation Steps:**
1. Record order details from confirmation page:
   - Order number: {orderNumber}
   - Order total: {orderTotal}
   - Items ordered: {orderedItems}
   - Shipping address: {shippingAddress}
2. Validate order appears in user profile (if logged in)
3. Check order details match checkout selections
4. Verify order calculations accuracy
5. Validate shipping and billing information stored correctly

**Order Data to Validate:**
- Order number uniqueness
- Item details match cart at checkout
- Quantities and prices accurate
- Shipping address correct
- Payment method recorded
- Order status appropriate
- Timestamps accurate

**Expected Results:**
- Order data stored completely and accurately
- Order number is unique and trackable
- All order details match checkout submissions
- Order appears in user account (if registered user)
- Order calculations correct including taxes and shipping
- Order status reflects current state
```

### Prompt: VALIDATE_005_Product_Data_Consistency
```
Validate product information consistency across different page views.

**Product to Validate:** {productName}

**Consistency Validation Steps:**
1. View product on category/search results page
2. Record displayed information:
   - Product name
   - Price
   - Image
   - Brief description (if shown)
3. Navigate to product detail page
4. Compare all information elements:
   - Product title matches exactly
   - Price identical across views
   - Image consistency
   - Description consistency
5. Add product to cart and verify cart shows same information
6. Proceed to checkout and verify order review matches

**Data Points to Compare:**
- Product names/titles
- Pricing information
- Product images
- Product descriptions
- Stock availability
- Product specifications

**Expected Results:**
- Product information identical across all views
- No discrepancies in names, prices, or descriptions
- Images consistent and relevant
- Product data maintains integrity through cart and checkout
- No data corruption or inconsistencies found
```

### Prompt: VALIDATE_006_Search_Results_Accuracy
```
Validate search functionality returns accurate and relevant results.

**Search Terms to Test:**
- "computer" (should return computer products)
- "book" (should return book products)
- "jewelry" (should return jewelry items)

**Search Validation Steps:**
1. Perform search for: {searchTerm}
2. Review all returned results
3. Verify result relevance:
   - Product titles contain or relate to search term
   - Product descriptions match search context
   - Products from appropriate categories
4. Check result count accuracy
5. Test pagination if multiple pages of results
6. Verify "no results" behavior for invalid search terms

**Search Quality Metrics:**
- Result relevance to search term
- Appropriate product categories returned
- Search result count accuracy
- Search performance and speed
- Handling of typos or similar terms

**Expected Results:**
- Search returns relevant products only
- Results match search term context
- Search count reflects actual results shown
- Pagination works correctly for large result sets
- No irrelevant products in search results
- Search handles edge cases appropriately
```

### Prompt: VALIDATE_007_Price_Calculation_Accuracy
```
Validate all price calculations throughout the shopping and checkout process.

**Calculation Validation Scenarios:**
- Individual product pricing
- Cart subtotal calculations
- Shipping cost additions
- Tax calculations (if applicable)
- Final order total

**Price Validation Steps:**
1. Select products with different price points
2. Add multiple quantities to cart
3. Verify line item calculations (price × quantity)
4. Validate cart subtotal (sum of all line items)
5. Proceed through checkout and verify shipping costs
6. Check tax calculations if applicable
7. Validate final order total includes all components
8. Compare final total across different checkout steps

**Calculations to Verify:**
- Product price × quantity = line item total
- Sum of line items = cart subtotal
- Subtotal + shipping + taxes = order total
- Currency formatting consistency
- Discount applications (if any)

**Expected Results:**
- All calculations mathematically correct
- No rounding errors or calculation mistakes
- Consistent price display formatting
- All cost components clearly itemized
- Final totals match sum of individual components
- Price changes reflect immediately in calculations
```