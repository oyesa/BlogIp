"""second Migration

Revision ID: 7cdd14df5895
Revises: 2dd2d1b2cd55
Create Date: 2022-05-18 12:39:30.757234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cdd14df5895'
down_revision = '2dd2d1b2cd55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('roles', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'bio',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.alter_column('users', 'bio',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('roles', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###