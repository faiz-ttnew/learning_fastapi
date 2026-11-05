from fastapi import FastAPI, Request, HTTPException
from app.routers import users
from app.routers import products
from app.routers import employees
from app.routers import employees_pydantic
from fastapi.responses import JSONResponse
from app.routers import employees_mysql
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.middleware.request_logging import log_requests

app = FastAPI(
    title="User Management API",
    version="1.0.0"
)

app.middleware("http")(log_requests)

# Expected HTTP errors: 404, 403, etc.
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": {
                "message": exc.detail
            }
        },
        headers=exc.headers
    )


# Invalid request body, path or query parameters.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(str(part) for part in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": {
                "message": "Request validation failed",
                "errors": errors
            }
        }
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
