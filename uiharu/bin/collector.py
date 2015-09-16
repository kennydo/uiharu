import logging.config

from uiharu.collector import TemperatureCollector
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
        }
    },
)
logging.config.dictConfig(_logging_config)
log = logging.getLogger(__name__)

# The number of seconds between each measurement collection
COLLECTION_PERIOD = 60.0


def main():
    log.info("Starting temperature collector")
    collector = TemperatureCollector()
    periodic_sleeper = PeriodicSleeper(COLLECTION_PERIOD)

    log.info("Running the collector")
    while True:
        temperature = collector.get_temperature()

        if not temperature:
            log.error("Could not fetch temperature. Sleeping until next collection period.")
            periodic_sleeper.sleep_until_next_period()
            continue

        log.info("Collected the temperature in Celsius: %f", temperature)
        periodic_sleeper.sleep_until_next_period()


if __name__ == "__main__":
    main()
