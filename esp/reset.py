#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) # sets GPIO identification by physical pin numbers
resetPin = 3 # identify RPi physical pin connected to ESP8266 RST pin

GPIO.setup(resetPin, GPIO.OUT) # set reset pin as output

GPIO.output(resetPin, GPIO.LOW) # drop voltage on RST pin
time.sleep(.2) # wait for .2 s
GPIO.output(resetPin, GPIO.HIGH) # restore voltage on RST pin

GPIO.cleanup() # reset pins on RPI to prevent future runtime warnings
