# Checkout Prompts Library

## Checkout Process Prompts

### Prompt: CHECKOUT_001_Guest_Checkout_Flow
```
Test complete guest checkout process without user account.

**Prerequisites:**
- Items added to shopping cart
- Not logged into any user account

**Test Data:**
- First Name: {firstName}
- Last Name: {lastName}
- Email: {email}
- Address: {address}
- City: {city}
- ZIP: {zipCode}
- Country: {country}
- Phone: {phone}

**Steps:**
1. Navigate to cart page with items
2. Click "Checkout" button
3. Select "Checkout as Guest" option (if available)
4. Fill in billing information:
   - First Name: {firstName}
   - Last Name: {lastName}
   - Email: {email}
   - Address: {address}
   - City: {city}
   - ZIP: {zipCode}
   - Country: {country}
   - Phone: {phone}
5. Continue to shipping information
6. Select shipping method
7. Continue to payment method
8. Select payment method and fill details (demo mode)
9. Review order summary
10. Place order

**Expected Results:**
- Guest checkout option available
- All form fields accept valid data
- Shipping options display correctly
- Payment methods available
- Order summary accurate
- Order confirmation received
- Guest order processed successfully
```

### Prompt: CHECKOUT_002_Registered_User_Checkout
```
Test checkout process with logged-in registered user.

**Prerequisites:**
- User logged in with credentials: {email}, {password}
- Items added to shopping cart

**Steps:**
1. Ensure user is logged in
2. Navigate to cart page with items
3. Click "Checkout" button
4. Verify user information pre-populated
5. Review/confirm shipping address
6. Select shipping method from available options
7. Review/confirm billing information
8. Select payment method
9. Review order summary
10. Place order

**Expected Results:**
- Checkout recognizes logged-in user
- User information auto-populated correctly
- Saved addresses available (if any)
- Shipping methods display with costs
- Payment options available
- Order summary matches cart contents
- Order processes successfully
- Order confirmation displayed
- Order saved to user account history
```

### Prompt: CHECKOUT_003_Shipping_Method_Selection
```
Test different shipping method selection and cost calculation.

**Available Shipping Methods:**
- Ground (Standard)
- Next Day Air (if available)
- 2nd Day Air (if available)

**Steps:**
1. Proceed through checkout to shipping method selection
2. Review all available shipping options
3. Note shipping costs for each method
4. Select Ground shipping method
5. Verify shipping cost calculation
6. Change to Next Day Air (if available)
7. Verify cost update
8. Complete checkout with selected method

**Expected Results:**
- All shipping methods display clearly
- Shipping costs shown for each option
- Order total updates when shipping method changes
- Selected shipping method highlighted
- Delivery timeframes shown (if available)
- Shipping cost correctly added to order total
```

### Prompt: CHECKOUT_004_Payment_Method_Testing
```
Test payment method selection and form validation (demo mode).

**Available Payment Methods:**
- Credit Card (demo)
- Check/Money Order
- Purchase Order

**Steps:**
1. Proceed through checkout to payment section
2. Select "Credit Card" payment method
3. Fill in demo credit card information:
   - Card Number: 4111111111111111 (demo Visa)
   - Expiry: 12/26
   - CVV: 123
   - Cardholder Name: {firstName} {lastName}
4. Test other payment methods if available
5. Complete payment selection
6. Proceed to order review

**Expected Results:**
- Payment method options clearly displayed
- Credit card form fields function properly
- Form validation works for payment fields
- Demo payment processing works
- Payment method appears in order summary
- Other payment options function correctly
```

### Prompt: CHECKOUT_005_Order_Review_Validation
```
Test order review page accuracy before final submission.

**Steps:**
1. Proceed through checkout to final order review
2. Verify all order details are accurate:
   - Items in order match cart contents
   - Quantities correct for each item
   - Individual prices match product pages
   - Subtotal calculation correct
   - Shipping cost included correctly
   - Tax calculations accurate (if applicable)
   - Total amount correct
3. Verify shipping address details
4. Verify billing information
5. Verify payment method selection
6. Review terms and conditions (if required)
7. Place final order

**Expected Results:**
- Order review page displays all details clearly
- All order information matches previous selections
- Calculations are accurate and complete
- Address information correct and complete
- Payment method confirmed correctly
- Order placement button clearly labeled
- Terms acceptance process clear (if required)
```

### Prompt: CHECKOUT_006_Order_Confirmation
```
Test order confirmation page and completion process.

**Steps:**
1. Complete entire checkout process
2. Submit final order
3. Wait for order confirmation page to load
4. Verify order confirmation details:
   - Order number generated
   - Order summary displayed
   - Customer information confirmed
   - Shipping details confirmed
   - Payment confirmation
5. Check for next steps information
6. Test any additional features (print receipt, email confirmation)

**Expected Results:**
- Order confirmation page loads successfully
- Unique order number generated and displayed
- All order details summarized correctly
- Confirmation includes customer service information
- Next steps clearly communicated
- Professional appearance and messaging
- Email confirmation sent (if applicable)
```

### Prompt: CHECKOUT_007_Checkout_Error_Handling
```
Test checkout error scenarios and validation.

**Error Scenarios to Test:**
- Invalid payment information
- Empty required fields
- Invalid shipping address
- Network interruption during checkout

**Steps:**
1. Proceed through checkout normally
2. Test invalid credit card number (demo): 1234567890123456
3. Verify error handling and messaging
4. Test empty required fields submission
5. Test invalid address format
6. Verify user guidance for error correction

**Expected Results:**
- Invalid payment details rejected with clear error message
- Required field validation prevents progression
- Address validation provides helpful feedback
- Error messages are clear and actionable
- User can correct errors and continue
- Checkout process resilient to user errors
```