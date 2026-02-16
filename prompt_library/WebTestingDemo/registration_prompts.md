# Registration Prompts Library

## Basic Registration Prompts

### Prompt: REG_001_Valid_Male_Registration
```
Navigate to the registration page and complete a valid male user registration using the following test data:
- Gender: Male
- First Name: {firstName}
- Last Name: {lastName}
- Email: {email}
- Password: {password}
- Confirm Password: {password}

**Steps:**
1. Navigate to registration page (https://demowebshop.tricentis.com/register)
2. Select Male gender radio button
3. Fill in first name field with: {firstName}
4. Fill in last name field with: {lastName}
5. Enter unique email address: {email}
6. Enter secure password: {password}
7. Confirm password: {password}
8. Click Register button
9. Wait for page to load and verify success

**Expected Results:**
- Registration completes successfully
- User redirected to confirmation page or login page
- Success message displayed
- User data saved to database
- Password encrypted in database
- Unique UID generated
```

### Prompt: REG_002_Valid_Female_Registration
```
Navigate to the registration page and complete a valid female user registration using the following test data:
- Gender: Female
- First Name: {firstName}
- Last Name: {lastName}
- Email: {email}
- Password: {password}
- Confirm Password: {password}

**Steps:**
1. Navigate to registration page (https://demowebshop.tricentis.com/register)
2. Select Female gender radio button
3. Fill in first name field with: {firstName}
4. Fill in last name field with: {lastName}
5. Enter unique email address: {email}
6. Enter secure password: {password}
7. Confirm password: {password}
8. Click Register button
9. Verify successful registration

**Expected Results:**
- Successful registration with female gender stored correctly
- All validation passes
- Database entry created with correct gender
- User redirected appropriately
```

### Prompt: REG_003_Duplicate_Email_Validation
```
Test duplicate email validation by attempting to register with an existing email address.

**Test Data:**
- Email: {existingEmail} (use existing user email)
- Other fields: Valid data

**Steps:**
1. Navigate to registration page
2. Fill in all fields with valid data
3. Use existing email address: {existingEmail}
4. Attempt to submit registration form
5. Verify error handling

**Expected Results:**
- Registration should fail
- Error message displayed for duplicate email
- User not created in database
- Form remains on registration page with error message
```

### Prompt: REG_004_Password_Mismatch_Validation
```
Test password confirmation validation with mismatched passwords.

**Test Data:**
- Password: {password}
- Confirm Password: {password}123 (intentionally different)

**Steps:**
1. Navigate to registration page
2. Fill in all fields with valid data
3. Enter password: {password}
4. Enter different confirm password: {password}123
5. Attempt to submit form
6. Verify validation error

**Expected Results:**
- Registration should fail
- Password mismatch error displayed
- Form validation prevents submission
- User remains on registration page
```

### Prompt: REG_005_Required_Field_Validation
```
Test required field validation by leaving mandatory fields empty.

**Test Scenarios:**
- Empty first name
- Empty last name
- Empty email
- Empty password

**Steps:**
1. Navigate to registration page
2. Leave first name field empty
3. Fill other required fields
4. Attempt submission
5. Verify validation error
6. Repeat for each required field

**Expected Results:**
- Form validation prevents submission
- Required field error messages displayed
- User guided to complete missing fields
- Registration not processed until all fields completed
```