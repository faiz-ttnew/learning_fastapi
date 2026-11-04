from fastapi import FastAPI, Request, HTTPException
from app.routers import users
from app.routers import products
from app.routers import employees
from app.routers import employees_pydantic
from fastapi.responses import JSONResponse
from app.routers import employees_mysql

app = FastAPI(
    title="User Management API",
    version="1.0.0"
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'success': False,
            'data': {
                'message': exc.detail
            }
        },
        headers=exc.headers
    )

@app.get("/")
def home():
    return {
        "message": "Hello from FastApi"
    }

app.include_router(users.router)
app.include_router(products.router)
app.include_router(employees.router)
app.include_router(employees_pydantic.router)
app.include_router(employees_mysql.router)
