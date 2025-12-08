# 📘 Social Media API – README

This **Social Media API** is built with **Django REST Framework** and provides functionality for user authentication, posts, comments, and more. It uses **Token Authentication** for secure access to protected endpoints. The default database for development is **SQLite**.

---

## 🟢 Apps Overview

1. **Accounts App** – Handles user authentication and profile management.
2. **Posts App** – Allows users to create, view, update, delete posts and comments, with search and pagination.

---

# 📘 Accounts App

This app handles user authentication and profile management.

## 🚀 Features

### **1. User Registration**

* Implemented using `CreateAPIView`
* Validates incoming user data
* Creates a new user account
* **Endpoint:** `POST /account/register/`

### **2. User Login**

* Custom login flow using `APIView`
* Uses a dedicated `LoginSerializer` for username/password validation
* Generates or retrieves an existing token:

```python
Token.objects.get_or_create(user=user)
```

* Returns the token for authenticated requests
* **Endpoint:** `POST /account/login/`

### **3. User Profile**

* Implemented using `RetrieveUpdateAPIView`
* Allows users to fetch or update their profile
* **Endpoints:**
  `GET /account/profile/`
  `PUT /account/profile/` (or PATCH)

### 🔐 Authentication

* Uses **DRF Token Authentication**
* Clients must include in request headers:

```
Authorization: Token <your_token_here>
```

### 🗂️ Directory Overview

```
accounts/
│
├── serializers.py      # Registration + Login serializers
├── views.py            # Register, Login, Profile views
├── urls.py             # /register, /login, /profile endpoints
└── models.py           # CustomUser model
```

---

# 📘 Posts App

This app allows users to create posts and comments, with full CRUD functionality, search, and pagination.

## 🚀 Features

### **1. Posts**

* Users can **create, view, update, and delete posts**
* Each post includes:

  * `author` – the user who created it
  * `title` – title of the post
  * `content` – text content
  * `created_at` and `updated_at` timestamps
* Only the **author** can edit or delete their own posts
* Supports **searching** posts by `title` or `content`
* **Endpoint Examples:**

  * `GET /post/posts/` – List all posts (paginated)
  * `POST /post/posts/` – Create a new post (authenticated)
  * `GET /post/posts/{id}/` – Retrieve a single post
  * `PUT /post/posts/{id}/` – Update post (author only)
  * `DELETE /post/posts/{id}/` – Delete post (author only)

### **2. Comments**

* Users can **create, view, update, and delete comments** on posts
* Each comment includes:

  * `post` – the related post
  * `author` – the user who commented
  * `content` – text content
  * `created_at` and `updated_at` timestamps
* Only the **author** can edit or delete their own comments
* **Endpoint Examples:**

  * `GET /post/comments/` – List all comments
  * `POST /post/comments/` – Create a comment
  * `GET /post/comments/{id}/` – Retrieve a comment
  * `PUT /post/comments/{id}/` – Update comment (author only)
  * `DELETE /post/comments/{id}/` – Delete comment (author only)

### 🔄 Pagination & Search

* Pagination is applied to post listings (default page size: 10)
* Search via query parameters, e.g.,
  `GET /post/posts/?search=keyword`

### 🗂️ Directory Overview

```
posts/
│
├── serializers.py      # PostSerializer + CommentSerializer
├── views.py            # PostViewSet + CommentViewSet
├── urls.py             # /posts and /comments endpoints
├── permissions.py      # IsAuthorOrReadOnly custom permission
└── models.py           # Post + Comment models
```

---

## 🗝️ Summary

This Social Media API provides:

* **Accounts App** – user registration, login, and profile management
* **Posts App** – posts and comments with CRUD, author-only permissions, search, and pagination

Everything is structured for scalability and ease of extension. Future apps like **follows, fe
