from pydantic import (
    BaseModel, 
    Field,
    EmailStr,
    field_validator,
    model_validator
)
from datetime import date
from typing import Self


class Address(BaseModel):
    city: str = Field(min_length=2)
    pincode : str = Field(pattern=r"^\d{6}$")

class EmployeeBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, le=60)
    department: str = Field(min_length=2)
    salary: float = Field(gt=0)
    address: Address
    skills: list[str] = Field(default_factory=list)
    joining_date: date

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not all(
            char.isalpha() or char.isspace()
            for char in value
        ):
            raise ValueError(
                'Name must be contain only letters and spaces'
            )
        return value.strip()

    @field_validator('skills')
    @classmethod
    def validate_skills(cls, value: list[str]) -> list[str]:
        if any(not skill.strip() for skill in value):
            raise ValueError(
                'Skills can not be empty'
            )
        return value

    @model_validator(mode='after')
    def validate_joining_date(self) -> Self:
        if self.joining_date > date.today():
            raise ValueError(
                'Joining date cannot be in the future'
            )
        return self

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: str | None = Field(
        default=None, min_length=2, max_length=50
    )
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18, le=60)
    department: str | None = Field(default=None, min_length=2)
    salary: float | None = Field(default=None, gt=0)
    address: Address | None = None
    skills: list[str] | None = None
    joining_date : date | None = None

# Schema for API responses
class EmployeeResponse(EmployeeBase):
    id: int
