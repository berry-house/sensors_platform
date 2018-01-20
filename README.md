# sensors_platform
Raspberry Pi sensors and data processing.
## Raspberry Pi setup
Circuit:<br/>
![circuit](https://www.sunfounder.com/media/wysiwyg/swatches/sensor_kit_v2_0_for_b_plus/lesson-26-ds18b20-temperature-sensor/ds18b202.png)<br/>
Add the following to the bottom of */boot/config.txt*
```
dtoverlay=w1-gpio
```
Then reboot. After rebooting, type these commands to mount the device drivers and confirm whether the device is effective or not:
```
sudo modprobe w1-gpio
sudo modprobe w1-therm
```
Then, change directory to location */sys/bus/w1/devices/*<br/>
Once there, you should see a directory with name similar to *28-031554cff6ff* (the serial number of your particular ds18db20). Now, to check the current temperature with Python, we'll use the Python code in this repository and run
```
sudo puthon 26_ds18db20.py
```
The current temperature will be displayed on the screen.
