import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

database_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
    query={"charset": "utf8mb4"}
)

engine = create_engine(
    database_url,
    pool_pre_ping=True, 
)