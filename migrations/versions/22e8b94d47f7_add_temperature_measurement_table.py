"""add temperature measurement table

Revision ID: 22e8b94d47f7
Revises: 
Create Date: 2015-09-13 18:18:01.681040

"""

# revision identifiers, used by Alembic.
revision = '22e8b94d47f7'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temperature_measurements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_name', sa.String(length=128), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_temperature_measurements')),
    mysql_charset='utf8',
    mysql_collate='utf8_general_ci',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_sensor_name_timestamp', 'temperature_measurements', ['sensor_name', 'timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_sensor_name_timestamp', table_name='temperature_measurements')
    op.drop_table('temperature_measurements')
    ### end Alembic commands ###
