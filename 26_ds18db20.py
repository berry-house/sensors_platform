#!/usr/bin/env python
#----------------------------------------------------------------
#	Note:
#		ds18b20's data pin must be connected to pin7.
#		replace the 28-XXXXXXXXX as yours.
#----------------------------------------------------------------
import os
import requests
url = "http://localhost:8000/broker/temperature"

ds18b20 = ''

def setup():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1_bus_master1':
			ds18b20 = i

def read():
#	global ds18b20
	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	tfile = open(location)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature
	
def loop():
	while True:
		if read() != None:
			print "Current temperature : %0.3f C" % read()
			data = {
			    "id": 1,
			    "timestamp": 1516740522,
			    "temperature": read(),
			}
			resp = requests.post(url, json=data)
			print(" URL:\t\t%s" % resp.url)
			print(" encoding:\t%s" % resp.encoding)
			print(" status_code:\t%s" % resp.status_code)
			print(" text:\t\t%s" % resp.text)

def destroy():
	pass

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
