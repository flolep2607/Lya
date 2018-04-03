#!/usr/bin/env python
# coding: utf8
import argparse
import socket
from phue import Bridge
import sys

# create arguments
parser = argparse.ArgumentParser(description='HUE neuron binding to bridge')
parser.add_argument("--ip", help="IP address of you HUE bridge")

# parse arguments from script parameters
args = parser.parse_args()

if args.ip is None:
    print "You must set the IP of your HUE bridge"
    sys.exit(1)

bridge_ip = args.ip
# the user set an IP, ask him to press the link buton, block the main process until a key is pressed
value = raw_input("Please press the link button on your bridge and then press enter on your keyboard")

# key has been pressed
try:
    # connect to allow the lib to discuss with the API
    b = Bridge(bridge_ip)
except socket.error:
    print "Please check the IP address"
    sys.exit(1)

print "Bridge linked, you can now use the neuron"
