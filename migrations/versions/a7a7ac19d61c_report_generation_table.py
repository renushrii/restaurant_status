"""report generation table

Revision ID: a7a7ac19d61c
Revises: d3f295e2fe7a
Create Date: 2023-07-30 14:53:10.179474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7a7ac19d61c'
down_revision = 'd3f295e2fe7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('report_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('Running', 'Completed', name='reportstatusenum'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report_status')
    # ### end Alembic commands ###
