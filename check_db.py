from sqlalchemy import text
from app.db.database import engine

def check_database():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        # print("Database connection successful:", result.scalar() == 1)
        print("Query result:", result.scalar_one())

if __name__ == "__main__":
    check_database()