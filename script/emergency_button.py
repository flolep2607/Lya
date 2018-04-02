#!/usr/bin/python

# This script will listen to a push button on the GPIO 23
# When clicked, it fires an ssh commands on the kalliope server and fire a restart script.

import RPi.GPIO as GPIO
import commands
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(23)
    if input_state == False:
        print('Button Pressed - killing kallipe')
        status, output = commands.getstatusoutput("ssh -t pi@kalliope 'sh /home/pi/kalliope_config/script/restart.sh'")

        # Leave time to avoid multiple trigger
        time.sleep(10)

