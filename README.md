

# SmartLink API

**SmartLink API** is a FastAPI-based URL shortening service with user authentication, email verification via OTP, and link analytics. Users can register, verify their email, create short links, and track link clicks.

---

## 🚀 Features

* User registration and email verification via OTP
* JWT-based authentication
* Short URL creation with unique Base62 short codes
* Link analytics (click count, recent clicks, referrer, user agent, IP)
* Fully tested with `pytest` and `FastAPI TestClient`
* Async email sending for OTP delivery

---

## 🛠 Tech Stack

* **Backend**: Python 3.11, FastAPI
* **Database**: PostgreSQL / SQLite (for testing)
* **ORM**: SQLAlchemy 2.0 with Pydantic v2 models
* **Authentication**: JWT access tokens
* **Email**: FastAPI-Mail
* **Testing**: Pytest, unittest.mock, FastAPI TestClient

---

## 📋 API Flow


graph LR
    A[User Registration] --> B[Email Verification]
    B --> C[JWT Login]
    C --> D[Create Short Links]
    D --> E[Redirect & Analytics]
    E --> F[View Link Stats]


---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/your-username/smartlink-api.git
cd smartlink-api
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file:
```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRATION_MINUTES=60

MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_PORT=587
MAIL_SERVER=smtp.example.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USE_CREDENTIALS=True
VALIDATE_CERTS=True
```

### 5. Run the API
```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the **Swagger UI**.

---

## 📡 API Endpoints

### 👤 User Routes

| Endpoint              | Method | Description                         |
| --------------------- | ------ | ----------------------------------- |
| `/users/register`     | POST   | Register a new user and send OTP    |
| `/users/verify-email` | POST   | Verify user email using OTP         |
| `/users/login`        | POST   | Authenticate user and get JWT token |
| `/users/otp-request`  | POST   | Request a new OTP                   |

### 🔗 Link Routes

| Endpoint                   | Method | Description                              |
| -------------------------- | ------ | ---------------------------------------- |
| `/links/`                  | POST   | Create a new short link                  |
| `/links/{short_url}`       | GET    | Redirect to the original URL             |
| `/links/get/all`           | GET    | Get all links for the authenticated user |
| `/links/{short_url}/stats` | GET    | Get analytics for a short link           |

---

## 💡 Example Usage

### Register User
```bash
POST /users/register
{
  "username": "john",
  "email": "john@example.com",
  "password": "Strong@123"
}
```

### Login User
```bash
POST /users/login
username=john@example.com
password=Strong@123
```

### Create Short Link
```bash
POST /links/
Authorization: Bearer <token>
{
  "original_url": "https://example.com"
}
```

### Get Link Stats
```bash
GET /links/{short_url}/stats
Authorization: Bearer <token>
```

---

## 🧪 Testing

Run the test suite using `pytest`:

```bash
pytest tests/ -v
```

* The project includes **fixtures** for a test database and a test user.
* Mocked OTP email sending ensures tests do not send real emails.

---

## 📁 Project Structure

```
app/
├─ auth/
│  ├─ auth_bearer.py
│  ├─ auth_handler.py
│  ├─ otp_utils.py
│  └─ email_utils.py
├─ core/
│  └─ config.py
├─ db/
│  ├─ session.py
├─ models/
│  ├─ base.py
│  ├─ user.py
│  ├─ link.py
│  └─ click_log.py
├─ repository/
│  ├─ users.py
│  └─ link.py
├─ routers/
│  ├─ users.py
│  ├─ link.py
│  └─ __init__.py
├─ schemas/
│  ├─ user.py
│  └─ link.py
└─ main.py

tests/
├─ test_auth.py
├─ test_links.py
└─ conftest.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Open a pull request

---

## 📄 License

MIT License © 2025 Srinivas Reddy Marri
