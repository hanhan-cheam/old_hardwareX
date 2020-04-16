"""empty message

Revision ID: 74c661758f02
Revises: b680952e7856
Create Date: 2020-04-16 11:40:54.442267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74c661758f02'
down_revision = 'b680952e7856'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fullname', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'fullname')
    # ### end Alembic commands ###
