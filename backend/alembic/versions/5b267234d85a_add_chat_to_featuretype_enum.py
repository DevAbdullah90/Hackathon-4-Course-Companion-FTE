"""add_chat_to_featuretype_enum

Revision ID: 5b267234d85a
Revises: 25301b64af78
Create Date: 2026-02-14 14:21:27.436229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b267234d85a'
down_revision: Union[str, None] = '25301b64af78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Postgres specific: Add 'CHAT' to the enum
    op.execute("ALTER TYPE featuretype ADD VALUE 'CHAT'")


def downgrade() -> None:
    # Removing enum values is not supported in Postgres without dropping the type
    pass
