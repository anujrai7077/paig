"""added paig api key and encryption level

Revision ID: a9c87d84b974
Revises: f36705415cd9
Create Date: 2025-04-14 14:29:35.779715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import core.db_models.utils


# revision identifiers, used by Alembic.
revision: str = 'a9c87d84b974'
down_revision: Union[str, None] = 'f36705415cd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paig_level1_encryption_key',
    sa.Column('key_id', sa.String(length=255), nullable=False),
    sa.Column('created_by_id', sa.String(length=20), nullable=True),
    sa.Column('updated_by_id', sa.String(length=20), nullable=True),
    sa.Column('paig_key_value', sa.String(length=1024), nullable=False),
    sa.Column('key_status', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_id')
    )
    op.create_index(op.f('ix_paig_level1_encryption_key_create_time'), 'paig_level1_encryption_key', ['create_time'], unique=False)
    op.create_index(op.f('ix_paig_level1_encryption_key_id'), 'paig_level1_encryption_key', ['id'], unique=False)
    op.create_index(op.f('ix_paig_level1_encryption_key_update_time'), 'paig_level1_encryption_key', ['update_time'], unique=False)
    op.create_table('paig_level2_encryption_key',
    sa.Column('key_id', sa.String(length=255), nullable=False),
    sa.Column('created_by_id', sa.String(length=20), nullable=True),
    sa.Column('updated_by_id', sa.String(length=20), nullable=True),
    sa.Column('paig_key_value', sa.String(length=1024), nullable=False),
    sa.Column('key_status', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_id')
    )
    op.create_index(op.f('ix_paig_level2_encryption_key_create_time'), 'paig_level2_encryption_key', ['create_time'], unique=False)
    op.create_index(op.f('ix_paig_level2_encryption_key_id'), 'paig_level2_encryption_key', ['id'], unique=False)
    op.create_index(op.f('ix_paig_level2_encryption_key_update_time'), 'paig_level2_encryption_key', ['update_time'], unique=False)
    op.create_table('paig_api_key',
    sa.Column('key_id', sa.String(length=255), nullable=False),
    sa.Column('tenant_id', sa.String(length=255), nullable=False),
    sa.Column('api_key_name', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_by_id', sa.String(length=20), nullable=True),
    sa.Column('updated_by_id', sa.String(length=20), nullable=True),
    sa.Column('key_status', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('last_used_on', sa.DateTime(), nullable=True),
    sa.Column('api_key_masked', sa.String(length=255), nullable=False),
    sa.Column('api_key_encrypted', sa.String(length=512), nullable=True),
    sa.Column('expiry', sa.DateTime(), nullable=True),
    sa.Column('never_expire', sa.Boolean(), nullable=False),
    sa.Column('api_scope_id', sa.String(length=255), nullable=True),
    sa.Column('version', sa.String(length=255), nullable=True),
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['ai_application.id'], name='fk_paig_api_key_application_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_id')
    )
    op.create_index(op.f('ix_paig_api_key_create_time'), 'paig_api_key', ['create_time'], unique=False)
    op.create_index(op.f('ix_paig_api_key_id'), 'paig_api_key', ['id'], unique=False)
    op.create_index(op.f('ix_paig_api_key_update_time'), 'paig_api_key', ['update_time'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_paig_api_key_update_time'), table_name='paig_api_key')
    op.drop_index(op.f('ix_paig_api_key_id'), table_name='paig_api_key')
    op.drop_index(op.f('ix_paig_api_key_create_time'), table_name='paig_api_key')
    op.drop_table('paig_api_key')
    op.drop_index(op.f('ix_paig_level2_encryption_key_update_time'), table_name='paig_level2_encryption_key')
    op.drop_index(op.f('ix_paig_level2_encryption_key_id'), table_name='paig_level2_encryption_key')
    op.drop_index(op.f('ix_paig_level2_encryption_key_create_time'), table_name='paig_level2_encryption_key')
    op.drop_table('paig_level2_encryption_key')
    op.drop_index(op.f('ix_paig_level1_encryption_key_update_time'), table_name='paig_level1_encryption_key')
    op.drop_index(op.f('ix_paig_level1_encryption_key_id'), table_name='paig_level1_encryption_key')
    op.drop_index(op.f('ix_paig_level1_encryption_key_create_time'), table_name='paig_level1_encryption_key')
    op.drop_table('paig_level1_encryption_key')
    # ### end Alembic commands ###
