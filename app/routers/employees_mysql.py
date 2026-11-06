from fastapi import APIRouter, Query, status
from app.schemas.employee_pydantic_schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.services import employee_mysql_service
from app.schemas.api_response import APIResponse, ResponseData
from fastapi import APIRouter, Depends, Query, status
from app.dependencies.auth import get_current_user, require_admin

router = APIRouter(
    prefix='/employees-mysql',
    tags= ['Employees - Mysql']
)

# POST employee
@router.post(
        "",
        response_model=APIResponse[EmployeeResponse],
        status_code=status.HTTP_201_CREATED,
)
def create_employee(emp: EmployeeCreate):
    emp = employee_mysql_service.create_employee(emp)

    return APIResponse[EmployeeResponse](
        success=True,
        data=ResponseData[EmployeeResponse](
            message="Employee created successfully",
            data=emp
        )
    )

@router.get(
    "/", 
    response_model=APIResponse[list[EmployeeResponse]],
    dependencies=[Depends(get_current_user)]
)
def get_employees(
        department: str | None = None,
        skip: int = Query(default = 0, ge = 0),
        limit: int = Query(default = 10, ge=1, le=100),
):
    data = employee_mysql_service.get_all_employees(
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
    "/{id}",
    response_model=APIResponse[EmployeeResponse],
    dependencies=[Depends(get_current_user)]
)
def get_employee_by_id(id: int):
    employee = employee_mysql_service.get_employee_by_id(id)

    return APIResponse[EmployeeResponse](
        success=True,
        data=ResponseData[EmployeeResponse](
            message="",
            data=employee
        )
    )

@router.put(
    "/{id}",
    response_model=APIResponse[EmployeeResponse],
    response_model_exclude_none=True
)
def replace_employee(id: int, emp: EmployeeCreate):

    employee = employee_mysql_service.replace_employee(id, emp);
    return APIResponse[EmployeeResponse](
            success=True,
            data=ResponseData[EmployeeResponse](
                message="Employee updated successfully",
                data=employee
            )
        )

@router.patch(
    "/{id}",
    response_model=APIResponse[EmployeeResponse],
    response_model_exclude_none=True
)
def udpate_employee(id: int, emp: EmployeeUpdate):
    employee = employee_mysql_service.update_employee(id, emp);
    return APIResponse[EmployeeResponse](
        success=True,
        data=ResponseData[EmployeeResponse](
            message="Employee updated successfully",
            data=employee
        )
    )

@router.delete(
    "/{id}",
    response_model=APIResponse[EmployeeResponse],
    response_model_exclude_none=True
)
def delete_employee(id: int):
    employee_mysql_service.delete_employee(id);
    return APIResponse[EmployeeResponse](
        success=True,
        data=ResponseData[EmployeeResponse](
            message="Employee deleted successfully",
            data={}
        )
    )