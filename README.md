# Hospital Management System

A full-stack Hospital Management System built using **FastAPI**, **Next.js**, **MySQL**, and **RabbitMQ** with role-based access control, JWT authentication, middleware, background workers, and CSV processing.

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* Pydantic
* JWT Authentication
* MySQL
* RabbitMQ
* Pika
* Pandas

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Axios

---

# Features

## Authentication

* JWT-based authentication
* Login system
* Protected routes
* Token validation middleware

---

## Role-Based Access Control

### Super Admin

* View dashboard
* Manage users
* Add users
* Upload CSV files
* View hospitals
* View patients

### Admin

* Manage hospitals
* Manage patients
* Upload CSV files

### Doctor

* View patients

### Receptionist

* Add patients
* View patients

---

# Dashboard

Displays:

* Total Users
* Total Hospitals
* Total Patients
* Admitted Patients
* Discharged Patients

---

# User Management

Super Admin can:

* View all users
* Add new users
* Assign roles:

  * ADMIN
  * DOCTOR
  * RECEPTIONIST

---

# Patient Management

* Add patient
* View patients
* Role-based access
* Duplicate prevention

Patient fields:

* Name
* Age
* Contact Number
* Height
* Weight
* Blood Group

---

# Hospital Management

* Add hospitals
* View hospitals
* Duplicate hospital checking

Hospital fields:

* Name
* City

---

# CSV Upload

Supported entities:

* Patients
* Hospitals

CSV files are uploaded through the frontend and processed asynchronously.

---

# RabbitMQ Integration

RabbitMQ is used for background processing.

## CSV Queue

Queue Name:

csv_queue

Used for:

* Hospital CSV uploads
* Patient CSV uploads

Worker:

```bash
python -m app.workers.csv_worker
```

---

## Logging Queue

Queue Name:

log_queue

Used for:

* Login logs
* API request logs

Worker:

```bash
python -m app.workers.log_worker
```

---

# Middleware

## Authentication Middleware

Responsible for:

* JWT validation
* Setting current user
* Setting user role

Request state:

```python
request.state.user
request.state.role
```

---

## Logging Middleware

Logs:

* Request method
* API path
* Timestamp

Logs are sent to RabbitMQ.

---

# Project Structure

```text
backend/
│
├── app/
│   ├── middleware/
│   ├── workers/
│   ├── tasks/
│   ├── queues/
│   ├── models/
│   ├── schemas/
│   └── api.py
│
frontend/
│
├── app/
├── components/
├── services/
└── pages/
```

---

# Installation

## Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Run backend:

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# RabbitMQ

Install RabbitMQ:

```bash
sudo apt install rabbitmq-server

sudo systemctl start rabbitmq-server

sudo systemctl enable rabbitmq-server
```

---

# Run Workers

CSV Worker:

```bash
python -m app.workers.csv_worker
```

Log Worker:

```bash
python -m app.workers.log_worker
```

---

# Default Roles

* SUPER_ADMIN
* ADMIN
* DOCTOR
* RECEPTIONIST

---

# API Endpoints

## Authentication

* POST /auth/login

## Users

* GET /users
* POST /users

## Patients

* GET /patients
* POST /patients

## Hospitals

* GET /hospitals
* POST /hospitals

## Dashboard

* GET /dashboard

## Profile

* GET /me

## CSV Upload

* POST /upload-data

---

# Future Enhancements

* Appointment Management
* Email Notifications
* Audit Logs
* Report Generation
* Appointment Scheduling
* Redis Caching
* Docker Deployment
* Kubernetes Deployment

---

# Author
Moksha Krishna 
