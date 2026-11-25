# Skill-to-Opportunities: Backend

## Project summary
Django REST API for a platform where students turn project work into a skills portfolio and find internships and entry-level openings. Candidates link skills to projects as evidence, employers post openings, and the API will compute an explainable match score. This repository is the backend; the React frontend is in `skill-to-opportunities_frontend`.

Done so far: project setup, PostgreSQL connection, custom user model with roles (candidate, employer, admin), register, login, token refresh, current user, role permission classes, Swagger docs and tests.

## Tech stack
Django 5.1, Django REST Framework, SimpleJWT (token login), PostgreSQL, drf-spectacular (Swagger / OpenAPI), pytest and pytest-django.

## Setup steps
1. Install Python 3.12 and PostgreSQL.
2. Create the database: `createdb skill_to_opportunities` (or create it in pgAdmin).
3. Create and activate a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your values.
6. Apply migrations: `python manage.py migrate`
7. Create an admin: `python manage.py createsuperuser`

## Environment variables
| Variable | Meaning |
|---|---|
| DJANGO_SECRET_KEY | Secret key. Use a long random string |
| DJANGO_DEBUG | `True` for development |
| DJANGO_ALLOWED_HOSTS | Comma-separated hosts |
| DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT | PostgreSQL connection |
| CORS_ALLOWED_ORIGINS | Frontend URL, for example `http://localhost:5173` |
| USE_SQLITE | `1` runs on SQLite for quick tests without PostgreSQL |

## How to run
`python manage.py runserver` then open:
- Swagger documentation: http://localhost:8000/api/docs/
- Django admin: http://localhost:8000/admin/

## How to test
`pytest`

To run tests without PostgreSQL: set `USE_SQLITE=1` (Windows PowerShell: `$env:USE_SQLITE=1`).

## API (so far)
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/auth/register/ | Register as candidate or employer |
| POST | /api/auth/login/ | Log in with email and password |
| POST | /api/auth/refresh/ | New access token |
| GET | /api/auth/me/ | Logged-in user details |

## Git workflow
Never commit to `main`. Work on branches such as `neha/feat/auth`, open a pull request with a clear description, add a label, and write `Closes #<issue>` in the description.
