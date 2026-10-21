from fastapi import FastAPI
from app.routers import users
from app.routers import products
from app.routers import employees

app = FastAPI(
    title="User Management API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Hello from FastApi"
    }

app.include_router(users.router)
app.include_router(products.router)
app.include_router(employees.router)
