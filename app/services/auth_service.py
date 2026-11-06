from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password
from app.db.database import engine
from app.schemas.auth_schema import UserRegister, UserResponse
from app.common.enums import UserRole

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
