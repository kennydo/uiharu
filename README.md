# Uiharu

I was curious about the temperature of my room, so I got a BME280 sensor from Adafruit and connected it to my Raspberry Pi 2.

# Installation

First, create a Python 3.6 virtual environment. The reading from the BME280 sensor requires a the `Adafruit_Python_GPIO` library, which requires system packages to be installed. Follow the instructions on https://github.com/adafruit/Adafruit_Python_GPIO to install the system packages.

Then, install our dependencies and package:
```bash
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python setup.py install
```

This will add the necessary entry points to the virtual environment.

# Running

To run the collector in the foreground, just activate the virtual environment and then run the `uiharu-exporter` command:
```bash
$ source venv/bin/activate
$ uiharu-exporter
```

You an also run this under systemd by modifying the example sysytemd system service unit file and installing it (replacing `myuser` with the desired user):
```bash
$ sudo cp etc/systemd/system/uiharu-collector@.service /etc/systemd/system

# Edit the ExecStart and other properties as needed
$ sudo vim /etc/systemd/system/uiharu-collector@.service

$ sudo systemctl enable uiharu-collector@myuser.service
$ sudo systemctl start uiharu-collector@myuser.service

# Now, you should see logs
$ sudo journalctl -u uiharu-collector@myuser
```
