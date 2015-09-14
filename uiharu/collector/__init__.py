import logging
import time

from temperusb.temper import TemperHandler


# The number of seconds between each measurement collection
DEFAULT_COLLECTION_PERIOD = 60.0

log = logging.getLogger(__name__)


class TemperatureCollector(object):
    """Keeps track of a USB temperature sensor/s and saves measurements.
    """

    def __init__(self, collection_period=DEFAULT_COLLECTION_PERIOD):
        """

        :param float collection_period: the seconds to sleep between collections
        :return:
        """
        self.collection_period = collection_period

    def get_temperature(self):
        """Get the degrees Celsius of the first (and only) temperature sensor, or return `None` if no sensor exists.

        :return: the degrees Celsius of the temperature reading, or None if no devices
        :rtype: float
        """
        devices = TemperHandler().get_devices()

        if not devices:
            return None

        # Only fetch the temperature from the first device
        return devices[0].get_temperature()


    def run(self):
        """The main loop that collects the temperature, does stuff with it, then repeats."""
        periodic_sleeper = PeriodicSleeper(self.collection_period)

        while True:
            temperature = self.get_temperature()

            if not temperature:
                log.error("Could not fetch temperature. Sleeping until next collection period.")
                periodic_sleeper.sleep_until_next_period()
                continue
            print temperature
            log.info("Collected the following temperature: %d", temperature)
            periodic_sleeper.sleep_until_next_period()


class PeriodicSleeper(object):
    def __init__(self, period):
        """
        :param float period: desired period length in seconds
        """
        self.period = period

        # The timestamp of the last
        self.last_time_awakened = time.time()

    def sleep_until_next_period(self):
        """Sleep until the next period."""
        time_to_sleep = self.time_until_next_period()
        log.info("Sleeping %d seconds", time_to_sleep)
        time.sleep(time_to_sleep)
        self.last_time_awakened = time.time()

    def time_until_next_period(self):
        """The time in seconds until the start of the next period. If we're already past that point, returns 0.

        :returns: seconds until the next period
        :rtype: float
        """
        now = time.time()
        next_awakening = self.last_time_awakened + self.period
        if now > next_awakening:
            return 0

        return next_awakening - now
