from pydantic import (
    BaseModel,
    Field, 
    field_validator,
)
from datetime import date
from typing import Self

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str

class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    sku: str = Field(min_length=3, max_length=30)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str = Field(min_length=3, max_length=50)
    tags: list[str] = Field(default_factory=list)

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

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        if any(not tag.strip() for tag in value):
            raise ValueError(
                'Tag can not be empty'
            )
        return value

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None, min_length=2, max_length=50
    )
    sku: str | None = Field(
        default=None, min_length=3, max_length=30
    )
    price: str | None = Field(
        default=None, gt=0
    )
    stock: str | None = Field(
        default=None, ge=0
    )
    category: str | None = Field(
        default=None, min_length=3, max_length=50
    )
    tags: list[str] | None = None

class ProductResponse(ProductBase):
    id: int
