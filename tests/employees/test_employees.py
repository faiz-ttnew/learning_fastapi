from unittest.mock import Mock

from app.routers import employees_mysql
from app.schemas.employee_pydantic_schema import EmployeeResponse

def test_employee_list_passes_filters_and_pagination(
        authenticated_client,
        monkeypatch
):
    employee = EmployeeResponse(
        id=1,
        name="Rahul",
        email="rahul@example.com",
        age=28,
        department="IT",
        salary=50000,
        address={"city": "Noida", "pincode": "201014"},
        skills=["Python"],
        joining_date="2025-01-15",
    )

    mock_get_employees = Mock(return_value=[employee])

    monkeypatch.setattr(
        employees_mysql.employee_mysql_service,
        "get_all_employees",
        mock_get_employees
    )

    response = authenticated_client.get(
        "/employees-mysql/",
        params={"department": "IT", "skip": 0, "limit": 5},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert len(body["data"]["data"]) == 1
    assert body["data"]["data"][0]["name"] == "Rahul"

    mock_get_employees.assert_called_once_with(
        department="IT",
        skip=0,
        limit=5,
    )
