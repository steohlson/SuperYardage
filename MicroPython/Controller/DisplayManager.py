from machine import Pin
import time

#Use firmware from this repository to use driver
#https://github.com/russhughes/st7789_mpy
import st7789


import vga1_16x32 as font1




width=170
height=320
res=12
dc=13

class DisplayManager:
    
   

    def _init_(self, SPI, CS):
        global csPin
        global spi
        global display


        csPin = Pin(CS, Pin.OUT)
        self.spi = SPI

        csPin.value(0)
        
        display = st7789.ST7789(spi=spi, width=width, height=height, reset=Pin(res, Pin.OUT), dc=Pin(dc, Pin.OUT), rotation=45)
        display.init()
        
        display.jpg("ControllerLoadingScreen.jpg", 0, 0, st7789.SLOW)

        time.sleep(2)

        csPin.value(1)



    def updateDisplay(self):
        
        csPin.value(0)
        display.fill(st7789.BLACK)
        display.text(font1,"CPU temp: ", 0, 0)
        

        display.text(font1, str(6.3) + " C", 144, 0)
        csPin.value(1)
        time.sleep(.1)



#display.fill(st7789.RED)
