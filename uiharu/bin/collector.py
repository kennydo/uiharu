from __future__ import print_function

import argparse
import logging.config
import socket
import sys
import datetime

from influxdb import InfluxDBClient

from uiharu.collector import MeasurementCollector
from uiharu.config import ConfigAction
from uiharu.periodic_sleeper import PeriodicSleeper


_logging_config = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'null': {
            'class': 'logging.NullHandler',
        }
    },
    loggers={
        '': {
            'handlers': ['console'],
            'level': logging.INFO,
        },
        'temperusb': {
            'level': logging.WARN,
        },
    },
)
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
        '--config',
        action=ConfigAction,
        help="The location of the JSON config file",
    )
    parser.add_argument(
        '--hostname',
        default=hostname,
        help="The name to save collector measurements under. Defaults to this host's hostname ({0})".format(hostname),
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
        ) for name, value in measurements.iteritems()
    ]


def main():
    args = parse_cli_args()
    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("Debug mode enabled")

    if not args.config:
        print("Error: A config path must be specified", file=sys.stderr)
        sys.exit(1)

    log.info("Using sensor name: %s", args.hostname)

    log.info("Connecting to database")
    influxdb_client = InfluxDBClient(
        host=args.config['INFLUXDB_HOST'],
        port=args.config['INFLUXDB_PORT'],
        database=args.config['INFLUXDB_DATABASE'],
        username=args.config['INFLUXDB_USERNAME'],
        password=args.config['INFLUXDB_PASSWORD'],
        ssl=args.config['INFLUXDB_SSL'],
    )

    log.info("Starting temperature collector with a collection period of %f seconds", args.period)
    collector = MeasurementCollector()
    periodic_sleeper = PeriodicSleeper(args.period)

    log.info("Running the collector")
    while True:
        timestamp = datetime.datetime.utcnow()
        sensor_measurement = collector.get_measurements()

        if not sensor_measurement:
            log.error("Could not fetch temperature. Sleeping until next collection period.")
            periodic_sleeper.sleep_until_next_period()
            continue

        log.info("Collected the measurement: %r", sensor_measurement)
        influxdb_points = create_influxdb_points_body(
            args.hostname,
            sensor_measurement._asdict(),
            timestamp=timestamp,
        )
        influxdb_client.write_points(influxdb_points)

        periodic_sleeper.sleep_until_next_period()


if __name__ == "__main__":
    main()
