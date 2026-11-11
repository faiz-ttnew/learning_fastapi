"""create tickets table

Revision ID: 72c3c8100e1a
Revises: 71b456857560
Create Date: 2026-11-10 12:27:33.563713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72c3c8100e1a'
down_revision: Union[str, Sequence[str], None] = '71b456857560'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.execute("""
        CREATE TABLE tickets (
            id INT NOT NULL AUTO_INCREMENT,
            title VARCHAR(150) NOT NULL,
            description TEXT NOT NULL,
            status ENUM('open','in_progress','resolved','closed') NOT NULL DEFAULT 'open',
            priority ENUM('low','medium','high') NOT NULL DEFAULT 'medium',
            created_by INT NOT NULL,
            assigned_to INT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY idx_tickets_created_by (created_by),
            KEY idx_tickets_assigned_to (assigned_to),
            CONSTRAINT fk_tickets_created_by FOREIGN KEY (created_by) REFERENCES users(id),
            CONSTRAINT fk_tickets_assigned_to FOREIGN KEY (assigned_to) REFERENCES users(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)


def downgrade():
     op.execute("DROP TABLE tickets")
