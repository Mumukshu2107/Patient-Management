# Patient Management API

A FastAPI-based Patient Management System integrated with MySQL.

## Features

* Add Patients
* View Patients
* Add Hospitals
* View Hospitals
* Admit Patient to Hospital
* Discharge Patient from Hospital
* Track Patient Hospital Visit History
* Many-to-Many Relationship between Patients and Hospitals
* Admission and Discharge Timestamp Tracking
* Environment Variable Based Database Configuration

## Tech Stack

* Python 3.12
* FastAPI
* SQLAlchemy
* MySQL
* PyMySQL
* Pydantic
* Uvicorn

## Project Structure

```text
Patient-Management/
│
├── .env
├── main.py
├── models.py
├── requirements.txt
├── README.md
│
├── config/
│   ├── __init__.py
│   ├── db.py
│   └── settings.py
│
└── app/
    ├── __init__.py
    ├── api.py
    └── schemas.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=hospital_db
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Mumukshu2107/Patient-Management.git
cd Patient-Management
```

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Patient APIs

| Method | Endpoint  | Description      |
| ------ | --------- | ---------------- |
| POST   | /patients | Add Patient      |
| GET    | /patients | Get All Patients |

### Hospital APIs

| Method | Endpoint   | Description       |
| ------ | ---------- | ----------------- |
| POST   | /hospitals | Add Hospital      |
| GET    | /hospitals | Get All Hospitals |

### Admission APIs

| Method | Endpoint                          | Description               |
| ------ | --------------------------------- | ------------------------- |
| POST   | /assign-hospital                  | Admit Patient             |
| POST   | /patients/{patient_id}/discharge  | Discharge Patient         |
| GET    | /patients/{patient_id}/hospitals  | Patient Hospital History  |
| GET    | /hospitals/{hospital_id}/patients | Patients Visited Hospital |

## Business Rules

* A patient can visit multiple hospitals.
* A hospital can have multiple patients.
* A patient can only be admitted to one hospital at a time.
* A patient must be discharged before admission to another hospital.
* Admission and discharge timestamps are stored for audit purposes.

## Author

Moksha Krishna
