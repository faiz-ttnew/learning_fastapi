import json
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.db.database import engine
from app.schemas.employee_pydantic_schema import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate
)

EMPLOYEE_SELECT = """
    SELECT
        id, name, email, age, department, salary,
        city, pincode, skills, joining_date, mobile_number
    FROM employees
"""

def row_to_employee(row) -> EmployeeResponse:
    skills = row['skills']

    if isinstance(skills, str):
        skills = json.loads(skills)

    return EmployeeResponse(
         id=row["id"],
        name=row["name"],
        email=row["email"],
        age=row["age"],
        department=row["department"],
        salary=row["salary"],
        address={
            "city": row["city"],
            "pincode": row["pincode"]
        },
        skills=skills,
        joining_date=row["joining_date"],
        mobile_number=row['mobile_number']
    )

def create_employee(emp: EmployeeCreate):
    query = text(
        """
        INSERT INTO employees (
            name, 
            email,
            age, 
            department,
            salary,
            city,
            pincode,
            skills,
            joining_date,
            mobile_number
        )
        VALUES (
            :name, 
            :email, 
            :age,
            :department,
            :salary,
            :city,
            :pincode,
            :skills,
            :joining_date,
            :mobile_number
        )
        """
    )

    params = {
        "name": emp.name,
        'email': emp.email,
        "age": emp.age,
        "department": emp.department,
        "salary": emp.salary,
        "city": emp.address.city,
        "pincode": emp.address.pincode,
        "skills": json.dumps(emp.skills),
        "joining_date": emp.joining_date,
        "mobile_number": emp.mobile_number
    }

    try:
        with engine.begin() as connection:
            result = connection.execute(query, params)

            emp_id = result.lastrowid

            row = connection.execute(
                text(EMPLOYEE_SELECT + " WHERE id = :emp_id"),
                {"emp_id": emp_id}
            ).mappings().one()


            employee = row_to_employee(row)

        return employee
    except IntegrityError as exc:
        if exc.orig.args[0] == 1062:
            raise HTTPException(
                status_code=409,
                detail="Employee email already exists"
            ) from exc
        raise


# 1. Get all Employees
def get_all_employees(
        department: str | None = None,
        skip: int = 0,
        limit: int = 10
):
    query = EMPLOYEE_SELECT
    params =  {"skip": skip, "limit": limit}

    if department is not None:
        query += " WHERE department = :department"
        params["department"] = department

    query += " ORDER BY id LIMIT :limit OFFSET :skip"

    with engine.begin() as conn:
        rows = conn.execute(
            text(
                query
            ), params
        ).mappings().all()
        employees = [row_to_employee(row) for row in rows]
        return employees

# 1. Get Employee by id
def get_employee_by_id(id: int):
    query = EMPLOYEE_SELECT
    params =  {}

    if id is not None:
        query += " WHERE id = :id"
        params["id"] = id

        with engine.begin() as conn:
            row = conn.execute(
                text(
                    query
                ), params
            ).mappings().one_or_none()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail='Employee not found'
                )
        employee = row_to_employee(row)
        return employee

# put full employee replacement
def replace_employee(
        id: int,
        emp: EmployeeCreate
):
    params = {
        "name": emp.name,
        "email": str(emp.email),
        "age": emp.age,
        "department": emp.department,
        "salary": emp.salary,
        "city": emp.address.city,
        "pincode": emp.address.pincode,
        "skills": json.dumps(emp.skills),
        "joining_date": emp.joining_date,
        "mobile_number": emp.mobile_number
    }
    params['id'] = id
    query = """
                    update employees
                    set
                    name=:name,
                    email = :email,
                    age = :age,
                    department = :department,
                    salary = :salary,
                    city = :city,
                    pincode = :pincode,
                    skills = :skills,
                    joining_date = :joining_date
                    mobile_number = :mobile_number
                where id = :id
                """
    with engine.begin() as conn:
        result = conn.execute(text(query), params)

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

def update_employee(id: int, emp: EmployeeUpdate):
    updates = emp.model_dump(exclude_unset = True)

    if not updates:
        raise HTTPException(
            status_code=422,
            detail="Provide at least one field to update"
        )
    if any(val is None for val in updates.values()):
        raise HTTPException(
            status_code=422,
            detail="Employee fields cannot be null"
        )
    # Only these fields can become SQL column names.
    allowed_columns = {
        "name",
        "email",
        'age',
        "department",
        "salary",
        "joining_date",
        "mobile_number"
    }
    params = {}

    for key, value in updates.items():
         if key in allowed_columns:
            params[key] = value
         elif key == "address":
            params["city"] = value["city"]
            params["pincode"] = value["pincode"]

         elif key == "skills":
            params["skills"] = json.dumps(value)
         
         else:
             raise HTTPException(
                 status_code=422,
                 detail=f"Unsupported update field: {key}"
             )
         set_clause = ", ".join(
             f"`{column}` = :{column}"
             for column in params
         )

         query = text(f"""
                    UPDATE employees
                    SET {set_clause}
                    WHERE id = :id
                """)
         params["id"] = id
         
    with engine.begin() as conn:
        result = conn.execute(query, params)

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

def delete_employee(id: int):
    query = text("delete from employees where id=:id")
    with engine.begin() as conn:
        result = conn.execute(query, {"id": id})
        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )