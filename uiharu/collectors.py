import logging
from typing import NamedTuple

from uiharu.utils import celsius_to_fahrenheit
from uiharu.vendor.Adafruit_BME280 import BME280


log = logging.getLogger(__name__)


class SensorMeasurement(NamedTuple):
    temperature_c: float
    temperature_f: float
    atmospheric_pressure_pascals: float
    relative_humidity_percentage: float


class MeasurementCollector(object):
    """Collects data from the BME280 sensor in a friendly format.

    The BME280 sensor returns the temperature in Celsius, the barometric pressure in Pascals,
    and the humidity in percent.
    """

    def get_measurements(self) -> SensorMeasurement:
        """Return a :class:`SensorMeasurement`.
        """
        sensor = BME280()

        temperature_c = sensor.read_temperature()
        temperature_f = celsius_to_fahrenheit(temperature_c)
        pressure = sensor.read_pressure()
        humidity = sensor.read_humidity()

        return SensorMeasurement(
            temperature_c=temperature_c,
            temperature_f=temperature_f,
            atmospheric_pressure_pascals=pressure,
            relative_humidity_percentage=humidity,
        )
