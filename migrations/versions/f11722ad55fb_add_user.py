"""add user

Revision ID: f11722ad55fb
Revises: 905ffdcff75d
Create Date: 2021-06-08 09:10:52.399637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f11722ad55fb'
down_revision = '905ffdcff75d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conference',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('short_name', sa.String(length=10), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.Column('path', sa.String(length=50), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_name')
    )
    op.create_table('app_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('is_editor', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'app_user', ['username'], unique=True)
    op.add_column('log', sa.Column('conference_id', sa.Integer(), nullable=True))
    op.add_column('log', sa.Column('app_user_id', sa.Integer(), nullable=True))
    op.add_column('log', sa.Column('status', sa.String(length=25), nullable=True))
    op.create_foreign_key('log_conference_id_fkey', 'log', 'conference', ['conference_id'], ['id'])
    op.create_foreign_key('log_user_id_fkey', 'log', 'app_user', ['app_user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('log_conference_id_fkey', 'log', type_='foreignkey')
    op.drop_constraint('log_user_id_fkey', 'log', type_='foreignkey')
    op.drop_column('log', 'app_user_id')
    op.drop_column('log', 'conference_id')
    op.drop_column('log', 'status')
    op.drop_index(op.f('ix_user_username'), table_name='app_user')
    op.drop_table('app_user')
    op.drop_table('conference')
    # ### end Alembic commands ###