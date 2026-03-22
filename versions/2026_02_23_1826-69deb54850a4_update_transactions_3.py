"""Update Transactions 3

Revision ID: 69deb54850a4
Revises: a840edc054c8
Create Date: 2026-02-23 18:26:45.151472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69deb54850a4'
down_revision: Union[str, Sequence[str], None] = 'a840edc054c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # zmieniamy tylko account_id i account_number, user_id zostaje UUID
    op.alter_column('accounts', 'account_id',
               existing_type=sa.VARCHAR(length=12),
               type_=sa.String(length=36),
               existing_nullable=False)
    op.alter_column('accounts', 'account_number',
               existing_type=sa.NUMERIC(precision=26, scale=0),
               type_=sa.String(length=32),
               existing_nullable=False)
    # nie ruszamy user_id, bo musi zostać UUID
    # op.drop_constraint(...) -> usuń ten drop