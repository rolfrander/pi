#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) # sets GPIO identification by physical pin numbers
resetPin = 3 # identify RPi physical pin connected to ESP8266 RST pin
flashPin = 5 # identify RPi physical pin connected to ESP8266 GPIO0 pin

GPIO.setup(resetPin, GPIO.OUT) # set reset pin as output
GPIO.setup(flashPin, GPIO.OUT) # set flash pin as output

GPIO.output(resetPin, GPIO.LOW) # drop voltage on RST pin
time.sleep(.2) # need for this waiting is speculative
GPIO.output(flashPin, GPIO.LOW) # drop voltage on GPIO0
time.sleep(.2) # need for this waiting is speculative
GPIO.output(resetPin, GPIO.HIGH) # start booting ESP8266
time.sleep(.5) # wait for ESP8266 to boot
GPIO.ouput(flashPin.GPIO.HIGH) # restore voltage on

GPIO pinGPIO.cleanup() # reset pins on RPI to prevent future runtime warnings
