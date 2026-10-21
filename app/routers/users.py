from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import User
from app.services.user_service import (
    get_user_by_id,
    get_all_users    
)

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/', response_model=list[User])
def fetch_users():
    return get_all_users()

@router.get('/{id}', response_model=User)
def fetch_user(id: int):
    user = get_user_by_id(id)
    if user is None:
        HTTPException(
            status_code=404,
            detail='User not found'
        )
    return user