"""create authentication users table

Revision ID: 71b456857560
Revises: 59f0e179fe7e
Create Date: 2026-11-06 09:45:35.516910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71b456857560'
down_revision: Union[str, Sequence[str], None] = '59f0e179fe7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE users (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(1024) NOT NULL,
            role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

            PRIMARY KEY (id),
            CONSTRAINT uk_users_email UNIQUE (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)


def downgrade() -> None:
    raise RuntimeError(
        "DROP TABLE users"
    )
