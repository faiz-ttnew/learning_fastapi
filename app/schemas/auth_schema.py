from typing import Literal
from app.common.enums import UserRole
from app.common.user_interface import UserInsertParams

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator
)

class UserRegister(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(num_length=2, max_length=100)
    email: EmailStr = Field(max_length=255)
    password: SecretStr = Field(min_length=6, max_length=120)

    @field_validator('name', mode='before')
    @classmethod
    def trim_name(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool