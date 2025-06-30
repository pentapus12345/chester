from Classes.RGBLED import RGBLED
import asyncio
import time

#led = RGBLED()

colors = {"red":0xFF0000, "green":0x00FF00, "blue":0x0000FF, "yellow":0xFFFF00, "purple":0xFF00FF, "light_blue":0x00FFFF, "light_purple":0X6F00D2, "orange":0xFF5809}

#async def talk():
#   await led.talking()


#loop = asyncio.create_task(talk())
#time.sleep(2)
#loop.stop()
led = RGBLED()
async def test():

    task = asyncio.create_task(led.talking())
    # let it flash for 2 seconds
    await asyncio.sleep(6)
    # tell the coroutine to clean up
    led.stop()
    # wait for it to finish tearing down
    await task


asyncio.run(test())

led.set_color("L",colors["red"])
time.sleep(1)