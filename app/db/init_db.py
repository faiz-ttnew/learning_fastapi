from pathlib import Path
import sqlparse
from sqlalchemy import create_engine

from app.db.database import database_url


SCHEMA_FILE = Path(__file__).resolve().parent / "schema.sql"

def init_db():
    # Same credentials, but no database selected initially.
    server_url = database_url._replace(database=None)

    setup_engine = create_engine(
        server_url, 
        pool_pre_ping=True
    )

    try:
        sql_content = SCHEMA_FILE.read_text(encoding="utf-8")

        sql_content = sqlparse.format(
            sql_content, 
            strip_comments=True
        )

        statements = [
            statement.strip()
            for statement in sqlparse.split(sql_content)
            if statement.strip()
        ]

        if not statements:
            raise RuntimeError("No SQL statements found in schema.sql")
        with setup_engine.begin() as conn:
            for index, statement in enumerate(statements, start=1):
                 print(f"Executing statement {index}")
                 conn.exec_driver_sql(statement)
        
        print("Database and tables created successfully.")
    finally:
        setup_engine.dispose()

if __name__ == "__main__":
    init_db()