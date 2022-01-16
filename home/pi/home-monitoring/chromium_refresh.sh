#!/bin/bash
export DISPLAY=:0.0
export XAUTHORITY=/home/pi/.Xauthority
while true;
do
  xdotool key ctrl+R &
  sleep 1200 #refresh time in seconds
done