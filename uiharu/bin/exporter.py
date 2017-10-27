import argparse
import logging.config
import socket
import sys
import datetime

import prometheus_client

from uiharu import metrics
from uiharu.collectors import MeasurementCollector
from uiharu.config import ConfigAction
from uiharu.periodic_sleeper import PeriodicSleeper


_logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
logging.config.dictConfig(_logging_config)
log = logging.getLogger(__name__)


def parse_cli_args():
    """Parse the CLI arguments and return the populated namespace."""
    hostname = socket.gethostname()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--period',
        type=float,
        default=60.0,
        help="How often to collect data (in seconds)",
    )
    parser.add_argument(
        '--metrics-port',
        type=int,
        default=9400,
        help="Port for prometheus metrics",
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Enable debug mode",
    )
    return parser.parse_args()


def create_influxdb_points_body(hostname, measurements, timestamp):
    """
    :param str hostname: the hostname
    :param dict measurements: a mapping of str measurement names to float values
    :param timestamp: Unix timestamp in seconds
    :type timestamp: :class:`datetime.datetime`
    :return: a `list` of `dict`s
    """
    return [
        dict(
            measurement=name,
            tags=dict(
                host=hostname,
            ),
            time=timestamp,
            fields=dict(
                value=value,
            )
        ) for name, value in measurements.items()
    ]


def main():
    args = parse_cli_args()
    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("Debug mode enabled")

    log.info("Starting temperature collector with a collection period of %f seconds", args.period)
    collector = MeasurementCollector()
    periodic_sleeper = PeriodicSleeper(args.period)

    log.info("Running the metrics server on port %s", args.metrics_port)
    prometheus_client.start_http_server(args.metrics_port)

    while True:
        measurement = collector.get_measurements()

        if not measurement:
            log.error("Could not fetch temperature. Sleeping until next collection period.")
            periodic_sleeper.sleep_until_next_period()
            continue

        log.info("Collected the measurement: %r", measurement)
        metrics.SENSOR_TEMPERATURE_CELSIUS.set(measurement.temperature_c)
        metrics.SENSOR_TEMPERATURE_FAHRENHEIT.set(measurement.temperature_f)
        metrics.SENSOR_ATMOSPHERIC_PRESSURE_PASCALS.set(measurement.atmospheric_pressure_pascals)
        metrics.SENSOR_RELATIVE_HUMIDITY_PERCENTAGE.set(measurement.relative_humidity_percentage)
        metrics.SENSOR_COLLECTIONS_TOTAL.inc()

        periodic_sleeper.sleep_until_next_period()


if __name__ == "__main__":
    main()
