# Hospital Management System

A full-stack Hospital Management System built using **FastAPI**, **Next.js**, **MySQL**, and **JWT Authentication**.

The application provides role-based access control for hospital staff and allows management of patients, hospitals, admissions, users, and reports.

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy ORM
* MySQL
* JWT Authentication
* Passlib (Password Hashing)
* Middleware
* Pandas
* Uvicorn

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Axios

---

# Features

## Authentication

* JWT Login
* Password Hashing using bcrypt
* Token-based Authentication
* User Profile API

---

## Role-Based Access Control

### SUPER_ADMIN

* Create users
* View users
* Dashboard access
* Full system access

### ADMIN

* Add hospitals
* Upload data
* Download reports
* Dashboard access

### DOCTOR

* View patient information
* Access hospital details

### RECEPTIONIST

* Add patients
* Admit patients
* Discharge patients

---

# User Roles

* SUPER_ADMIN
* ADMIN
* DOCTOR
* RECEPTIONIST

---

# Patient Management

* Add patient
* View patients
* Search patients
* Upload patient CSV
* Patient admission history

---

# Hospital Management

* Add hospitals
* View hospitals
* Assign patients
* Hospital-wise patient list
* Upload hospital CSV
* Download hospital CSV

---

# User Management

Only Super Admin can:

* Create users
* View users
* Manage system users

---

# Dashboard

Dashboard statistics:

* Total Patients
* Total Hospitals
* Admitted Patients
* Discharged Patients
* Total Users

---

# Project Structure

```text
Hospital-Project/

├── backend/
│   ├── app/
│   │   ├── middleware/
│   │   ├── routers/
│   │   ├── utils/
│   │   ├── security.py
│   │   └── schemas.py
│   │
│   ├── config/
│   │   ├── db.py
│   │   └── settings.py
│   │
│   ├── main.py
│   └── models.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── services/
│   └── middleware.ts
│
└── README.md
```

---

# Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create `.env`

```env
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=hospital_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

Install packages:

```bash
npm install
```

Run:

```bash
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

# Authentication Flow

1. User logs in.
2. JWT token is generated.
3. Token stored in localStorage.
4. Axios attaches token automatically.
5. Middleware validates token.
6. User information stored in request.state.
7. APIs check user roles.

---

# Middleware

## Logging Middleware

Logs:

* Request method
* URL
* Response status

---

## Authentication Middleware

Validates:

* Authorization header
* JWT token
* User existence

Stores:

```python
request.state.user
request.state.user_id
request.state.username
request.state.role
```

---

# Database Tables

## users

* id
* username
* password
* role

## patients

* id
* name
* age
* contact_no
* height
* weight
* blood_group
* status
* current_hospital_id

## hospitals

* id
* name
* city

## patient_hospital

* patient_id
* hospital_id
* admit_time
* discharge_time

---

# API Endpoints

## Authentication

| Method | Endpoint    |
| ------ | ----------- |
| POST   | /auth/login |
| GET    | /me         |

---

## Users

| Method | Endpoint |
| ------ | -------- |
| GET    | /users   |
| POST   | /users   |

---

## Patients

| Method | Endpoint        |
| ------ | --------------- |
| GET    | /patients       |
| POST   | /patients       |
| GET    | /search/patient |

---

## Hospitals

| Method | Endpoint   |
| ------ | ---------- |
| GET    | /hospitals |
| POST   | /hospitals |

---

## Admission

| Method | Endpoint                 |
| ------ | ------------------------ |
| POST   | /assign-hospital         |
| POST   | /patients/{id}/discharge |

---

## Dashboard

| Method | Endpoint   |
| ------ | ---------- |
| GET    | /dashboard |

---

# Security

* Password hashing using bcrypt
* JWT authentication
* Role-based authorization
* Protected frontend routes
* Middleware validation

---

# Future Enhancements

* RabbitMQ Queue
* Email Notifications
* Redis Caching
* Audit Logs
* Appointment Module
* Doctor Scheduling
* Billing System
* Docker Deployment
* Kubernetes Deployment
* CI/CD Pipeline

---

# Author

Moksha Krishna

Hospital Management System built using FastAPI and Next.js.
