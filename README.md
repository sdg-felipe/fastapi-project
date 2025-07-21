# FastAPI Rental App

Backend built with FastAPI, SQLAlchemy, and JWT for managing users, items, and rentals.

## Requirements

- Python 3.11+
- MySQL
- pip

## Installation
```bash
pip install -r requirements.txt
```

## Environment Variables
Create a .env file in the project root with:

```bash
DATABASE_URL=mysql+pymysql://user:password@localhost/db_name
JWT_SECRET=secret
JWT_ALGORITHM=HS256
```

## Run the Server
```bash
uvicorn main:app --reload
```

App available at: http://localhost:8000/docs
