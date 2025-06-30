import asyncio
from Classes.RGB_2 import RGB_2
import board

async def main():

    led = RGB_2(pin=board.D12, count=2)
    task = asyncio.create_task(led.talking())
    # let it flash for 5 seconds
    await asyncio.sleep(5)
    led.stop()
    await task

if __name__ == "__main__":
    asyncio.run(main())