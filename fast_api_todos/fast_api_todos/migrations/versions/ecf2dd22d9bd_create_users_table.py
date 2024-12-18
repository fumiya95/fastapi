"""create Users table

Revision ID: ecf2dd22d9bd
Revises: f11aa05dc0ef
Create Date: 2024-12-11 12:03:29.636785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ecf2dd22d9bd'
down_revision: Union[str, None] = 'f11aa05dc0ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('hashed_password', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('role', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.add_column('todos', sa.Column('user_id', sa.Integer(), nullable=True))
    op.alter_column('todos', 'description',
               existing_type=mysql.TEXT(collation='utf8mb4_unicode_ci'),
               nullable=True)
    op.create_foreign_key(None, 'todos', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.alter_column('todos', 'description',
               existing_type=mysql.TEXT(collation='utf8mb4_unicode_ci'),
               nullable=False)
    op.drop_column('todos', 'user_id')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
