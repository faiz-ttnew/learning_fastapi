# FastAPI Employee Management API

## Project Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Configure database settings

Ensure MySQL is running. Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=db_name
```

The database name must match `app/db/schema.sql`. The MySQL user needs permission to create the database and tables.

### 5. Create the database and tables

```bash
python -m app.db.init_db
```

6. Check the database connection

```bash
python check_db.py
```

### 7. Run the project

```bash
uvicorn main:app --reload
```

### 8. Open the application

- Application: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

Press `Ctrl+C` to stop the server.

### 9. JWT setup

- run command in terminal

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Run database migrations

```bash
alembic upgrade head
```

Applies all pending migrations (employees `mobile_number`, `users` table, etc.).

## Database Migrations (Alembic)

Run all commands from the project root. The DB connection is read from `.env`.
Migrations are written by hand (`--autogenerate` is not supported in this project).

| Command | Purpose |
| --- | --- |
| `alembic revision -m "message"` | Create a new empty migration file in `alembic/versions/` |
| `alembic upgrade head` | Apply all pending migrations (create/update tables) |
| `alembic upgrade +1` | Apply only the next migration |
| `alembic downgrade -1` | Roll back the last migration |
| `alembic downgrade <revision>` | Roll back to a specific revision |
| `alembic current` | Show the revision the database is currently on |
| `alembic heads` | Show the latest revision in the migration files |
| `alembic history` | List all migrations (`-v` for details) |
| `alembic upgrade head --sql` | Print the SQL without running it |
| `alembic stamp head` | Mark the DB as up to date without running SQL |

### Create a new table

```bash
alembic revision -m "create <table_name> table"
# write CREATE TABLE in upgrade() and DROP TABLE in downgrade()
alembic upgrade head
```

### Update an existing table

```bash
alembic revision -m "add <column> to <table_name>"
# write ALTER TABLE in upgrade() and the reverse in downgrade()
alembic upgrade head
```
