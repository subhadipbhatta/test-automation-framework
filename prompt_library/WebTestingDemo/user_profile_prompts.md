# User Profile Prompts Library

## Profile Management Prompts

### Prompt: PROFILE_001_View_User_Profile
```
Test accessing and viewing user profile information.

**Prerequisites:**
- User logged in with credentials: {email}, {password}

**Steps:**
1. Ensure user is successfully logged in
2. Navigate to user account section (usually in header menu)
3. Click on "My Account" or similar profile link
4. Review displayed user information on profile page
5. Validate profile data accuracy against registration data
6. Check available profile management options

**Profile Information to Validate:**
- First Name: {firstName}
- Last Name: {lastName}
- Email: {email}
- Gender: {gender}
- Account creation date (if displayed)
- UID/User ID (if visible to user)

**Expected Results:**
- Profile page loads correctly and completely
- User information displayed accurately
- Profile data matches original registration data
- Profile navigation menu available and functional
- User can access profile management features
- Professional page layout and design
```

### Prompt: PROFILE_002_Update_Profile_Information
```
Test updating user profile information and saving changes.

**Information to Update:**
- First Name: {newFirstName}
- Last Name: {newLastName}
- Email: {newEmail} (if changeable)
- Phone: {phoneNumber} (if field available)

**Steps:**
1. Navigate to profile/account settings page
2. Locate "Edit Profile" or similar option
3. Click to enter edit mode
4. Update first name to: {newFirstName}
5. Update last name to: {newLastName}
6. Update email to: {newEmail} (if allowed)
7. Add phone number: {phoneNumber} (if field exists)
8. Save/update changes
9. Verify changes are saved and displayed
10. Refresh page to confirm persistence

**Expected Results:**
- Profile edit functionality accessible
- Form fields pre-populated with current information
- Changes save successfully
- Updated information displayed immediately
- Changes persist after page refresh
- Database updated with new information
- Success confirmation message displayed
```

### Prompt: PROFILE_003_Change_Password
```
Test password change functionality in user profile.

**Test Data:**
- Current Password: {password}
- New Password: {newPassword}
- Confirm New Password: {newPassword}

**Steps:**
1. Navigate to user profile/account settings
2. Look for "Change Password" or "Security" section
3. Enter current password: {password}
4. Enter new password: {newPassword}
5. Confirm new password: {newPassword}
6. Submit password change
7. Verify success confirmation
8. Log out and test login with new password
9. Verify old password no longer works

**Expected Results:**
- Password change form accessible from profile
- Current password validation required
- New password meets security requirements
- Password confirmation validates match
- Change processes successfully
- Success message displayed
- New password works for login
- Old password rejected after change
```

### Prompt: PROFILE_004_Order_History_View
```
Test viewing order history in user profile.

**Prerequisites:**
- User with at least one completed order
- User logged in

**Steps:**
1. Navigate to user profile/account area
2. Look for "Order History" or "My Orders" section
3. Click to view order history
4. Review displayed orders list
5. Click on specific order for detailed view
6. Validate order information accuracy
7. Test navigation between orders

**Order Details to Validate:**
- Order number/ID
- Order date
- Items ordered
- Order total
- Shipping address
- Order status

**Expected Results:**
- Order history page accessible from profile
- Orders displayed in chronological order (newest first)
- Order list shows key information clearly
- Individual order details accessible
- Order information accurate and complete
- Professional layout and navigation
- Order status information clear
```

### Prompt: PROFILE_005_Address_Management
```
Test address book/management functionality in user profile.

**Test Addresses:**
- Shipping Address: {shippingAddress}
- Billing Address: {billingAddress}

**Steps:**
1. Navigate to user profile/account settings
2. Look for "Address Book" or "Manage Addresses"
3. View existing addresses (if any)
4. Add new shipping address:
   - Name: {firstName} {lastName}
   - Address: {shippingAddress}
   - City: {city}
   - ZIP: {zipCode}
   - Country: {country}
5. Add billing address (if different)
6. Set default addresses if option available
7. Edit an existing address
8. Test address deletion (if allowed)

**Expected Results:**
- Address management section accessible
- Can add multiple addresses successfully
- Address forms validate input properly
- Can set default shipping/billing addresses
- Address editing functions correctly
- Address deletion works (with confirmation)
- Addresses available during checkout
```

### Prompt: PROFILE_006_Account_Security_Settings
```
Test account security and privacy settings in user profile.

**Security Features to Test:**
- Password change (covered in PROFILE_003)
- Email change/verification
- Account privacy settings
- Security questions (if available)

**Steps:**
1. Navigate to account security/privacy section
2. Review available security options
3. Test email change process (if allowed)
4. Review privacy settings options
5. Test security question setup (if available)
6. Verify security change confirmations

**Expected Results:**
- Security section clearly organized
- Email change requires verification
- Privacy settings clearly explained
- Security changes require current password
- Confirmation emails sent for security changes
- All security features function properly
```

### Prompt: PROFILE_007_Account_Deletion_Deactivation
```
Test account deletion or deactivation options if available.

**Steps:**
1. Navigate to account settings
2. Look for "Delete Account" or "Deactivate Account" options
3. Review account deletion process
4. Test deletion confirmation requirements
5. Verify warnings and information provided
6. Test cancellation of deletion process

**Expected Results:**
- Account deletion option available (if feature exists)
- Clear warnings about deletion consequences
- Confirmation process requires multiple steps
- User data deletion policy explained
- Option to cancel deletion process
- Deletion process secure and confirmed
```