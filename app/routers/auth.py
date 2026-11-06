from fastapi import APIRouter, status, Query, Depends

from app.schemas.api_response import APIResponse, ResponseData
from app.schemas.auth_schema import UserRegister, UserResponse, UserLogin, TokenResponse
from app.services import auth_service
from app.core.security import create_access_token
from app.dependencies.auth import get_current_user

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
    response_model=APIResponse[TokenResponse]
)
def login(credentials: UserLogin):
    user = auth_service.login_user(credentials)

    access_token = create_access_token(user.id)

    return APIResponse[TokenResponse](
        success=True,
        data=ResponseData[TokenResponse](
            message="Login successful",
            data=TokenResponse(
                access_token=access_token,
                token_type="bearer"
            )
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

@router.get(
    "/me",
    response_model=APIResponse[UserResponse]
)
def get_profile(
    current_user: UserResponse = Depends(get_current_user)
):
    return APIResponse[UserResponse](
        success=True,
        data=ResponseData[UserResponse](
            message="Profile fetched successfully",
            data=current_user
        )
    )
