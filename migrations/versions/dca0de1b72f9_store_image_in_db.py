"""store image in db

Revision ID: dca0de1b72f9
Revises: 410c795f3c03
Create Date: 2025-01-05 20:05:10.745668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dca0de1b72f9'
down_revision = '410c795f3c03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('barcode_image', sa.LargeBinary(), nullable=True))
        batch_op.add_column(sa.Column('qrcode_image', sa.LargeBinary(), nullable=True))

    with op.batch_alter_table('unique_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('barcode_image', sa.LargeBinary(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('unique_item', schema=None) as batch_op:
        batch_op.drop_column('barcode_image')

    with op.batch_alter_table('inventory_item', schema=None) as batch_op:
        batch_op.drop_column('qrcode_image')
        batch_op.drop_column('barcode_image')

    # ### end Alembic commands ###
