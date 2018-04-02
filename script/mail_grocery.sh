#!/bin/bash

/home/pi/kalliope_config/script/sendmail.py -s="[kalliope] Liste de courses" -b="`grep +course ~/todo.txt`"
