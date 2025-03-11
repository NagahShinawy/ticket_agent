# Ticket Assignment System

This project is a Django-based API for assigning support tickets to agents. It includes features like ticket creation, assignment, and retrieval, with support for pagination, authentication, and logging.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Logging](#logging)
- [Testing](#testing)

---

## Features
- **Ticket Management**: Admins can create, update, and delete tickets.
- **Ticket Assignment**: Agents can fetch and assign tickets to themselves.
- **Pagination**: Tickets are paginated for efficient retrieval.
- **Authentication**: Token-based authentication for secure API access.
- **Logging**: Custom logging for debugging and monitoring.

---

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- PostgreSQL (or any other database supported by Django)
- pip (Python package manager)

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/NagahShinawy/ticket_agent.git
cd ticket_agent
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements/base.txt
```

### 4. Configure the Database
1. Create a PostgreSQL database named `softxpert`.
2. Update the database settings in `settings/base.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'softxpert',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

---

## Running the Project

### 1. Start the Development Server
```bash
python manage.py runserver
```

### 2. Access the API
- Open your browser and go to `http://127.0.0.1:8000/api/`.
- Use the browsable API to interact with the endpoints.

### 3. Obtain a Token
To access protected endpoints, obtain a token by sending a POST request to:
```bash
curl -X POST -d "username=your_username&password=your_password" http://127.0.0.1:8000/api/auth/token/
```

---

## API Endpoints

### Admin Endpoints
- **Create Ticket**: `POST /api/admin/tickets/`
- **Update Ticket**: `PUT /api/admin/tickets/{id}/`
- **Delete Ticket**: `DELETE /api/admin/tickets/{id}/`

### Agent Endpoints
- **Fetch Tickets**: `GET /api/agent/tickets/`
  - Assigns up to 15 tickets to the agent if none are assigned.
  - Returns paginated results.

---

## Logging
Logs are printed to the console for debugging and monitoring. The logging level is set to `DEBUG` for the `tickets` app, so all log messages are displayed.

Example logs:
```
DEBUG Fetching tickets for agent: admin
INFO Agent admin is requesting tickets.
DEBUG Assigning 5 new tickets to agent: admin
INFO Assigned 5 tickets to agent: admin
```

---

## Testing
To run tests, use the following command:
```bash
python manage.py test
```

---

Enjoy using the Ticket Assignment System! 🚀