# Uiharu

I was curious about the temperature of my room, so I got a BME280 sensor from Adafruit and connected it to my Raspberry Pi 2.

# Installation

First, create a virtual environment *with* system packages. The reading from the BME280 sensor requires a the `Adafruit_Python_GPIO` library, which requires system packages to be installed. Follow the instructions on https://github.com/adafruit/Adafruit_Python_GPIO.

Then, run the `setup.py` from this repository:
```
$ python setup.py install
```

This will add the necessary entry points to the virtual environment.

# Running

To run the collector, just activate the virtual environment and then run the `uiharu-collector` command, with a path to a config file passed in:
```
$ workon uiharu
$ uiharu-collector --config config/uiharu-prod.json
```

You an also run this under supervisord:
```
# /etc/supervisor/conf.d/uiharu.conf
[program:uiharu-collector]
command=/virtualenv/path/bin/uiharu-collector --config /some/path/config/uiharu-prod.json
autostart=true
autorestart=true
user=USERNAME_HERE
```
