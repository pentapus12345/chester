import asyncio
import board
import neopixel

class RGB_2:
    def __init__(self, pin=board.D18, count=2, brightness=0.5):
        # pin: the board.Dxx pin where your HAT’s DIN line is wired
        self.pixels = neopixel.NeoPixel(
            pin, count,
            brightness=brightness,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        self.flag = asyncio.Event()

    def set_pixel(self, idx, color):
        r = (color >> 16) & 0xFF
        g = (color >>  8) & 0xFF
        b =  color        & 0xFF
        self.pixels[idx] = (r, g, b)
        self.pixels.show()

    async def talking(self):
        self.flag.clear()
        while not self.flag.is_set():
            # left=0, right=1
            self.set_pixel(0, 0xFF0000)  # left red
            self.set_pixel(1, 0x00FFFF)  # right cyan
            await asyncio.sleep(0.25)
            self.set_pixel(0, 0x00FFFF)
            self.set_pixel(1, 0xFF0000)
            await asyncio.sleep(0.25)
        # turn off when done
        self.set_pixel(0, 0)
        self.set_pixel(1, 0)

    def stop(self):
        self.flag.set()
