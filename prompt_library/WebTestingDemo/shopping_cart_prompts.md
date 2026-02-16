# Shopping Cart Prompts Library

## Cart Management Prompts

### Prompt: CART_001_Add_Single_Item
```
Test adding a single item to shopping cart from product detail page.

**Test Data:**
- Product: {productName}
- Quantity: 1

**Steps:**
1. Navigate to product detail page: {productName}
2. Verify product information is displayed
3. Confirm quantity is set to 1
4. Click "Add to Cart" button
5. Verify cart update notification appears
6. Check cart counter/badge updates
7. Navigate to cart page
8. Validate item appears in cart correctly

**Expected Results:**
- Item successfully added to cart
- Cart counter updates to show 1 item
- Cart notification confirms addition
- Product appears in cart with correct:
  - Product name
  - Price
  - Quantity (1)
  - Subtotal calculation
- Cart page accessible and functional
```

### Prompt: CART_002_Add_Multiple_Different_Items
```
Test adding multiple different items to shopping cart.

**Items to Add:**
- Product 1: {product1}
- Product 2: {product2}
- Product 3: {product3}

**Steps:**
1. Add first product to cart: {product1}
2. Continue shopping (navigate away from cart)
3. Add second product to cart: {product2}
4. Continue shopping
5. Add third product to cart: {product3}
6. Navigate to cart page
7. Validate all three items are present
8. Verify cart calculations

**Expected Results:**
- All three items appear in cart
- Each item shows correct product details
- Individual quantities correct (1 each)
- Individual prices displayed correctly
- Cart subtotal calculated properly
- Cart counter shows total item count (3)
```

### Prompt: CART_003_Update_Item_Quantities
```
Test updating item quantities in shopping cart.

**Test Scenario:**
- Start with 1 item in cart
- Update quantity to 3
- Update quantity to 5
- Update quantity back to 2

**Steps:**
1. Add one item to cart with default quantity (1)
2. Navigate to cart page
3. Locate quantity update controls for the item
4. Change quantity from 1 to 3
5. Apply/update quantity change
6. Verify quantity and price recalculation
7. Change quantity to 5, then to 2
8. Verify each update works correctly

**Expected Results:**
- Quantity updates successfully each time
- Item price multiplied correctly by new quantity
- Cart subtotal recalculated automatically
- Total cart amount updates correctly
- Quantity controls are user-friendly
```

### Prompt: CART_004_Remove_Items_From_Cart
```
Test removing items from shopping cart.

**Test Setup:**
- Add 3 different items to cart
- Remove items one by one

**Steps:**
1. Add multiple items to cart (3 items)
2. Navigate to cart page
3. Locate remove/delete option for first item
4. Remove first item from cart
5. Verify item is removed and cart recalculates
6. Remove second item
7. Verify cart updates again
8. Remove final item
9. Verify empty cart state

**Expected Results:**
- Each item can be removed successfully
- Cart recalculates after each removal
- Remaining items unaffected by removals
- Cart counter updates with each removal
- Empty cart displays appropriate message
- Remove action is clear and intuitive
```

### Prompt: CART_005_Cart_Persistence
```
Test shopping cart persistence across sessions and navigation.

**Test Scenarios:**
- Cart persistence during site navigation
- Cart persistence across browser sessions (if logged in)

**Steps:**
1. Add items to cart
2. Navigate to different pages on the site
3. Return to cart page and verify items remain
4. Close browser and reopen (if testing session persistence)
5. Navigate back to cart
6. Verify cart contents maintained

**Expected Results:**
- Cart contents maintained during site navigation
- Items remain in cart across page visits
- Cart counter consistently shows correct count
- For logged-in users: cart may persist across sessions
- For guest users: cart maintained during current session
```

### Prompt: CART_006_Empty_Cart_State
```
Test empty cart page display and functionality.

**Steps:**
1. Ensure cart is completely empty (remove all items)
2. Navigate to cart page
3. Verify empty cart message and appearance
4. Check for continue shopping options
5. Test navigation from empty cart page

**Expected Results:**
- Empty cart message clearly displayed
- Professional appearance for empty state
- Clear options to continue shopping
- Links to product categories or homepage
- No calculation errors or broken elements
- Encouraging message to browse products
```

### Prompt: CART_007_Cart_Calculations_Validation
```
Test all cart calculation accuracy including taxes and totals.

**Test Setup:**
- Add multiple items with different prices
- Verify all calculations

**Steps:**
1. Add items with various prices to cart
2. Navigate to cart page
3. Verify individual item calculations (price × quantity)
4. Verify subtotal calculation (sum of all items)
5. Check tax calculations (if applicable)
6. Verify final total amount
7. Test calculations after quantity updates

**Expected Results:**
- Individual item totals calculated correctly
- Subtotal matches sum of all item totals
- Tax calculations accurate (if applicable)
- Final total includes all applicable charges
- All monetary amounts formatted consistently
- Calculations update correctly with quantity changes
```