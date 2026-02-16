# Checkout Context Library

## Checkout Process Context

### Multi-Step Checkout Context
```
You are testing the complete checkout process from cart review to order completion.

**Scenario Context:**
- Testing multi-step checkout process
- Validating shipping and billing information
- Testing payment processing (demo mode)
- Verifying order confirmation

**Checkout Steps:**
1. Cart review and item verification
2. Shipping address entry
3. Billing information
4. Payment method selection
5. Order review and confirmation
6. Order placement and confirmation

**Payment Methods Available:**
- Credit Card (demo)
- Check/Money Order
- Purchase Order
```

### Guest vs Registered Checkout Context
```
You are testing checkout functionality for different user types.

**Scenario Context:**
- Testing guest checkout process
- Testing registered user checkout
- Validating user-specific checkout features

**User Types:**
- Guest users (no account)
- Registered users (logged in)
- Returning customers

**Checkout Variations:**
- Guest checkout flow
- Registered user with saved addresses
- First-time registered user checkout
```

## Shipping Context

### Shipping Options Context
```
You are testing shipping method selection and calculation.

**Scenario Context:**
- Testing available shipping methods
- Validating shipping cost calculations
- Testing shipping address validation

**Shipping Methods:**
- Standard Ground
- Express shipping (if available)
- Overnight delivery (if available)
- International shipping (if available)

**Shipping Validations:**
- Address format validation
- Shipping cost calculations
- Delivery time estimates
- Shipping restrictions
```

## Payment Context

### Payment Processing Context
```
You are testing payment method selection and processing (demo mode).

**Scenario Context:**
- Testing payment form functionality
- Validating payment method selection
- Testing demo payment processing

**Payment Methods:**
- Credit Card (demo transactions)
- Debit Card (demo transactions)
- Check/Money Order
- Purchase Order
- Gift Cards (if available)

**Payment Validations:**
- Payment form validation
- Payment method selection
- Demo transaction processing
- Payment confirmation
```