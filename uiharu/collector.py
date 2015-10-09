import logging

from collections import namedtuple

from uiharu.vendor import Adafruit_BME280 as adafruit

log = logging.getLogger(__name__)
SensorMeasurement = namedtuple('SensorMeasurement', ['temperature', 'pressure', 'humidity'])


class MeasurementCollector(object):
    """Collects data from the BME280 sensor in a friendly format.

    The BME280 sensor returns the temperature in Celsius, the barometric pressure in Pascals,
    and the humidity in percent.
    """

    def get_measurements(self):
        """Return a :class:`SensorMeasurement`.
        """
        sensor = adafruit.BME280(mode=adafruit.BME280_OSAMPLE_8)
        temperature = sensor.read_temperature()
        pressure = sensor.read_pressure()
        humidity = sensor.read_humidity()

        return SensorMeasurement(
            temperature=temperature,
            pressure=pressure,
            humidity=humidity,
        )
