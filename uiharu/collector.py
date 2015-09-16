import logging

from temperusb.temper import TemperHandler


log = logging.getLogger(__name__)


class TemperatureCollector(object):
    """Keeps track of a USB temperature sensor/s and saves measurements.
    """

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
