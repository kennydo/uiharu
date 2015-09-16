from __future__ import print_function

import argparse
import datetime
import logging.config
import socket
import sys

import sqlalchemy as sa

from uiharu.collector import TemperatureCollector
from uiharu.config import ConfigAction
from uiharu.periodic_sleeper import PeriodicSleeper
from uiharu.models import TemperatureMeasurement


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
        help="How often to collect temperature data (in seconds)",
    )
    parser.add_argument(
        '--config',
        action=ConfigAction,
        help="The location of the JSON config file",
    )
    parser.add_argument(
        '--sensor-name',
        default=hostname,
        help="The name to save collector measurements under. Defaults to this host's hostname ({0})".format(hostname),
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Enable debug mode",
    )
    return parser.parse_args()


def main():
    args = parse_cli_args()
    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("Debug mode enabled")

    if not args.config:
        print("Error: A config path must be specified", file=sys.stderr)
        sys.exit(1)

    log.info("Using sensor name: %s", args.sensor_name)

    log.info("Connecting to database")
    engine = sa.create_engine(args.config['sqlalchemy_connection_url'])
    Session = sa.orm.sessionmaker(bind=engine)

    log.info("Starting temperature collector with a collection period of %f seconds", args.period)
    collector = TemperatureCollector()
    periodic_sleeper = PeriodicSleeper(args.period)

    log.info("Running the collector")
    while True:
        temperature = collector.get_temperature()

        if not temperature:
            log.error("Could not fetch temperature. Sleeping until next collection period.")
            periodic_sleeper.sleep_until_next_period()
            continue

        log.info("Collected the temperature in Celsius: %f", temperature)
        measurement = TemperatureMeasurement(
            sensor_name=args.sensor_name,
            timestamp=datetime.datetime.utcnow(),
            value=temperature,
        )
        session = Session()
        session.add(measurement)
        session.commit()

        periodic_sleeper.sleep_until_next_period()


if __name__ == "__main__":
    main()
