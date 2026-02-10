"""fresh schema

Revision ID: 5125bcb0d5c2
Revises: 
Create Date: 2026-01-01 21:42:16.338412

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5125bcb0d5c2'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Drop foreign keys BEFORE changing types
    op.drop_constraint(
        "transactions_account_id_from_fkey",
        "transactions",
        type_="foreignkey"
    )
    op.drop_constraint(
        "transactions_account_id_to_fkey",
        "transactions",
        type_="foreignkey"
    )

    # 2. Add new column
    op.add_column(
        'accounts',
        sa.Column('account_number', sa.Numeric(precision=26, scale=0), nullable=False)
    )

    # 3. Change types in transactions FIRST
    op.alter_column(
        'transactions', 'account_id_from',
        existing_type=sa.BIGINT(),
        type_=sa.String(length=12),
        existing_nullable=False
    )
    op.alter_column(
        'transactions', 'account_id_to',
        existing_type=sa.BIGINT(),
        type_=sa.String(length=12),
        existing_nullable=False
    )

    # 4. Change type in accounts
    op.alter_column(
        'accounts', 'account_id',
        existing_type=sa.BIGINT(),
        type_=sa.String(length=12),
        existing_nullable=False,
        existing_server_default=None  # usuwamy sekwencję
    )

    # 5. Replace unique constraint
    op.drop_constraint(op.f('accounts_account_id_key'), 'accounts', type_='unique')
    op.create_unique_constraint(None, 'accounts', ['account_number'])

    # 6. Recreate foreign keys
    op.create_foreign_key(
        "transactions_account_id_from_fkey",
        "transactions", "accounts",
        ["account_id_from"], ["account_id"],
        ondelete="CASCADE"
    )
    op.create_foreign_key(
        "transactions_account_id_to_fkey",
        "transactions", "accounts",
        ["account_id_to"], ["account_id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""

    # 1. Drop recreated FKs
    op.drop_constraint(
        "transactions_account_id_from_fkey",
        "transactions",
        type_="foreignkey"
    )
    op.drop_constraint(
        "transactions_account_id_to_fkey",
        "transactions",
        type_="foreignkey"
    )

    # 2. Restore old types in transactions
    op.alter_column(
        'transactions', 'account_id_from',
        existing_type=sa.String(length=12),
        type_=sa.BIGINT(),
        existing_nullable=False
    )
    op.alter_column(
        'transactions', 'account_id_to',
        existing_type=sa.String(length=12),
        type_=sa.BIGINT(),
        existing_nullable=False
    )

    # 3. Restore unique constraint
    op.drop_constraint(None, 'accounts', type_='unique')
    op.create_unique_constraint(
        op.f('accounts_account_id_key'),
        'accounts',
        ['account_id'],
        postgresql_nulls_not_distinct=False
    )

    # 4. Restore old type in accounts
    op.alter_column(
        'accounts', 'account_id',
        existing_type=sa.String(length=12),
        type_=sa.BIGINT(),
        existing_nullable=False,
        existing_server_default=sa.text("nextval('accounts_account_id_seq'::regclass)")
    )

    # 5. Drop new column
    op.drop_column('accounts', 'account_number')
