# 📘 Accounts App – README

This **Accounts** app handles user authentication and profile management for my social media API. It is built with **Django REST Framework** and uses **Token Authentication** for secure access to protected endpoints. The database used is the default **SQLite** for development.

---

## 🚀 Features

### **1. User Registration**

* Implemented using `CreateAPIView`
* Validates incoming user data
* Creates a new user account
* Endpoint:
  **POST** `/account/register/`

---

### **2. User Login**

* Custom login flow using `APIView`

* Uses a dedicated LoginSerializer for username/password validation

* Generates or retrieves an existing token using:

  ```python
  Token.objects.get_or_create(user=user)
  ```

* Returns the token so the frontend can authenticate future requests

* Endpoint:
  **POST** `/account/login/`

---

### **3. User Profile**

* Implemented using `RetrieveUpdateAPIView`
* Allows the user to:

  * Fetch their profile
  * Update profile details
* Authentication required using token in headers
* Endpoint:
  **GET /account/profile/**
  **PUT /account/profile/** (or PATCH)

---

## 🔐 Authentication

This app uses **DRF Token Authentication**.

Clients must send the token from login in the request header:

```
Authorization: Token <your_token_here>
```

---

## 🗂️ Tech Stack

* **Django**
* **Django REST Framework**
* **Token Authentication**
* **SQLite** (default development database)

---

## 📦 Directory Overview

```
accounts/
│
├── serializers.py      # Registration + Login serializers
├── views.py            # Register, Login, Profile views
├── urls.py             # /register, /login, /profile endpoints
└── models.py           # CustomUser model
```

---

## ✅ Summary

This accounts app provides a clean and simple authentication system using DRF.
It supports:

* registering new users
* logging in and receiving a token
* retrieving and updating user profile data

Everything is kept lightweight and straightforward, making it easy to extend later.
