import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

def cleanup():
    GPIO.cleanup()

class Pin(object):
    """General concept of a GPIO-pin on the RPi, used for input or output"""
    def __init__(self, pin):
        self.pin = pin

class DigitalOutput(Pin):
    """GPIO-pin used for digital output (GPIO.LOW=0 or GPIO.HIGH=1)"""
    def __init__(self, pin):
        """Connects to a given pin, sets it up for output and sets a default state of LOW"""
        super(DigitalOutput, self).__init__(pin)
        GPIO.setup(pin, GPIO.OUT)
        self.off()

    def on(self):
        """Sets the pin-state to HIGH"""
        self.value = GPIO.HIGH
        GPIO.output(self.pin, self.value)

    def off(self):
        """Sets the pin-state to LOW"""
        self.value = GPIO.LOW
        GPIO.output(self.pin, self.value)

    def toggle(self):
        if self.value == GPIO.LOW:
            self.on()
        else:
            self.off()

    def get_state(self):
        return self.value;

class DigitalInput(Pin):
    """Reading digital input from a GPIO-pin, possibly with a callback"""
    def __init__(self, pin):
        super(DigitalInput, self).__init__(pin)
        # input with pull-up-resistor, meaning default value is 1
        # see wikipedia for detailes
        # https://en.wikipedia.org/wiki/Pull-up_resistor
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # switch bounce
        # http://www.allaboutcircuits.com/textbook/digital/chpt-4/contact-bounce/
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback = self.callback, bouncetime=50)

    def callback(self, _pin):
        value = self.get_state()
        if value == 0:
            self.down()
        else:
            self.up()

    def get_state(self):
        """returns the current state of the pin. 0 means connected."""
        return GPIO.input(self.pin)

    def down(self):
        """called on falling edge"""
        pass

    def up(self):
        """called on rising edge"""
        pass

    def wait_for(self, event):
        """blocks until event happens. Event is one of GPIO.RISING, GPIO.FALLING or GPIO.BOTH"""
        GPIO.wait_for_edge(self.pin, event)
