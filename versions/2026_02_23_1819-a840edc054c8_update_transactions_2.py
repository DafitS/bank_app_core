"""Update Transactions 2

Revision ID: a840edc054c8
Revises: e4bf3c17aa80
Create Date: 2026-02-23 18:19:16.704690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a840edc054c8'
down_revision: Union[str, Sequence[str], None] = 'e4bf3c17aa80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Zamień user_id na UUID, konwertując dane jeśli trzeba
    op.alter_column(
        "accounts",
        "user_id",
        type_=sa.dialects.postgresql.UUID(),
        postgresql_using="user_id::uuid"
    )

def downgrade():
    # Cofnięcie zmiany
    op.alter_column(
        "accounts",
        "user_id",
        type_=sa.String(36),
        postgresql_using="user_id::varchar"
    )