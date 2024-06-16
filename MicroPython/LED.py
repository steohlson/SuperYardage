'''from machine import Pin
from machine import Timer

pin = Pin("LED", Pin.OUT)
timer = Timer()


def loop():
    global pin
    pin.toggle()



if __name__ == "__main__":
    timer.init(mode=Timer.PERIODIC, freq=5, callback=loop)'''

from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

print("LED starts flashing...")
while True:
    try:
        pin.toggle()
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")



