"""Initial migration.

Revision ID: f85d307e4cd4
Revises: 
Create Date: 2024-08-20 16:19:32.554203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f85d307e4cd4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('major_subject', schema=None) as batch_op:
        batch_op.drop_column('type')

    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.add_column(sa.Column('book', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('slides', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('course_plan', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.drop_column('course_plan')
        batch_op.drop_column('slides')
        batch_op.drop_column('book')

    with op.batch_alter_table('major_subject', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.VARCHAR(length=50), nullable=True))

    # ### end Alembic commands ###
