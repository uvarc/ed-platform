"""empty message

Revision ID: df361a922e41
Revises: e0a08c6a0885
Create Date: 2017-10-24 11:52:39.692663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

from ed_platform.models import Participant

revision = 'df361a922e41'
down_revision = 'e0a08c6a0885'
branch_labels = None
depends_on = None


def upgrade():

    bind = op.get_bind()
    session = Session(bind=bind)

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant', sa.Column('new_account', sa.Boolean(), nullable=True))
    op.add_column('participant', sa.Column('use_gravatar', sa.Boolean(), nullable=True))

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participant', 'use_gravatar')
    op.drop_column('participant', 'new_account')
    # ### end Alembic commands ###
