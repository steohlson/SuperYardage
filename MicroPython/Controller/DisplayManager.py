import machine
from machine import Pin
import time
import InputManager

#Use firmware from this repository to use the following libraries
#https://github.com/russhughes/st7789_mpy
import st7789 # type: ignore
import vga1_16x32 as font1 # type: ignore


#other pins
res=12
dc=13




class display_manager:

    width=170
    height=320

    Display : st7789.ST7789
    csPin : Pin
    inputManager : InputManager.input_manager

    def __init__(self, SPI : machine.SPI, CSPIN : Pin, inputManager : InputManager.input_manager) -> None:
        self.csPin = CSPIN
        self.inputManager = inputManager

        self.csPin.value(0)
        
        self.Display = st7789.ST7789(spi=SPI, width=self.width, height=self.height, reset=Pin(res, Pin.OUT), dc=Pin(dc, Pin.OUT), rotation=45)
        self.Display.init()
        
        self.Display.jpg("ControllerLoadingScreen.jpg", 0, 0, st7789.SLOW)

        time.sleep(2)
        self.Display.fill(st7789.BLACK)

        self.csPin.value(1)

    

    def Update(self, cpuTemp):
        temp = str(cpuTemp) + " C"
        self.csPin.value(0)
        #self.Display.fill(st7789.BLACK)
        self.Display.text(font1,"CPU temp: ", 0, 0)
        
        self.Display.text(font1, temp, 144, 0)
        self.csPin.value(1)
        



#display.fill(st7789.RED)
