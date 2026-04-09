"""users orm update structure

Revision ID: 016e6da86607
Revises: cb6e56d57f87
Create Date: 2026-03-21 20:54:49.637495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '016e6da86607'
down_revision: Union[str, Sequence[str], None] = 'cb6e56d57f87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
