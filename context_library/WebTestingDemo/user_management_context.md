# User Management Context Library

## Registration Context

### Fresh Registration Flow Context
```
You are testing user registration on a demo e-commerce website (https://demowebshop.tricentis.com/).

**Scenario Context:**
- Testing new user registration functionality
- Validating form fields and validation rules
- Ensuring successful account creation and database storage

**Test Data Requirements:**
- Valid email format (unique per test run)
- Strong password with special characters
- Gender selection (Male/Female)
- First name and last name
- Confirm password matching

**Success Criteria:**
- User redirected to success page or login page
- User data stored in database with encrypted password
- Unique UID generated
- No validation errors displayed
```

### Login Context
```
You are testing user login functionality using previously registered credentials.

**Scenario Context:**
- Testing existing user authentication
- Validating login form behavior
- Ensuring proper session management

**Prerequisites:**
- Valid registered user credentials available
- Database contains user record
- Website is accessible

**Success Criteria:**
- Successful authentication and redirect
- User session established
- Access to authenticated features
```

## User Profile Management Context

### Profile Access Context
```
You are testing user profile access and management features.

**Scenario Context:**
- Testing authenticated user profile functionality
- Validating profile information display
- Testing profile update capabilities

**Prerequisites:**
- User successfully logged in
- User session active
- Profile features accessible

**Profile Features to Test:**
- View personal information
- Update profile details
- Change password
- View order history
- Manage addresses
```

## Session Management Context

### Session Persistence Context
```
You are testing user session management and persistence across the application.

**Scenario Context:**
- Testing session establishment after login
- Validating session persistence across pages
- Testing session timeout behavior
- Validating logout functionality

**Session Behaviors:**
- Session creation on login
- Session maintenance during navigation
- Session security and validation
- Proper session termination on logout
```