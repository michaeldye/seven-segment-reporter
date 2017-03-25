# Seven Segment Service Reporter

A program that interrogates `systemd` using Python DBUS bindings to determine the uptime of a particular service unit and writes it to an Adafruit seven segment LED display w/ i2c backpack (cf. https://www.adafruit.com/products/880). **Note** the `Makefile` will attempt to install the python dbus bindings upon setting up the development environment.

## Installation on a Pi ##

### Preconditions ###

#### Setup i2c interface ####

For raspbian, consult https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c.

In Ubuntu 16.04:

* Install packages with `apt install -y i2c-tools python-smbus`
* Load kernel modules at boot: `echo -e "\ni2c-bcm2708\ni2c-dev\n" > /etc/modules`
* Add `i2c` support to the kernel boot config: `echo -e "\ndtparam=i2c1=on\ndtparam=i2c_arm=on\n" >> /boot/firmware/config.txt`

### Installation Steps ###

* Build the project with `make package`
* Copy the output `whl` file from `python/dist/` to the target Pi
* Install dependencies with `apt install -y python3 python3-pip python3-dbus`
* Install the package with `pip3 install <path>/*.whl`
* Execute the program with a systemd unit name as an argument: `seven-segment-service-uptime ntp.service`

If you want to start the program at boot, write a systemd unit file like the following to `/etc/systemd/system/seven-segment-service-uptime-ntp.service`:

    [Unit]
    Description=Service uptime output
    Wants=ntp.service
    After=ntp.service

    [Service]
    ExecStart=/usr/local/bin/seven-segment-service-uptime ntp.service

    [Install]
    WantedBy=multi-user.target

Install this service with `systemctl daemon-reload && systemctl enable seven-segment-service-uptime-ntp.service`
