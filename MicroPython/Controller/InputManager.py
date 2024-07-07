import machine
from machine import Pin
from machine import ADC
import time


def clamp(x, min, max) -> float:
    '''Limit input value to only values between max and min inclusive'''
    if(x > max):
        x = max
    elif(x < min):
        x = min
    return x

def max(a, b):
    if(a > b): 
        return a
    return b

def min(a, b):
    if(a > b): 
        return b
    return a


class Button:
    pin : Pin

    def __init__(self, pinNumber):
        self.pin = Pin(pinNumber, Pin.IN)

    prevValue = False
    def Update(self):
        self.prevValue = self.Get()

    def GetPressed(self) -> bool:
        if(self.prevValue == False and self.Get() == True):
            return True
        else:
            return False

    def GetReleased(self) -> bool:
        if(self.prevValue == True and self.Get() == False):
            return True
        else:
            return False
    
    def Get(self) -> bool:
        if(self.pin.value() == 1):
            return True
        else:
            return False




class Joystick:
    xPin : ADC
    yPin : ADC
    pushButton : Button

    #Variables for setting zero position
    xOffset = 0
    yOffset = 0

    #Variables for scaling input
    maxX = 0; minX = 0
    maxY = 0; minY = 0

    deadband : float = 0.01

    #minimum value before it considers the joystick held for UI interactions
    minOnLevel = 0.6



    def __init__(self, x, y, push) -> None:
        self.xPin = ADC(Pin(x, Pin.IN))
        self.yPin = ADC(Pin(y, Pin.IN))
        self.pushButton = Button(push)

        self.SetDeadband(0.1)

        self.Zero()
        print("Zeroed")
        print("Now Tuning Scaling")

        for i in range(1000):
            self.TuneScaling()
            time.sleep(.01)
        print("Done")
    

    prevUp = False; prevDown = False; prevRight = False; prevLeft = False



    def Update(self):
        '''Updates all feedback variables.  Allows for detecting when something is first pressed'''
        self.prevUp = self.GetUp()
        self.prevDown = self.GetDown()
        self.prevRight = self.GetRight()
        self.prevLeft = self.GetLeft()
        self.pushButton.Update()


    
    def GetUpPressed(self) -> bool:
        '''Returns boolean representing if this direction has just been pressed. Essentially the rising edge'''
        if(self.prevUp == False and self.GetUp() == True):
            return True
        else:
            return False
    
    def GetDownPressed(self) -> bool:
        '''Returns boolean representing if this direction has just been pressed. Essentially the rising edge'''
        if(self.prevDown == False and self.GetUp() == True):
            return True
        else:
            return False

    def GetRightPressed(self) -> bool:
        '''Returns boolean representing if this direction has just been pressed. Essentially the rising edge'''
        if(self.prevRight == False and self.GetUp() == True):
            return True
        else:
            return False
    
    def GetLeftPressed(self) -> bool:
        '''Returns boolean representing if this direction has just been pressed. Essentially the rising edge'''
        if(self.prevLeft == False and self.GetUp() == True):
            return True
        else:
            return False
    


    #Returns boolean representing if each direction is pressed or not
    def GetUp(self) -> bool:
        '''Returns boolean representing if this direction is pressed'''
        if(self.GetAxisY() > self.minOnLevel):
            return True
        else:
            return False
        
    
    def GetDown(self) -> bool:
        '''Returns boolean representing if this direction is pressed'''
        if(self.GetAxisY() < -self.minOnLevel):
            return True
        else:
            return False
        
    def GetRight(self) -> bool:
        '''Returns boolean representing if this direction is pressed'''
        if(self.GetAxisX() > self.minOnLevel):
            return True
        else:
            return False
        
    
    def GetLeft(self) -> bool:
        '''Returns boolean representing if this direction is pressed'''
        if(self.GetAxisX() < -self.minOnLevel):
            return True
        else:
            return False
        




    def GetAxisX(self) -> float:
        '''Returns value from -1 to 1 for joystick x-axis'''
        rawX = self.xPin.read_u16()
        x = rawX + self.xOffset

        if(x > 0):
            x /= self.maxX
        else:
            x /= self.minX


        x = clamp(x, -1, 1)

        if(x > 0):
            if(x < self.deadband):
                x = 0
            else:
                x = (x - self.deadband) / (1 - self.deadband)
        else:
            if(x > self.deadband):
                x = 0
            else:
                x = (x + self.deadband) / (-1 + self.deadband)

        
        return x
    



    def GetAxisY(self) -> float:
        '''Returns value from -1 to 1 for joystick y-axis'''
        rawY = self.yPin.read_u16()
        y = rawY + self.yOffset

        if(y > 0):
            y /= self.maxY
        else:
            y /= self.minY
        
        #Apply Deadband
        #Essentially take absolute value, apply deadband, then undo absolute value

        isNegative = (y < 0)

        if(isNegative):
            y *= -1


        if(y < self.deadband):
            y = 0
        elif( y > 1 - self.deadband):
            y = 1
        else:
            y = (y - self.deadband) / (1 - 2 * self.deadband)


        if(isNegative):
            y *= -1


        y = clamp(y, -1, 1)

        
        return y



    ########TUNING###########
    
    def SetDeadband(self, x):
        self.deadband = x


    def Zero(self):
        '''Zeros the joystick'''
        rawX = self.xPin.read_u16()
        rawY = self.yPin.read_u16()

        self.xOffset = -(rawX)
        self.yOffset = -(rawY)


    

    def TuneScaling(self):
        rawX = self.xPin.read_u16()
        rawY = self.yPin.read_u16()

        x = rawX + self.xOffset
        y = rawY + self.yOffset

        if(x > 0):
            self.maxX = max(x, self.maxX)
        else:
            self.minX = min(x, self.minX)

        if(y > 0):
            self.maxY = max(y, self.maxY)
        else:
            self.minY = min(y, self.minY)



    


stickX=27
stickY=26
stickPush=22

class input_manager:
    stick1 : Joystick

    def __init__(self) -> None:
        self.stick1 = Joystick(stickX, stickY, stickPush)
    
    def Update(self):
        self.stick1.Update()