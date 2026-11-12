from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import text

from app.db.database import engine


@pytest.fixture
def seeded_employees():
    if engine.url.database != "fastapi_test":
        pytest.skip("Run with DB_NAME=fastapi_test")

    department = f"Test-{uuid4().hex[:8]}"
    employee_ids = []

    try:
        with engine.begin() as conn:
            for name in ("Rahul", "Sara"):
                result = conn.execute(
                    text("""
                        INSERT INTO employees (
                            name, email, age, department, salary,
                            city, pincode, skills, joining_date
                        )
                        VALUES (
                            :name, :email, 28, :department, 50000,
                            'Noida', '201014', '[]', :joining_date
                        )
                    """),
                    {
                        "name": name,
                        "email": f"{uuid4().hex}@example.com",
                        "department": department,
                        "joining_date": date(2025, 1, 15),
                    },
                )
                employee_ids.append(result.lastrowid)

        yield department, employee_ids

    finally:
        with engine.begin() as conn:
            for employee_id in employee_ids:
                conn.execute(
                    text("DELETE FROM employees WHERE id = :id"),
                    {"id": employee_id},
                )


def test_employee_list_paginates_filtered_rows(
    authenticated_client,
    seeded_employees,
):
    department, employee_ids = seeded_employees

    response = authenticated_client.get(
        "/employees-mysql/",
        params={"department": department, "skip": 1, "limit": 1},
    )

    assert response.status_code == 200
    employees = response.json()["data"]["data"]
    assert [employee["id"] for employee in employees] == [employee_ids[1]]
