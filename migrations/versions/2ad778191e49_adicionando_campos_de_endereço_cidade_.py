"""Adicionando campos de endereço, cidade, estado e CEP

Revision ID: 2ad778191e49
Revises: 0c883984d523
Create Date: 2024-10-11 20:04:05.715165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ad778191e49'
down_revision = '0c883984d523'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('state', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('postal_code', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('postal_code')
        batch_op.drop_column('state')
        batch_op.drop_column('city')
        batch_op.drop_column('address')

    # ### end Alembic commands ###
