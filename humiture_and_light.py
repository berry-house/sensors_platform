import RPi.GPIO as GPIO
import PCF8591 as ADC
import time
import os
import requests
import calendar
import tweepy
import json
url = "http://35.230.39.10:80/broker/temperature"

DHTPIN = 17
DO = 17
GPIO.setmode(GPIO.BCM)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5


def setup():
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)


def read_dht11_dat():
	GPIO.setup(DHTPIN, GPIO.OUT)
	GPIO.output(DHTPIN, GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(DHTPIN, GPIO.LOW)
	time.sleep(0.02)
	GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

	unchanged_count = 0
	last = -1
	data = []
	while True:
		current = GPIO.input(DHTPIN)
		data.append(current)
		if last != current:
			unchanged_count = 0
			last = current
		else:
			unchanged_count += 1
			if unchanged_count > MAX_UNCHANGE_COUNT:
				break

	state = STATE_INIT_PULL_DOWN

	lengths = []
	current_length = 0

	for current in data:
		current_length += 1

		if state == STATE_INIT_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_INIT_PULL_UP
			else:
				continue
		if state == STATE_INIT_PULL_UP:
			if current == GPIO.HIGH:
				state = STATE_DATA_FIRST_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_FIRST_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_DATA_PULL_UP
			else:
				continue
		if state == STATE_DATA_PULL_UP:
			if current == GPIO.HIGH:
				current_length = 0
				state = STATE_DATA_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_PULL_DOWN:
			if current == GPIO.LOW:
				lengths.append(current_length)
				state = STATE_DATA_PULL_UP
			else:
				continue
	if len(lengths) != 40:
		print "Data not good, skip"
		return False

	shortest_pull_up = min(lengths)
	longest_pull_up = max(lengths)
	halfway = (longest_pull_up + shortest_pull_up) / 2
	bits = []
	the_bytes = []
	byte = 0

	for length in lengths:
		bit = 0
		if length > halfway:
			bit = 1
		bits.append(bit)
	#print "bits: %s, length: %d" % (bits, len(bits))
	for i in range(0, len(bits)):
		byte = byte << 1
		if (bits[i]):
			byte = byte | 1
		else:
			byte = byte | 0
		if ((i + 1) % 8 == 0):
			the_bytes.append(byte)
			byte = 0
	#print the_bytes
	checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
	if the_bytes[4] != checksum:
		print "Data not good, skip"
		return False

	return the_bytes[0], the_bytes[2]


def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)



def main():
	print "Berry House sensors platform!\n"

	with open('twitter_secret.json') as json_secret_file:
		data = json.load(json_secret_file)
	cfg = {
		"consumer_key"        : data['consumer_key'],
		"consumer_secret"     : data['consumer_secret'],
		"access_token"        : data['access_token'],
		"access_token_secret" : data['access_token_secret']
	}
	api = get_api(cfg)

	status = 1
	readings = open("readings.txt","w")
	initialTime = calendar.timegm(time.gmtime())
	period = 60 # 1 minute
	totalTemperature = 0.0
	totalHumidity = 0.0
	totalLight = 0.0
	count = 0
        while True:
                #print 'Light: ', ADC.read(0)
                #time.sleep(0.2)
		result = read_dht11_dat()
		if result:
			humidity, temperature = result
			print "Light:%s  Humidity: %s %%,  Temperature: %s C`" % (ADC.read(0), humidity, temperature)
			readings.write("Light:%s  Humidity: %s %%,  Temperature: %s C`\n" % (ADC.read(0), humidity, temperature))
			totalTemperature += int(temperature)
			totalHumidity += int(humidity)
			totalLight += int(ADC.read(0))
			count += 1
			if(int(calendar.timegm(time.gmtime())) >= int(initialTime)+period):
				tweet = "For the past {:.0f} minute, I've been at around {:.2f}C, with light intensity of {:.2f} and humidity of {:.2f}%%. Quite nice.".format(period/60, totalTemperature/count, totalLight/count, totalHumidity/count)
				status = api.update_status(status=tweet)
				print(tweet)
                readings.write(tweet + '\n')
				initialTime = calendar.timegm(time.gmtime())
				totalTemperature = 0.0
				totalHumidity = 0
				totalLight = 0
				count = 0
			data = {
				"id": 1,
				"timestamp": calendar.timegm(time.gmtime()),
				"temperature": temperature,
			}
			resp = requests.post(url, json=data)
#			print(" URL:\t\t%s" % resp.url)
#			print(" encoding:\t%s" % resp.encoding)
#			print(" status_code:\t%s" % resp.status_code)
#			print(" text:\t\t%s" % resp.text)
		time.sleep(2)


def destroy():
	GPIO.cleanup()


if __name__ == '__main__':
	try:
		setup()
		main()
		loop()
	except KeyboardInterrupt:
		pass
		destroy()
