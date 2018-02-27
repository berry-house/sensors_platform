# sensors_platform
Raspberry Pi sensors and data processing.
## Raspberry Pi setup
First, you should change the configuration of your Raspberry Pi to support these sensors. And for that, you should open the terminal and run:
```
echo “dtoverlay=w1-gpio” >> /boot/config.txt
sudo raspi-config
```
After that, you will see a screen similar to this. We’ll proceed to enable the I2C interface on your Raspberry Pi:
![raspi_config](img/raspi_config.png)<br/>
Select “Interfacing Options” and then “I2C”. The screen will ask if you want the ARM I2C interface to be enabled. Select “Yes”, “Ok” and “Finish” to return to the command line.<br/>
<br/>
Now we need to install some utilities. For that, run
```
sudo apt-get update
sudo apt-get install -y python-smbus i2c-tools
```
Reboot your Raspberry Pi to load the I2C module. Now we should be able to check if the i2c module is running, with the command:
```
lsmod | grep i2c_
```
## Circuit
...
