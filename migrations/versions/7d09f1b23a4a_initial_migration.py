"""Initial migration.

Revision ID: 7d09f1b23a4a
Revises: f85d307e4cd4
Create Date: 2024-08-20 16:25:35.900067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d09f1b23a4a'
down_revision = 'f85d307e4cd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('support', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.String(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('support', schema=None) as batch_op:
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###