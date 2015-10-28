import pi
import time

class MyButton(pi.DigitalInput):
    def __init__(self, pin, output):
        super(MyButton, self).__init__(pin)
        self.i=0
        self.output=output

    def down(self):
        self.i=self.i+1
        self.output.toggle()
        print self.i

    def up(self):
        pass

led = pi.DigitalOutput(18)
button = MyButton(22, led)

try:
    while True:
        time.sleep(0.01)

except KeyboardInterrupt:
    pi.cleanup()
