from typing import NotRequired, TypedDict

from app.common.enums import UserRole


class UserInsertParams(TypedDict):
    name: str
    email: str
    password: str
    role: UserRole
    is_active: NotRequired[bool]
