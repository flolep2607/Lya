#!/usr/bin/python
# coding: utf-8

# Script to check if Kalliope is still available (via API).
# If not, it will trigger a GPIO pin to switch on a led

import argparse
import requests
import RPi.GPIO as GPIO

def main():

    # Default Kalliope Api value:
    configuration = {
        "url": "http://localhost",
        "user": "admin",
        "password": "secret",
        "port": 5000,
        "endpoint": "/",
        "GPIO": 18,
        "statusfile": "/tmp/_kalliope_status"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Kalliope API URL")
    parser.add_argument("-l", "--user", help="Kalliope API username")
    parser.add_argument("-p", "--password", help="Kalliope API password")
    parser.add_argument("-P", "--port", help="Kalliope API port", type=int)
    parser.add_argument("-g", "--gpio", help="Led GPIO", type=int)
    parser.add_argument("-s", "--statusfile", help="Led GPIO", type=int)
    parser.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")

    args = parser.parse_args()

    if args.url:
        configuration["url"] = args.url
    if args.user:
        configuration["user"] = args.user
    if args.password:
        configuration["password"] = args.password
    if args.port:
        configuration["port"] = args.port
    if args.gpio:
        configuration["gpio"] = args.gpio
    if args.statusfile:
        configuration["statusfile"] = args.statusfile

    endpoint_url = configuration['url'] + ":" + str(configuration['port']) + configuration['endpoint']

    is_up = 0
    if configuration['password'] and configuration['user']:
        try:
            r = requests.get(endpoint_url, auth=(configuration['user'], configuration['password']))
            print("is_up = 1")
            is_up = 1
        except Exception, e:
            pass

    old_status = _get_previous_status(configuration['statusfile'])

    print("old_status: %s" % old_status)
    print("new_status: %s" % is_up)

    # Get previous status from file
    if old_status != is_up and is_up == 0:
        # Start led red
        print("starting led")
        red_led(configuration['GPIO'], 1)
    elif old_status != is_up and is_up == 1:
        # Stop red led
        print("stopping led")
        red_led(configuration['GPIO'], 0)

    _save_current_status(configuration['statusfile'], is_up)

def red_led(pin, mode = 0):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)

    if mode == 1:
        GPIO.output(pin,GPIO.HIGH)
    elif mode == 0:
        GPIO.output(pin,GPIO.LOW)

def _get_previous_status(statusfile):
    try:
        with open(statusfile, 'r') as f:
            old_status = f.read()
            print(old_status)
    except:
        old_status = -1

    return old_status

def _save_current_status(statusfile, is_up):
    print('is_up: %s' % is_up)
    try:
        with open(statusfile, 'w+') as f:
            f.write(is_up)
    except:
        pass

if __name__ == "__main__":
    main()
