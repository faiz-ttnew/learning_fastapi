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
