import sqlalchemy as sa
from flask.ext.sqlalchemy import SQLAlchemy


meta = sa.MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
db = SQLAlchemy()


class TemperatureMeasurement(db.Model):
    """A single temperature measurement"""

    __tablename__ = 'temperature_measurements'

    id = sa.Column(sa.Integer, primary_key=True)
    # The name of the specific sensor this measurement came from
    sensor_name = sa.Column(sa.String(length=128), nullable=False)
    # This timestamp is always in UTC
    timestamp = sa.Column(sa.DateTime, nullable=False)
    # The value is stored in Celsius
    value = sa.Column(sa.Float, nullable=False)

    __table_args__ = (
        sa.Index('ix_sensor_name_timestamp', sensor_name, timestamp),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8',
            'mysql_collate': 'utf8_general_ci',
        }
    )
