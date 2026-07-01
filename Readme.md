# 💰 SmartSpend AI - Backend

SmartSpend AI Backend is a RESTful API built using **Django** and **Django REST Framework**. It powers the SmartSpend AI application by providing secure authentication, expense tracking, budget management, analytics, AI-ready insights, and report generation.

---

# 🚀 Features

## 🔐 Authentication

- User Registration
- JWT Authentication
- Login
- Logout
- Profile Management
- Update Profile
- Protected APIs
- Automatic Token Refresh

---

## 💸 Expense Management

- Create Expense
- Update Expense
- Delete Expense
- List Expenses
- Search Expenses
- Filter by Category
- Ordering
- Pagination
- Recurring Expenses

---

## 💰 Budget Management

- Create Monthly Budget
- Update Budget
- Delete Budget
- Monthly Budget Tracking

---

## 📊 Dashboard

Provides analytics including:

- Total Budget
- Total Spent
- Remaining Budget
- Budget Usage Percentage
- Recent Expenses
- Monthly Spending Summary
- Category-wise Spending

---

## 📈 Reports

Generate professional reports.

### PDF Report

- SmartSpend AI Branding
- Financial Summary
- Expense Details
- Monthly Report

### Excel Report

- Financial Summary
- Styled Expense Table
- Monthly Report
- Professional Formatting

---

## 📡 REST API

Authentication

```
POST   /api/accounts/register/
POST   /api/accounts/login/
POST   /api/accounts/logout/
GET    /api/accounts/profile/
PUT    /api/accounts/profile/
```

Expenses

```
GET     /api/expenses/
POST    /api/expenses/
GET     /api/expenses/<id>/
PUT     /api/expenses/<id>/
PATCH   /api/expenses/<id>/
DELETE  /api/expenses/<id>/
```

Budgets

```
GET     /api/budgets/
POST    /api/budgets/
GET     /api/budgets/<id>/
PUT     /api/budgets/<id>/
DELETE  /api/budgets/<id>/
```

Dashboard

```
GET /api/expenses/dashboard/
GET /api/expenses/monthly-summary/
GET /api/expenses/category-summary/
```

Reports

```
GET /api/reports/pdf/
GET /api/reports/excel/
```

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Django | Web Framework |
| Django REST Framework | REST APIs |
| Simple JWT | Authentication |
| PostgreSQL | Database |
| ReportLab | PDF Reports |
| OpenPyXL | Excel Reports |
| django-filter | Filtering |
| Gunicorn | Production Server |
| WhiteNoise | Static Files |

---

# 📁 Project Structure

```
backend/
│
├── accounts/
├── expenses/
├── reports/
├── config/
│
├── media/
├── static/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/your-username/smartspend-ai-backend.git
```

Move into the project

```bash
cd smartspend-ai-backend
```

Create virtual environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔧 Environment Variables

Create a `.env` file.

```env
SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://username:password@localhost:5432/smartspend

ACCESS_TOKEN_LIFETIME=30

REFRESH_TOKEN_LIFETIME=7
```

---

# 🗄 Database

Create migrations

```bash
python manage.py makemigrations
```

Apply migrations

```bash
python manage.py migrate
```

Create superuser

```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

Server

```
http://127.0.0.1:8000/
```

API

```
http://127.0.0.1:8000/api/
```

---

# 🔑 Authentication

The backend uses **JWT Authentication**.

Login

```
POST /api/accounts/login/
```

Response

```json
{
    "access": "...",
    "refresh": "..."
}
```

Include access token

```
Authorization: Bearer <access_token>
```

---

# 📊 API Features

- JWT Authentication
- Pagination
- Search
- Ordering
- Filtering
- Validation
- Custom Serializers
- Generic Views
- APIView
- Error Handling

---

# 📄 Reports

Generate reports for any month.

### PDF

```
GET /api/reports/pdf/?month=7&year=2026
```

### Excel

```
GET /api/reports/excel/?month=7&year=2026
```

---

# 🌍 Deployment

Backend can be deployed using

- Render
- Railway
- Azure
- AWS EC2

Database

- PostgreSQL
- Supabase
- Neon

---

# 📌 Future Improvements

- AI Expense Prediction
- Savings Goals
- OCR Receipt Scanner
- Email Reports
- Scheduled Reports
- Multi Currency Support
- Notification System
- AI Financial Assistant
- REST API Documentation (Swagger/OpenAPI)

---

# 🧪 Testing

Run tests

```bash
python manage.py test
```

---

# 👨‍💻 Author

**Vignesh Donthi**

GitHub

```
https://github.com/your-username
```

LinkedIn

```
https://linkedin.com/in/your-profile
```

---

# 📄 License

Licensed under the MIT License.
## 🌐 Live API

Base URL

https://your-backend.onrender.com/api/