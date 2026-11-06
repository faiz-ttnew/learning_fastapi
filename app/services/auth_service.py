from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, verify_password
from app.db.database import engine
from app.schemas.auth_schema import UserRegister, UserResponse, UserLogin
from app.common.enums import UserRole

SELECT_USER = """select id, name, email, role, is_active from users"""

def register_user(user: UserRegister) -> UserRegister:
    hashed_password = hash_password(
        user.password.get_secret_value()
    )

    params = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": UserRole.USER
    }

    try:
        with engine.begin() as conn:
            result = conn.execute(
                text(
                    """
                    insert into users (
                        name,
                        email,
                        password,
                        role
                    )
                    values(
                        :name,
                        :email,
                        :password,
                        :role
                    )
                    """
                ),
                params
            )

            user_id = result.lastrowid

            row = conn.execute(
                text(
                    """
                        select id, name, email, role, is_active
                        from users as u 
                        where id = :user_id
                    """
                ),
                {'user_id': user_id}
            ).mappings().one()
            
            registered_user = UserResponse.model_validate(
                dict(row)
            )

            return registered_user
    except IntegrityError as exc:
        if exc.orig.args[0] == 1062:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            ) from exc

        raise

def get_user_by_email(email: str):
    query = text("""
                select id, name, email, password, role, is_active
                from users 
                where email = :email
            """)
    with engine.connect() as conn:
        return conn.execute(
            query,
            {'email': email}
        ).mappings().one_or_none()

def login_user(credentials: UserLogin) -> UserResponse:
    user = get_user_by_email(str(credentials.email))

    if user is None:
        raise HTTPException(
            status_code=401,
            detail='Invalid email or password'
        )

    password_valid = verify_password(
        credentials.password.get_secret_value(),
        user['password']
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail='Invalid email or password'
        )

    if not user['is_active']:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    return UserResponse(
        id=user["id"],
        name=user["name"],
        email=user["email"],
        role=user["role"],
        is_active=user["is_active"]
    )

def get_users(
    skip: int = 0,
    limit: int = 10
):
    query = SELECT_USER
    params = {'skip': skip, 'limit': limit}

    query += " ORDER BY id LIMIT :limit OFFSET :skip"

    with engine.begin() as conn:
        rows = conn.execute(
            text(
                query
            ), params
        ).mappings().all()

        users = [UserResponse.model_validate(dict(row)) for row in rows]

        return users
def get_auth_user_by_id(user_id: int) -> UserResponse:
    query = SELECT_USER;
    query += " where id = :user_id"
    params = {"user_id": user_id}

    with engine.connect() as conn:
        row = conn.execute(
            text(
                query
            ),
            params
        ).mappings().one_or_none()

        if row is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        if not row["is_active"]:
            raise HTTPException(
                status_code=403,
                detail="Account is inactive"
            )
        return UserResponse.model_validate(dict(row))
