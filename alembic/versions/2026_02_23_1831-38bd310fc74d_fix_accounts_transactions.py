"""Fix accounts transactions

Revision ID: 38bd310fc74d
Revises: 69deb54850a4
Create Date: 2026-02-23 18:31:20.989218
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38bd310fc74d'
down_revision = '69deb54850a4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema: fix user_id type and foreign key."""
    # Usuń najpierw constraint FK, żeby zmienić typ
    op.drop_constraint('accounts_user_id_fkey', 'accounts', type_='foreignkey')

    # Zamiana typu user_id na VARCHAR(36)
    op.alter_column(
    'accounts',
    'user_id',
    existing_type=sa.String(length=36),
    type_=sa.UUID(),
    existing_nullable=False
)

    # Dodanie FK ponownie (zakładamy, że users.user_id też jest VARCHAR(36))
    op.create_foreign_key(
    'accounts_user_id_fkey',
    'accounts',
    'users',
    ['user_id'],
    ['user_id'],
    ondelete='RESTRICT'
)


def downgrade() -> None:
    """Downgrade schema: przywrócenie UUID i FK."""
    # Usuń FK
    op.drop_constraint('accounts_user_id_fkey', 'accounts', type_='foreignkey')

    # Przywrócenie UUID
    op.alter_column(
        'accounts',
        'user_id',
        existing_type=sa.String(length=36),
        type_=sa.UUID(),
        existing_nullable=False
    )

    # Przywrócenie FK
    op.create_foreign_key(
        'accounts_user_id_fkey',
        'accounts',
        'users',
        ['user_id'],
        ['user_id'],
        ondelete='RESTRICT'
    )