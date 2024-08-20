# Energy Collection System
This application gathers measurements from various platforms. It retrieves data through API calls and present the measurements in a standardized format.

## Models
- User
- Installation
- Meter
- Channel
- Measurement

## Stack

- [Fast api](https://fastapi.tiangolo.com/) + Uvicorn
- [SQLAlchemy](https://sqlalchemy.org) + [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment) + Postgres

---

- [Energy dashboard](http://localhost:5555)
Flower UI for celery workers and tasks
- [Postgres admin ](http://localhost:8080) web interface

## Alembic

to write database migrations change DB_HOST in env to localhost and forward docker port to localhost in docker-compose:

    alembic revision --autogenerate -m "description"

if migration script is tested, undo above changes and rerun docker-compose, this updates the database with the latest migration version. Please do improve workflow :)
