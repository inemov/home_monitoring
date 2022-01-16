# Home environmental monitoring
Sensor metrics collection with BME280, storage in PostgreSQL and Grafana dashboard on Raspberry Pi.
 
## Hardware
- Raspberry Pi 4 Model B 4GB RAM https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
- BME280 https://shop.pimoroni.com/products/bme280-breakout
- Waveshare 7" HDMI LCD (C) Capacitive Touchscreen 1024 x 600 https://www.waveshare.com/7inch-hdmi-lcd-c.htm
- HDMI to HDMI micro cable
- USB A to USB micro B cable

- BME280 connection to Raspberry Pi via I2C: 2-6V - 3V3; SDA - GPIO 3 (SDA); SCL - GPIO 5 (SCL); GND - GPIO 9 (Ground).
![image](https://user-images.githubusercontent.com/24581566/149649740-9fe03407-5da1-4edf-a594-d3ab34becb6b.png)

## Software

- Setup of right-click functionality for Waveshare 7" touch screen https://www.inemov.com/post/set-rightclick-rpi-waveshare7-touchscreen
- Install PostgreSQL and create pi user and pi database:
'''
sudo apt install postgresql
sudo su postgres
createuser pi -P --interactive
'''
provide password and allow the role to be a superuser
'''
psql
CREATE DATABASE pi;
exit
'''
- 
