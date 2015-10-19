import datetime as dt


def celsius_to_fahrenheit(celsius):
    """Convert degrees Celsius to degrees Fahrenheit

    :param float celsius: a temperature in Celsius
    :return: a temperature in Fahrenheit
    :rtype: float
    """
    return celsius * 9.0/5.0 + 32.0


def seconds_since_epoch(timestamp):
    """The seconds since the UTC epoch of a given :class:`~datetime.datetime`
    timestamp

    :param timestamp: a timestamp as a (naive) datetime, implied UTC
    :type timestamp: :class:`~datetime.datetime`
    :returns: the seconds since UTC epoch of the given timestamp
    :rtype: float
    """
    epoch = dt.datetime.utcfromtimestamp(0)
    delta = timestamp - epoch
    return delta.total_seconds()
