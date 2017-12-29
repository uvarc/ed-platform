"""empty message

Revision ID: ba62e09f66cb
Revises: 8453020a4135
Create Date: 2017-12-28 20:25:16.087202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba62e09f66cb'
down_revision = '8453020a4135'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_message', sa.Column('type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('email_message', 'type')
    # ### end Alembic commands ###