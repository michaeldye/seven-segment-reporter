#!/usr/bin/env python3
# -*- coding: latin-1 -*-

""" """

__author__ = 'michael dye <m-github@divisive.info>'
__license__ = 'GPLv3'

import dbus
import time
import sys

from Adafruit_LED_Backpack import SevenSegment

def display_duration(usec):
  if usec == 0:
    return (0, None)

  duration = (time.time()-usec)

  if duration < 3600:
    return (int(duration//1), 'SECONDS')
  elif duration < 86400:
    return (int(duration//3600), 'HOURS')
  else:
    return (int(duration//86400), 'DAYS')

def uptime():
    args = sys.argv[1:]

    if len(args) != 1:
        raise Exception('systemd unit name as argument required')

    display = SevenSegment.SevenSegment()
    display.begin()

    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

    while True:
      display.clear()

      unit = manager.GetUnit(args[0])
      unit_object = sysbus.get_object('org.freedesktop.systemd1', unit)
      prop_unit = dbus.Interface(unit_object, 'org.freedesktop.DBus.Properties')
      active_timestamp = prop_unit.Get('org.freedesktop.systemd1.Unit', 'ActiveEnterTimestamp')

      # interrogate unit, get time
      clock_value, value_unit = display_duration(active_timestamp / 1e6)

      if not value_unit:
        sleep_time = 3

        for ix in range (4):
          display.set_digit(ix, '-')

      elif value_unit == 'SECONDS':
        sleep_time = .35

        display.print_float(clock_value, decimal_digits=0, justify_right=False)
      else:
        sleep_time = 3599

        display.print_number_str(str(clock_value), justify_right=False)

        if value_unit == 'HOURS':
          display.set_digit_raw(3, 0x74)
        elif value_unit == 'DAYS':
          display.set_digit_raw(3, 0x5E)
        else:
            print('Unknown clock value unit {}'.format(value_unit), file=sys.stderr)

      print('{}'.format(clock_value))
      display.write_display()
      time.sleep(sleep_time)

if __name__ ==  '__main__':
    uptime()

# vim: set ts=4 sw=4 expandtab:
