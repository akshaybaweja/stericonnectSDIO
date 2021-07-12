#!/bin/bash
mountStatus=$( DEV="sda"; USB=$(udevadm info -q all /dev/$DEV | grep DEVPATH | grep -o '/usb[1-9]*/[1-9,-]*' | cut -d'/' -f3); echo $USB > /sys/bus/usb/drivers/usb/unbind; echo $USB > /sys/bus/usb/drivers/usb/bind)
exit $?