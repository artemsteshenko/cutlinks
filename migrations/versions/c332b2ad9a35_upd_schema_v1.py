"""upd schema v1

Revision ID: c332b2ad9a35
Revises: 
Create Date: 2022-05-21 21:32:41.124143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c332b2ad9a35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clicks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(length=1000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('links',
    sa.Column('link_id', sa.String(length=5), nullable=False),
    sa.Column('link', sa.String(length=1000), nullable=True),
    sa.Column('username', sa.String(length=1000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('link_id')
    )
    op.create_table('treelinks',
    sa.Column('link_id', sa.String(length=6), nullable=False),
    sa.Column('link', sa.String(length=1000), nullable=True),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.Column('username', sa.String(length=1000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('link_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('treelinks')
    op.drop_table('links')
    op.drop_table('clicks')
    # ### end Alembic commands ###
