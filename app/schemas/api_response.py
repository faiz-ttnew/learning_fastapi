from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar('T')

class ResponseData(BaseModel, Generic[T]):
    message: str
    data: T | None = None

class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: ResponseData[T]