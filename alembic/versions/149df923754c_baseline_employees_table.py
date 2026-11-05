"""baseline employees table

Revision ID: 149df923754c
Revises: 
Create Date: 2026-11-05 16:17:30.206827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '149df923754c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            department VARCHAR(100) NOT NULL,
            salary DECIMAL(12, 2) NOT NULL,
            city VARCHAR(100) NOT NULL,
            pincode VARCHAR(6) NOT NULL,
            skills JSON NOT NULL,
            joining_date DATE NOT NULL,

            PRIMARY KEY (id),
            CONSTRAINT uk_employees_email UNIQUE (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)


def downgrade() -> None:
    raise RuntimeError(
        "Baseline rollback is disabled to preserve employee data"
    )
