# AWS Lambda FastAPI Boilerplate

## Overview
A Python 3.12 AWS Lambda boilerplate with FastAPI, SQLite database, Pydantic models, and comprehensive unit tests. Uses Mangum as the ASGI adapter for AWS Lambda integration.

## Project Structure
```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and Lambda handler
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py    # SQLite connection and initialization
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py          # Pydantic models
│   └── routes/
│       ├── __init__.py
│       ├── health.py        # Health check endpoints
│       └── items.py         # CRUD endpoints for items
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_database.py     # Database tests
│   ├── test_health.py       # Health endpoint tests
│   ├── test_items.py        # Item CRUD tests
│   ├── test_lambda.py       # Lambda handler tests
│   └── test_models.py       # Pydantic model tests
└── pyproject.toml
```

## Key Features
- **FastAPI**: Modern Python web framework with automatic OpenAPI docs
- **Mangum**: ASGI adapter for running FastAPI on AWS Lambda
- **SQLite**: Lightweight database (configure DATABASE_PATH env var)
- **Pydantic v2**: Data validation and serialization
- **Full Test Suite**: Unit tests for all components

## Running Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

## Running Tests
```bash
pytest tests/ -v
```

## API Endpoints
- `GET /` - Root welcome message
- `GET /health` - Health check
- `GET /items` - List all items
- `POST /items` - Create item
- `GET /items/{id}` - Get item by ID
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

## AWS Lambda Deployment
The `handler` in `app/main.py` is the Lambda entry point. Configure API Gateway to route to this handler.
