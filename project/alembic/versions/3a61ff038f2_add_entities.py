"""Add entities

Revision ID: 3a61ff038f2
Revises: 33ffbd43f2e
Create Date: 2015-07-14 17:23:30.957326

"""

# revision identifiers, used by Alembic.
revision = '3a61ff038f2'
down_revision = '33ffbd43f2e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import project
from project.auth.models import User


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('surname', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('role', project.lib.orm.types.TypeEnum(User.ROLE), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('short_description', sa.String(length=300), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('name_in_url', sa.String(length=50), nullable=True),
    sa.Column('visits', sa.Integer(), nullable=True),
    sa.Column('salary', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('keywords', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancy')
    op.drop_table('users')
    op.drop_table('category')
    ### end Alembic commands ###