from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float


# Schema for POST and PUT
class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2)
    department: str = Field(min_length=2)
    salary: float = Field(gt=2)

# # Schema for PATCH


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    department: str | None = Field(default=None, min_length=2)
    salary: float | None = Field(default=None, gt=0)

# Schema for API responses


class EmployeeResponse(EmployeeCreate):
    id: int
