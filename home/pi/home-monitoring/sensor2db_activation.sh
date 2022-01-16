#!/bin/bash
export DISPLAY=:0.0
source /home/pi/.profile
workon sensor_dev
cd /home/pi/home-monitoring
python sensor_read.py