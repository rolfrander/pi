import RPi.GPIO as GPIO
import time
import sys

# MCP3008
clkPin=17
outPin=27
inPin=22
csPin=5


ledPin = 19
butPin = 22
f=2
dc = 0

v=1
cnt=0

## General setup

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

def setupLed():
    GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
    #GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
    pwm = GPIO.PWM(ledPin, f)  # Initialize PWM on pwmPin 100Hz frequency
    GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

    # Initial state for LEDs:
    GPIO.output(ledPin, GPIO.HIGH)
    pwm.start(50)

def setupADC(clkPin, outPin, inPin, csPin):
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(outPin, GPIO.IN)
    GPIO.setup(inPin, GPIO.OUT)
    GPIO.setup(csPin, GPIO.OUT)

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)
 
    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low
 
    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
 
    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1
 
    GPIO.output(cspin, True)
        
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout

oldv=1
ledstate=0

def lightswitch():
    while 1:
        oldv = v
        v = GPIO.input(butPin)
        if v == 1 and v != oldv:
            print "release!", cnt
            cnt = cnt+1
        elif v == 0 and v != oldv:
            f=f*2
            print "press!", cnt, dc
            if f > 32:
                f = 1
            # pwm.ChangeDutyCycle(dc)
            pwm.ChangeFrequency(f)

#            ledstate = 1-ledstate
#            if ledstate == 0:
#                GPIO.output(ledPin, GPIO.LOW)
#            else:
#                GPIO.output(ledPin, GPIO.HIGH)

setupADC(clkPin, outPin, inPin, csPin);

linewith = int(sys.argv[1])

def adc(analogInputPin):
    prev=0
    while 1:
        i=readadc(analogInputPin, clkPin, inPin, outPin, csPin)*linewith/1023
        if i != prev:
            print "*"*i
            prev = i
        
def my_callback(channel):
    global cnt
    print "callback:",cnt
    cnt = cnt+1


try:
    GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
    GPIO.add_event_detect(butPin, GPIO.BOTH, callback=my_callback)
    while True:
        time.sleep(0.01)

except KeyboardInterrupt: # CTRL+C is pressed, exit cleanly
    GPIO.cleanup() # cleanup all GPIO
