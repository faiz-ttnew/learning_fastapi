from fastapi import APIRouter, status

from app.schemas.api_response import APIResponse, ResponseData
from app.schemas.auth_schema import UserRegister, UserResponse
from app.services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    '/register',
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED
)
def register(user: UserRegister):
    registered_user = auth_service.register_user(user)

    return APIResponse[UserResponse](
        success=True,
        data=ResponseData[UserResponse](
            message="User registered successfully",
            data=registered_user
        )
    )