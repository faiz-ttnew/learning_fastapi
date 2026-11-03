from fastapi import APIRouter, Query, status
from app.schemas.employee_pydantic_schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.services import employee_pydantic_service
from app.schemas.api_response import APIResponse, ResponseData

router = APIRouter(
    prefix='/employees-pydantic',
    tags= ['Employees - Pydantic']
)

# Get Employees
@router.get("/", response_model=APIResponse[list[EmployeeResponse]])
def get_employees(
        department: str | None = None,
        skip: int = Query(default = 0, ge = 0),
        limit: int = Query(default = 10, ge=1, le=100),
):
    data = employee_pydantic_service.get_all_employees(
        department=department,
        skip=skip,
        limit=limit
    )
    return APIResponse[list[EmployeeResponse]](
        success=True,
        data=ResponseData[list[EmployeeResponse]](
            message="",
            data=data
        )
    )

# Get employee by id
# /employees/1
@router.get(
        '/{emp_id}',
        response_model=APIResponse[EmployeeResponse]
)
def get_employee(emp_id: int):
    data = employee_pydantic_service.get_employee_by_id(emp_id)
    return APIResponse[EmployeeResponse](
        success=True,
        data=ResponseData[EmployeeResponse](
            message="",
            data=data
        )
    )

# POST emloyee
@router.post(
        "",
        response_model=APIResponse[EmployeeResponse],
        status_code=status.HTTP_201_CREATED,
)
def create_employee(emp: EmployeeCreate):
    emp = employee_pydantic_service.create_employee(emp)

    return APIResponse[EmployeeResponse](
        success=True,
        data=ResponseData[EmployeeResponse](
            message="Employee created successfully",
            data=emp
        )
    )

#  PUT employee replace
@router.put(
    '/{emp_id}',
    response_model=EmployeeResponse,
    )
def replace_employee(emp_id: int, emp:EmployeeCreate):
    return employee_pydantic_service.replace_employee(emp_id, emp)

# PATCH employee delete
@router.patch(
    '/{emp_id}',
    response_model = EmployeeResponse
    )
def update_employee(emp_id: int, emp:EmployeeUpdate):
    return employee_pydantic_service.update_employee(emp_id, emp)

@router.delete(
        "/{emp_id}", 
        status_code=status.HTTP_200_OK,
        response_model=APIResponse[None],
        response_model_exclude_none=True
    )
def delete_employee(emp_id: int):
    employee_pydantic_service.delete_employee(emp_id)
    return APIResponse[None](
        success=True,
        data=ResponseData[None](
            message="Employee deleted successfully",
    )
)
