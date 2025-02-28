"""Adding new encryption type in enum

Revision ID: db6e7b60cb0a
Revises: 701ddf55a1b4
Create Date: 2024-12-17 10:59:41.630340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic.context import get_context


# revision identifiers, used by Alembic.
revision: str = 'db6e7b60cb0a'
down_revision: Union[str, None] = '701ddf55a1b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check the database dialect
    dialect = get_context().dialect.name

    if dialect == 'sqlite':
        # Skip execution for SQLite
        print("Skipping this migration for SQLite.")
        return

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('encryption_key', 'key_type',
               existing_type=sa.VARCHAR(length=18),
               type_=sa.Enum('MSG_PROTECT_SHIELD', 'MSG_PROTECT_PLUGIN', 'CRDS_PROTECT_GUARDRAIL', name='encryptionkeytype'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # Check the database dialect
    dialect = get_context().dialect.name

    if dialect == 'sqlite':
        # Skip execution for SQLite
        print("Skipping downgrade for SQLite.")
        return

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('encryption_key', 'key_type',
               existing_type=sa.Enum('MSG_PROTECT_SHIELD', 'MSG_PROTECT_PLUGIN', 'CRDS_PROTECT_GUARDRAIL', name='encryptionkeytype'),
               type_=sa.VARCHAR(length=18),
               existing_nullable=False)
    # ### end Alembic commands ###
