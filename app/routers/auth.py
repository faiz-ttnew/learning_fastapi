from fastapi import APIRouter, status, Query

from app.schemas.api_response import APIResponse, ResponseData
from app.schemas.auth_schema import UserRegister, UserResponse, UserLogin
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

@router.post(
    '/login',
    response_model=APIResponse[UserResponse]
)
def login(credentials: UserLogin):
    user = auth_service.login_user(credentials)

    return APIResponse[UserResponse](
        success=True,
        data = ResponseData[UserResponse](
            message='Credentials verified successfully',
            data=user
        )
    )

@router.get(
    '/users',
    response_model=APIResponse[list[UserResponse]]
)
def get_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default = 10, ge=1, le=100),
):
    users = auth_service.get_users(
        skip=skip,
        limit=limit
    )

    return APIResponse[list[UserResponse]](
        success=True,
        data = ResponseData[list[UserResponse]](
            message='',
            data=users
        )
    )
