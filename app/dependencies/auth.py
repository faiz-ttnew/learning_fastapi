from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import verify_access_token
from app.schemas.auth_schema import UserResponse
from app.services.auth_service import get_auth_user_by_id

bearer_schema = HTTPBearer(
    auto_error=False
)

def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(
            bearer_schema
        )
) -> UserResponse:
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Access token required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user_id = verify_access_token(credentials.credentials)

    return get_auth_user_by_id(user_id)
