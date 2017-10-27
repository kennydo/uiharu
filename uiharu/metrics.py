from prometheus_client import Counter
from prometheus_client import Gauge


SENSOR_TEMPERATURE_CELSIUS = Gauge(
    'uiharu_sensor_temperature_celsius',
    'Temperature recorded by the sensor in Celsius',
)

SENSOR_TEMPERATURE_FAHRENHEIT = Gauge(
    'uiharu_sensor_temperature_fahrenheit',
    'Temperature recorded by the sensor in Fahrenheit',
)

SENSOR_ATMOSPHERIC_PRESSURE_PASCALS = Gauge(
    'uiharu_sensor_atmospheric_pressure_pascals',
    'Atmospheric pressure recorded by the sensor in Pascals',
)

SENSOR_RELATIVE_HUMIDITY_PERCENTAGE = Gauge(
    'uiharu_relative_humidity_percentage',
    'Relative humidity recorded by the sensor in percentage',
)

SENSOR_COLLECTIONS_TOTAL = Counter(
    'uiharu_sensor_collections_total',
    'Number of times measurements have been collected from the sensor',
)
