"""empty message

Revision ID: b8255a026207
Revises: c2994ade3196
Create Date: 2022-03-13 14:14:44.225499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8255a026207'
down_revision = 'c2994ade3196'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'file', ['filename'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'file', type_='unique')
    # ### end Alembic commands ###
