import logging

from collections import namedtuple

from uiharu.utils import celsius_to_fahrenheit
from uiharu.vendor import Adafruit_BME280 as adafruit


log = logging.getLogger(__name__)
SensorMeasurement = namedtuple('SensorMeasurement',
    ['temperature_c', 'temperature_f', 'pressure', 'humidity'])


class MeasurementCollector(object):
    """Collects data from the BME280 sensor in a friendly format.

    The BME280 sensor returns the temperature in Celsius, the barometric pressure in Pascals,
    and the humidity in percent.
    """

    def get_measurements(self):
        """Return a :class:`SensorMeasurement`.
        """
        sensor = adafruit.BME280(mode=adafruit.BME280_OSAMPLE_8)

        temperature_c = sensor.read_temperature()
        temperature_f = celsius_to_fahrenheit(temperature_c)
        pressure = sensor.read_pressure()
        humidity = sensor.read_humidity()

        return SensorMeasurement(
            temperature_c=temperature_c,
            temperature_f=temperature_f,
            pressure=pressure,
            humidity=humidity,
        )
