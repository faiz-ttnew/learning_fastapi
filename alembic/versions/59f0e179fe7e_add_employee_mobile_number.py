"""add employee mobile number

Revision ID: 59f0e179fe7e
Revises: 149df923754c
Create Date: 2026-11-05 16:28:08.136253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59f0e179fe7e'
down_revision: Union[str, Sequence[str], None] = '149df923754c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op


def upgrade():
    op.execute("""
        ALTER TABLE employees
        ADD COLUMN mobile_number VARCHAR(20) NULL
    """)


def downgrade():
    op.execute("""
        ALTER TABLE employees
        DROP COLUMN mobile_number
    """)
