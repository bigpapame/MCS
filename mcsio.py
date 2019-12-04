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
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
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

