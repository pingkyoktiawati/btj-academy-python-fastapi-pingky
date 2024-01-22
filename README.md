# FastAPI + SQLAlchemy + Alembic Boilerplate

This is a sample project of Async Web API with FastAPI + SQLAlchemy 2.0 + Alembic.
It includes asynchronous DB access using asyncpg and test code.

See [reference](https://github.com/rhoboro/async-fastapi-sqlalchemy/tree/main).

Other References
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQL Alchemy](https://docs.sqlalchemy.org/en/20/orm/index.html)
- [SQL Alchemy - PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

# Setup

## Install

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

## Setup a database and create tables

```shell
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=root \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgdata:/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  postgres:15.2-alpine

# Cleanup database
# $ docker stop db
# $ docker rm db
# $ docker volume rm pgdata

(venv) $ APP_CONFIG_FILE=local python3 app/main.py migrate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a8483365f505, initial_empty
INFO  [alembic.runtime.migration] Running upgrade a8483365f505 -> 24104b6e1e0c, add_tables
```

# Run

```shell
(venv) $ APP_CONFIG_FILE=local python3 app/main.py api
INFO:     Will watch for changes in these directories: ['...']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [92173] using WatchFiles
INFO:     Started server process [92181]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

You can now access [localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.

# Test

```shell
(venv) $ python3 -m pytest
```

# Create Migration

```shell
(venv) $ cd app/migrations
(venv) alembic revision -m "<name_of_migration_file>"
```

# API Documentation - Note

## Create Note

This API endpoint allows you to create a new note by sending an HTTP POST request to the specified URL. 
The request should include a JSON payload in the raw request body type with the keys "title" and "content". 
The values for these keys should represent the title and content of the new note being created.

### Request Body

- title (string, required): The title of the new note.
- content (string, required): The content of the new note.

### Example Request

```shell
curl --location 'http://localhost:8000/api/v1/notes' \
--data '{
    "title": "note1",
    "content": "my first note in btj-academy-python-fastapi-pingky"
}'
```

## Read All Notes

This API endpoint makes an HTTP GET request to retrieve a list of all notes from the API. The request does not require any payload in the request body.

### Example Request

```shell
curl --location 'http://localhost:8000/api/v1/notes'
```

## Read One Note

This API endpoint makes an HTTP GET request to retrieve one notes from the API. The request does not require any payload in the request body.

### Example Request

```shell
curl --location 'http://localhost:8000/api/v1/notes/1'
```

## Update Note

This API endpoint allows you to update an existing note by sending an HTTP PUT request to the specified URL. The request should include a JSON payload in the raw request body type with the keys "new_title" and "new_content". The values for these keys should represent the title and content of the note being updated.

### Request Body

- new title (string, required): The title of the update note.
- new content (string, required): The content of the update note.

### Example Request

```shell
curl --location 'http://localhost:8000/api/v1/notes/1' \
--data '{
    "new_title": "note1rev",
    "new_content": "my first note revision in btj-academy-python-fastapi-pingky"
}'
```

## Delete Note

This API endpoint allows you to delete user by sending an HTTP DELETE request to the specified URL.

### Example Request

```shell
curl --location 'http://localhost:8000/api/v1/notes/1'
```

You also can access the documentation at [localhost:8000/redoc](http://localhost:8000/redoc).