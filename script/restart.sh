#!/bin/sh 

# Hard reset script
#Kill Kalliope, mopidy, pulseaudio and previous tmux session
#And restart everything

mopidy_pid=`ps faux | grep mopidy | grep -v grep | awk '{print $2}'`
kalliope_pid=`ps faux | grep kalliope | grep -v grep | grep -v tee | awk '{print $2}'`
pulseaudio_pid=`ps faux | grep pulseaudio | grep -v grep | awk '{print $2}'`

kill "$mopidy_pid"
kill "$kalliope_pid"
kill "$pulseaudio_pid"

tmux kill-session -t "kalliope"

tmux new-session -d -s "kalliope" 'pulseaudio --start && cd /home/pi/kalliope_config/ && /usr/bin/python -u /usr/local/bin/kalliope start | tee kalliope.log'
tmux new-window 'mopidy'
