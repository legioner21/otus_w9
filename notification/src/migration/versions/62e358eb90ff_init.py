"""init

Revision ID: 62e358eb90ff
Revises: 
Create Date: 2024-01-30 12:18:35.284506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62e358eb90ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='notification'
    )
    op.create_index(op.f('ix_notification_notification_id'), 'notification', ['id'], unique=False, schema='notification')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_notification_notification_id'), table_name='notification', schema='notification')
    op.drop_table('notification', schema='notification')
    # ### end Alembic commands ###
