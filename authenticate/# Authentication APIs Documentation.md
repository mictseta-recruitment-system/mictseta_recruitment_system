# Authentication APIs Documentation

This document provides detailed information on how to use the authentication APIs provided by the system. These APIs facilitate user sign-in, sign-up, password reset, and related functionalities.

## 1. Signing In

### Endpoint
`POST /sign_in`

### Description

Allows existing users to sign in to their accounts.

### Request Body
```json
{
  "email": "user@example.com",
  "password": "password"
}
```
### Response

   - Success (200 OK)

```json

{
  "message": "Welcome back <username>",
  "status": "success"
}
```
   - Error (400 Bad Request)

```json

{
  "errors": {
    "password": ["Password is incorrect"]
  },
  "status": "error"
}
```
# 2. Signing Up

### Endpoint

`POST /auth/sign_up`

### Description

Allows new users to create an account.

#### Request Body

```json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "idnumber": "1234567890123",
  "password": "password",
  "password2": "password"
}
```
#### Response

   - Success (201 Created)

```json

{
  "message": "User profile for <username> is created successfully",
  "status": "success"
}
```
   - Error (400 Bad Request)

```json

{
  "errors": {
    "password": ["Password no match"]
  },
  "status": "error"
}
```
# 3. Logging Out

### Endpoint

`POST /auth/log_out`

### Description

- Logs out the currently authenticated user.
Response

- Redirects to the authentication page.

# 4. Reset Password Link

### Endpoint

`POST /auth/reset_password_link`

### Description

Generates a reset password link for the user.

#### Request Body

```json

{
  "email": "user@example.com"
}
```
#### Response

  -  Success (201 Created)

```json

{
  "message": "Link generated successfully",
  "link": "http://127.0.0.1:8000/auth/reset_password/<uid>/<token>/",
  "status": "success"
}
```
  - Error (404 Not Found)

```json

{
  "errors": {
    "email": ["Not Found"]
  },
  "status": "error"
}
```
# 5. Reset Password

### Endpoint

`POST /reset_password/<uid>/<token>/`

### Description

Resets the user's password using the provided token.

#### Request Body

```json

{
  "password": "newpassword",
  "re-password": "newpassword"
}
```
#### Response

- Redirects to the password reset completion page.