# Login Prompts Library

## Authentication Prompts

### Prompt: LOGIN_001_Valid_Credentials
```
Test successful login using valid registered user credentials.

**Test Data:**
- Email: {email}
- Password: {password}

**Steps:**
1. Navigate to login page (https://demowebshop.tricentis.com/login)
2. Enter email address: {email}
3. Enter password: {password}
4. Click Login button
5. Wait for page to load
6. Verify successful authentication

**Expected Results:**
- Successful authentication
- Redirect to user dashboard or home page
- User session established
- User menu/profile accessible
- Login link changes to user account link
```

### Prompt: LOGIN_002_Invalid_Password
```
Test login failure with incorrect password.

**Test Data:**
- Email: {email} (valid existing email)
- Password: "InvalidPassword123!" (incorrect password)

**Steps:**
1. Navigate to login page
2. Enter valid email: {email}
3. Enter incorrect password: InvalidPassword123!
4. Click Login button
5. Verify login failure handling

**Expected Results:**
- Login should fail
- Error message displayed (e.g., "Login was unsuccessful")
- User remains on login page
- No session established
- Login form remains accessible
```

### Prompt: LOGIN_003_Nonexistent_User
```
Test login attempt with non-existent user credentials.

**Test Data:**
- Email: "nonexistent.user@testmail.com"
- Password: "AnyPassword123!"

**Steps:**
1. Navigate to login page
2. Enter non-existent email: nonexistent.user@testmail.com
3. Enter any password: AnyPassword123!
4. Click Login button
5. Verify error handling

**Expected Results:**
- Login should fail
- Appropriate error message displayed
- No session created
- User remains on login page
```

### Prompt: LOGIN_004_Empty_Credentials
```
Test login form validation with empty credentials.

**Test Scenarios:**
- Empty email and password
- Empty email only
- Empty password only

**Steps:**
1. Navigate to login page
2. Leave email field empty
3. Leave password field empty
4. Click Login button
5. Verify validation errors
6. Test each empty field scenario

**Expected Results:**
- Form validation prevents submission
- Required field validation messages displayed
- Login not attempted with empty fields
- User guided to complete required fields
```

### Prompt: LOGIN_005_Session_Persistence
```
Test user session persistence after successful login.

**Prerequisites:**
- Valid user credentials: {email}, {password}

**Steps:**
1. Login with valid credentials
2. Navigate to different pages within the site
3. Check user session maintenance
4. Verify authenticated features remain accessible
5. Test session across page refreshes

**Expected Results:**
- Session maintained across page navigation
- User remains authenticated
- User-specific features accessible
- Session persists through page refreshes
- User menu shows logged-in state
```

### Prompt: LOGIN_006_Logout_Functionality
```
Test user logout functionality and session termination.

**Prerequisites:**
- User successfully logged in

**Steps:**
1. Ensure user is logged in
2. Locate logout link/button
3. Click logout
4. Verify session termination
5. Attempt to access authenticated features
6. Verify redirect to login page

**Expected Results:**
- User successfully logged out
- Session terminated properly
- Redirect to home page or login page
- Authenticated features no longer accessible
- User menu shows logged-out state
```