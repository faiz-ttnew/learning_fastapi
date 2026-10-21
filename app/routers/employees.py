from fastapi import APIRouter, Query, status
from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.services import employee_service

router = APIRouter(
    prefix='/employees',
    tags= ['Employees']
)

# Get Employees
@router.get("/", response_model=list[EmployeeResponse])
def get_employees(
        department: str | None = None,
        skip: int = Query(default = 0, ge = 0),
        limit: int = Query(default = 10, ge=1, le=100),
):
    return employee_service.get_all_employees(
        department=department,
        skip=skip,
        limit=limit
    )

# Get employee by id
# /employees/1
@router.get(
        '/{emp_id}',
        response_model=EmployeeResponse
)
def get_employee(emp_id: int):
    return employee_service.get_employee_by_id(emp_id)

# POST emloyee
@router.post(
        "",
        response_model=EmployeeResponse,
        status_code=status.HTTP_201_CREATED
)
def create_employee(emp: EmployeeCreate):
    return employee_service.create_employee(emp)

#  PUT employee replace
@router.put(
    '/{emp_id}',
    response_model=EmployeeResponse,
    )
def replace_employee(emp_id: int, emp:EmployeeCreate):
    return employee_service.replace_employee(emp_id, emp)

# PATCH employee delete
@router.patch(
    '/{emp_id}',
    response_model = EmployeeResponse
    )
def update_employee(emp_id: int, emp:EmployeeUpdate):
    return employee_service.update_employee(emp_id, emp)

@router.delete("/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(emp_id: int):
    employee_service.delete_employee(emp_id)
    return None