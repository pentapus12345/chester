from Classes.Mover import Mover
from Classes.UltrasonicSensor import UltrasonicSensor
from Classes.Listener import Listener
import asyncio

class Chester(object):
    def __init__(self):
        self.mover = Mover()
        self.sensor = UltrasonicSensor()
        self.listener = Listener()
        self.listener.setVerbose( False )
        self.input_message = ""

    #async def do_not_crash(self):
    #    flag = asyncio.Event()
    #    asyncio.create_task(self.sensor.too_close(flag))
    #    await flag.wait()
    #    self.mover.setThrottle(0)
    #    print( "too close!")




    async def do_not_crash(self):
        asyncio.create_task( self.get_message() )

    #async def get_message(self):
    #    await self.input_message = self.listener.listen()
    #    await self.execute_message( self.input_message )

    async def listen_loop(self):
        while True:
            sentence = await self.get_message()
            if sentence:
                await self.execute_message(sentence)


    async def get_message(self):
        """
        Block until the user talks, then return the final sentence.
        Runs the synchronous Listener.listen() in a background thread
        so the asyncio event-loop stays responsive.
        """
        msg = await asyncio.to_thread(self.listener.listen)   # ← key line
        return msg.strip()

    async def execute_message(self, msg: str):
        print( msg )

    async def main(self):
        await self.listen_loop()

    def run(self):
        asyncio.run(self.main())
        #loop = asyncio.get_event_loop()
        #loop.create_task(self.do_not_crash())
        #loop.create_task(self.get_message())
        #self.mover.setThrottle(.5)
        #asyncio.run( self.do_not_crash)
        #try:
        #    loop.run_forever()
        #finally:
        #    loop.close()


    