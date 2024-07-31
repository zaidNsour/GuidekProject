"""Initial migration.

Revision ID: e8a7b28dfb4a
Revises: 
Create Date: 2024-07-30 15:32:24.994694

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'e8a7b28dfb4a'
down_revision = None
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    bind = op.get_bind()
    insp = Inspector.from_engine(bind)
    columns = [col['name'] for col in insp.get_columns(table_name)]
    return column_name in columns


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verified', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('verification_code', sa.Integer(), nullable=True))
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), nullable=False))
        batch_op.drop_column('verification_code')
        batch_op.drop_column('verified')

    # ### end Alembic commands ###
