#!/bin/bash
orders=$(grep "order:" ../brains/*.yml | awk -F ': ' '{print $3;}' | sed -e s/\"//g | sort)
/home/pi/kalliope_config/script/sendmail.py -s="[kalliope] Ordres disponibles" -b="$orders"
