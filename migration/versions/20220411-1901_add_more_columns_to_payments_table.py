"""add more columns to payments table

Revision ID: c675388bd0a8
Revises: ffaf97e34e03
Create Date: 2022-04-11 19:01:37.546506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c675388bd0a8'
down_revision = 'ffaf97e34e03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pairid', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_column('pairid')

    # ### end Alembic commands ###
