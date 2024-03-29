"""init

Revision ID: 1a037856d60c
Revises: 
Create Date: 2024-01-30 09:50:45.873754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a037856d60c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('state', sa.String(), server_default='created', nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='order'
    )
    op.create_index(op.f('ix_order_order_id'), 'order', ['id'], unique=False, schema='order')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_order_id'), table_name='order', schema='order')
    op.drop_table('order', schema='order')
    # ### end Alembic commands ###
