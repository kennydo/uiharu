import logging
import time


log = logging.getLogger(__name__)


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
        log.debug("Sleeping for %f seconds", time_to_sleep)
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
