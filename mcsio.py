#!/usr/bin/python3
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import sys
import http.client as http
import urllib
import json
deviceId = "DK8Td3BQ"
deviceKey = "0PKeMevWZ02Z1PpN"
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def post_to_mcs(payload):
	headers = {"Content-type": "application/json", "deviceKey": deviceKey}
	not_connected = 1
	while (not_connected):
		try:
			conn = http.HTTPConnection("api.mediatek.com:80")
			conn.connect()
			not_connected = 0
		except (http.HTTPException, socket.error) as ex:
			print ("Error: %s" % ex)
			time.sleep(10)
			 # sleep 10 seconds
	conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload),headers)
	response = conn.getresponse()


	print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
	data = response.read()
	conn.close()

while True:
	h0, t0= Adafruit_DHT.read_retry(sensor, pin)
	if h0 is not None and t0 is not None:
		print('Temp={0:0.1f}*Humidity={1:0.1f}%'.format(t0, h0))
		SwitchStatus=GPIO.input(24)
		if(SwitchStatus==0):
			print('Button pressed')
		else:
			print('Button released')
		payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}}
		,{"dataChnId":"Temperature","values":{"value":t0}}
		,{"dataChnId":"SwitchStatus","values":{"value":SwitchStatus}}]}
		post_to_mcs(payload)
		time.sleep(1) 

	else:
		print('Failed to get reading. Try again!')
		sys.exit(10)

