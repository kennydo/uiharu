import datetime as dt
import logging

import sqlalchemy as sa
from flask import abort, Blueprint, jsonify, request

import uiharu.utils
from uiharu.models import db, TemperatureMeasurement


api = Blueprint('api', __name__)
log = logging.getLogger(__name__)


@api.route('/sensors')
def list_sensors():
    """Return a list of sensor names"""
    sensor_names = [
        row[0] for row in
        db.session.query(sa.distinct(TemperatureMeasurement.sensor_name)).all()
    ]

    return jsonify({
        'sensors': [{'name': name} for name in sensor_names],
    })


@api.route('/sensors/<sensor_name>/measurements')
def list_sensor_data(sensor_name):
    """Return the measurements recorded by the given sensor name.
    Each measurement has a timestamp (in seconds since UTC epoch) and the
    Fahrenheit value of the measurement.

    Params:
        start_time: float seconds since the epoch UTC
        end_time: float seconds since the epoch UTC, defaults to now
    """
    if 'start_time' not in request.args:
        abort(400)

    start_time_in_seconds = float(request.args['start_time'])
    start_time = dt.datetime.utcfromtimestamp(start_time_in_seconds)

    if 'end_time' in request.args:
        end_time_in_seconds = float(request.args['end_time'])
        end_time = dt.datetime.utcfromtimestamp(end_time_in_seconds)
    else:
        end_time = dt.datetime.utcnow()

    query = db.session.query(
          TemperatureMeasurement.timestamp,
          sa.func.avg(TemperatureMeasurement.value),
        ).\
        filter(TemperatureMeasurement.sensor_name == sensor_name).\
        filter(TemperatureMeasurement.timestamp >= start_time).\
        filter(TemperatureMeasurement.timestamp <= end_time).\
        group_by(
          sa.func.year(TemperatureMeasurement.timestamp),
          sa.func.month(TemperatureMeasurement.timestamp),
          sa.func.day(TemperatureMeasurement.timestamp),
          sa.func.hour(TemperatureMeasurement.timestamp)
        ).\
        order_by(TemperatureMeasurement.timestamp.desc())
    measurements = []

    for row in query.all():
        measurements.append({
            'timestamp': uiharu.utils.seconds_since_epoch(row[0]),
            'value': uiharu.utils.celsius_to_fahrenheit(row[1]),
        })

    return jsonify({
        'measurements': measurements,
    })
