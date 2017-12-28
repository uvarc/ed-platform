"""empty message

Revision ID: 8453020a4135
Revises: 5007b5f4af73
Create Date: 2017-12-28 12:20:44.435761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8453020a4135'
down_revision = '5007b5f4af73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant_session', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participant_session', 'confirmed')
    # ### end Alembic commands ###
