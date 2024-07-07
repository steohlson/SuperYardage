import machine
from machine import Pin
import time
import InputManager

#Use firmware from this repository to use the following libraries
#https://github.com/russhughes/st7789_mpy
import st7789 # type: ignore
import vga1_8x16 # type: ignore
import vga1_16x32 # type: ignore


class Font:
    font = vga1_8x16
    width : int
    height : int
    
    def __init__(self, font, width, height):
        self.font = font
        self.height = height
        self.width = width


font1 = Font(vga1_8x16, 8, 16)
font2 = Font(vga1_16x32, 16, 32)




#other pins
res=12
dc=13

width=320
height=170




class Item:
    font : Font
    startX : float ; startY : float
    fg = st7789.WHITE
    bg = st7789.BLACK

    def __init__(self, font, x, y, fg, bg):
        self.font = font
        self.startX = x
        self.startY = y
        self.fg = fg
        self.bg = bg

    def Start(self):
        pass
    
    def Print(self, Display, text, fg=fg, bg=bg):
        Display.text(self.font.font, text, self.startX, self.startY, fg, bg)

        




class Page:

    Display : st7789.ST7789
    bg = st7789.BLACK


    def __init__(self, Display, bg):
        self.Display = Display
        self.bg = bg


    def Start(self):
        '''Run when you actually want to display this page'''
        pass

    def Update(self):
        '''Update page'''
        pass


class Menu(Page):

    items = {}
    

    def __init__(self, Display, bg):
        Page.__init__(self, Display, bg)
        
        

    def AddItem(self, itemName : str, font : Font = font1, fg=st7789.WHITE, bg=st7789.BLACK):
        x=0
        y=0
        for item in self.items.values():
            y += item.font.height

        self.items[itemName] = (Item(font, x, y, fg, bg))


    def Start(self):
        '''Run when you actually want to display this page'''
        self.Display.fill(self.bg)
        

    def Update(self):
        '''Update page'''
        pass


class Console(Menu):
    inputManager : InputManager.input_manager

    def __init__(self, Display, bg, inputManager : InputManager.input_manager):
        Menu.__init__(self, Display, bg)
        self.inputManager = inputManager


    def Start(self):
        '''Run when you actually want to display this page'''
        Menu.Start(self)
        self.AddItem("JoystickX")
        self.AddItem("JoystickY")
        
        

    def Update(self):
        '''Update page'''

        self.items["JoystickX"].Print(self.Display, "Stick X: {:.2f}".format(self.inputManager.stick1.GetAxisX()))
        self.items["JoystickY"].Print(self.Display, "Stick Y: {:.2f}".format(self.inputManager.stick1.GetAxisY()))

    
        


class display_manager:

    Display : st7789.ST7789

    csPin : Pin
    inputManager : InputManager.input_manager

    console : Page

    def __init__(self, SPI : machine.SPI, CSPIN : Pin, inputManager : InputManager.input_manager) -> None:
        self.csPin = CSPIN
        self.inputManager = inputManager

        

        self.csPin.value(0)
        
        self.Display = st7789.ST7789(spi=SPI, width=height, height=width, reset=Pin(res, Pin.OUT), dc=Pin(dc, Pin.OUT), rotation=45)
        self.Display.init()
        
        self.Display.jpg("ControllerLoadingScreen.jpg", 0, 0, st7789.SLOW)
        
        
        self.console = Console(self.Display, st7789.BLACK, inputManager)

        time.sleep(1)

        self.console.Start()

        self.csPin.value(1)



    

    def Update(self, cpuTemp):
        self.csPin.value(0)

        self.console.Update()

        self.csPin.value(0)
        
