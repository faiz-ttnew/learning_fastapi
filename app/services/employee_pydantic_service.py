from fastapi import HTTPException
from app.schemas.employee_pydantic_schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from pydantic import ValidationError

# Temporary in-memory database
employees: dict[int, EmployeeResponse] = {}

next_employee_id = 3

# 1. Get all Employees
def get_all_employees(
        department: str | None = None,
        skip: int = 0,
        limit: int = 10
):
    result = list(employees.values())

    if department is not None:
        result = [
            emp for emp in result
            if emp.department.lower() == department.lower()
        ]
    return result[skip:skip+limit]

# 2. Get employee by ID
def get_employee_by_id(emp_id: int):
    employee = employees.get(emp_id)

    if employee is None:
        raise HTTPException(
            status_code = 404,
            detail= "Employee not found"
        )
    return employee

# 3. Create employee
def create_employee(emp: EmployeeCreate):
    global next_employee_id

    new_emp = EmployeeResponse(
        id  = next_employee_id,
        **emp.model_dump()
    )
    employees[next_employee_id] = new_emp

    next_employee_id += 1

    return new_emp

# 4. PUT - Full replacement Employee
def replace_employee(
        emp_id: int,
        emp: EmployeeCreate
        ):
    get_employee_by_id(emp_id)

    update_employee = EmployeeResponse(
        id = emp_id,
        **emp.model_dump()
    )
    employees[emp_id] = update_employee

    return update_employee


# 5. PATCH - partial update employee
def update_employee(
        emp_id: int,
        emp: EmployeeUpdate
):
    # Existing employee fetch ; not match then 404.
    existing_emp = get_employee_by_id(emp_id)

    updates = emp.model_dump(exclude_unset=True)

    # Do not allow null values
    if any(value is None for value in updates.values()):
        raise HTTPException(
            status_code = 422,
            detail = 'Employee field can not be null'
        )

    merged = {
        **existing_emp.model_dump(),
        **updates
    }

    try:
        updated_employee = EmployeeResponse.model_validate(merged)
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": [
                        str(part) for part in error['loc']
                    ],
                    'msg': error['msg'],
                    'type': error['type']
                }
                for error in exc.errors()
            ]
        ) from exc

    employees[emp_id] = updated_employee
    return updated_employee

# 6. Delete - employee 
def delete_employee(emp_id: int):
    get_employee_by_id(emp_id)

    del employees[emp_id]
