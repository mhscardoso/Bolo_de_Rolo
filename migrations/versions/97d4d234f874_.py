"""empty message

Revision ID: 97d4d234f874
Revises: 
Create Date: 2022-01-27 19:06:19.666565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97d4d234f874'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=70), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('cpf', sa.String(length=11), nullable=True),
    sa.Column('tel', sa.String(length=11), nullable=True),
    sa.Column('endereco', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('cart',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produto',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=30), nullable=True),
    sa.Column('sabor', sa.String(length=30), nullable=True),
    sa.Column('cod', sa.String(), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.Column('fabricacao', sa.String(length=10), nullable=True),
    sa.Column('pedido', sa.Boolean(), nullable=True),
    sa.Column('cart_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cod')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('produto')
    op.drop_table('cart')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###