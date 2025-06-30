from gpiozero import PWMOutputDevice as PWM
import asyncio

class RGBLED:
    def __init__(self):
        # Pin assignments
        L_pins = dict(R=3, G=2,  B=0)
        R_pins = dict(R=1,  G=5,  B=6)

        # build devices
        self.devices = {}
        for side, pins in (("L", L_pins), ("R", R_pins)):
            for col, pin in pins.items():
                self.devices[f"{side}_{col}"] = PWM(pin=pin, initial_value=1.0, frequency=2000)

        # handy colors
        self.colors = {
            "red":        0xFF0000,
            "light_blue": 0x00FFFF,
            "blue": 0x0000FF,
            "green": 0x00FF00
        }

        # event to control the loop
        self._stop_event = asyncio.Event()

    def map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min

    def set_color(self, side, color):
        if side not in ("L","R"):
            raise ValueError("side must be 'L' or 'R'")
        # extract and normalize
        r = (color >> 16) & 0xFF
        g = (color >>  8) & 0xFF
        b = (color >>  0) & 0xFF
        r, g, b = (self.map_value(v, 0, 255, 0, 1) for v in (r,g,b))
        # gpiozero is inverted
        self.devices[f"{side}_R"].value = 1 - r
        self.devices[f"{side}_G"].value = 1 - g
        self.devices[f"{side}_B"].value = 1 - b

    async def talking(self):
        """Flash back-and-forth until stopped."""
        self._stop_event.clear()
        try:
            while not self._stop_event.is_set():
                self.set_color("R", self.colors["red"])
                self.set_color("L", self.colors["red"])
                await asyncio.sleep(.05)
                self.set_color("R", self.colors["blue"])
                self.set_color("L", self.colors["blue"])
                await asyncio.sleep(.05)
                self.set_color("R", self.colors["green"])
                self.set_color("L", self.colors["green"])
                await asyncio.sleep(.05)
        finally:
            # make sure LEDs end off (or white) when loop exits
            for d in self.devices.values():
                d.value = 1.0

    def stop(self):
        """Signal talking() to exit at the next opportunity."""
        self._stop_event.set()

f="""
#import RPi.GPIO as GPIO
from gpiozero import PWMOutputDevice as PWM
import time
import asyncio

class RGBLED(object):
    def __init__(self):
        pass
        Left_R = 19
        Left_G = 0
        Left_B = 13

        Right_R = 1
        Right_G = 5
        Right_B = 6
        L_R = PWM(pin=Left_R, initial_value=1.0, frequency=2000)
        L_G = PWM(pin=Left_G, initial_value=1.0, frequency=2000)
        L_B = PWM(pin=Left_B, initial_value=1.0, frequency=2000)

        R_R = PWM(pin=Right_R, initial_value=1.0, frequency=2000)
        R_G = PWM(pin=Right_G, initial_value=1.0, frequency=2000)
        R_B = PWM(pin=Right_B, initial_value=1.0, frequency=2000)
    
        self.devices = {"L_R":L_R, "L_G":L_G, "L_B":L_B, "R_R":R_R, "R_G":R_G, "R_B":R_B}
        self.colors = {"red":0xFF0000, "green":0x00FF00, "blue":0x0000FF, "yellow":0xFFFF00, "purple":0xFF00FF, "light_blue":0x00FFFF, "light_purple":0X6F00D2, "orange":0xFF5809}

        self.flag = asyncio.Event()

    def map_value(self, x, in_min, in_max, out_min, out_max):
         return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def set_color(self, side , color ):
        if not side in ("L","R"):
            raise( "side has to be L or R")
        R_val = (color & 0xff0000) >> 16
        G_val = (color & 0x00ff00) >> 8
        B_val = (color & 0x0000ff) >> 0

        R_val = self.map_value(R_val, 0, 255, 0, 1.00)
        G_val = self.map_value(G_val, 0, 255, 0, 1.00)
        B_val = self.map_value(B_val, 0, 255, 0, 1.00)


        self.devices[f"{side}_R"].value = 1.0-R_val
        self.devices[f"{side}_G"].value = 1.0-G_val
        self.devices[f"{side}_B"].value = 1.0-B_val

    async def talking(self):
        self.flag.clear()
        while True:
            self.set_color("R", self.colors["red"] )
            self.set_color("L", self.colors["light_blue"])
            await time.sleep(.25)
            self.set_color("R", self.colors["light_blue"] )
            self.set_color("L", self.colors["red"])
            await time.sleep(.25)
            
    def stop(self):
        self.flag.clear()
        for key in self.devices.keys():
            print( key )
            self.devices[key].value=1

     


colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF, 0X6F00D2, 0xFF5809]




def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def setAllColor(col):   # For example : col = 0x112233
  R_val = (col & 0xff0000) >> 16
  G_val = (col & 0x00ff00) >> 8
  B_val = (col & 0x0000ff) >> 0

  R_val = map(R_val, 0, 255, 0, 1.00)
  G_val = map(G_val, 0, 255, 0, 1.00)
  B_val = map(B_val, 0, 255, 0, 1.00)
  
  L_R.value = 1.0-R_val
  L_G.value = 1.0-G_val
  L_B.value = 1.0-B_val

  R_R.value = 1.0-R_val
  R_G.value = 1.0-G_val
  R_B.value = 1.0-B_val

def setAllRGBColor(R,G,B):   # For example : col = 0x112233

  R_val = map(R, 0, 255, 0, 1.00)
  G_val = map(G, 0, 255, 0, 1.00)
  B_val = map(B, 0, 255, 0, 1.00)
  
  L_R.value = 1.0-R_val
  L_G.value = 1.0-G_val
  L_B.value = 1.0-B_val

  R_R.value = 1.0-R_val
  R_G.value = 1.0-G_val
  R_B.value = 1.0-B_val

def loop():
  while True:
    for col in colors:
      setAllColor(col)
      time.sleep(0.5)

def destroy():
  L_R.stop()
  L_G.stop()
  L_B.stop()
  R_R.stop()
  R_G.stop()
  R_B.stop()

if __name__ == "__main__":

  setup()
  try:
    loop()
  except KeyboardInterrupt:
    destroy()
"""