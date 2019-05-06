"""add log table

Revision ID: 905ffdcff75d
Revises: 
Create Date: 2019-05-06 17:43:07.164737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '905ffdcff75d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('report', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_log_filename'), 'log', ['filename'], unique=False)
    op.create_index(op.f('ix_log_timestamp'), 'log', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_log_timestamp'), table_name='log')
    op.drop_index(op.f('ix_log_filename'), table_name='log')
    op.drop_table('log')
    # ### end Alembic commands ###
