from Classes.Mover import Mover
from Classes.UltrasonicSensor import UltrasonicSensor
from Classes.Listener import Listener
from Classes.Agent import Agent
from Classes.Voice import Voice
import asyncio
from dotenv import load_dotenv
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
print( os.getenv("OPENAI_API_KEY"))

class Chester(object):
    def __init__(self):
        self.mover = Mover()
        self.sensor = UltrasonicSensor()
        self.listener = Listener()
        self.voice = Voice()
        self.agent = Agent([self.voice.say, self.go])

        self.input_message = ""
        #api_key = os.getenv("OPEN_API_KEY")
        self.init()


    #async def do_not_crash(self):
    #    flag = asyncio.Event()
    #    asyncio.create_task(self.sensor.too_close(flag))
    #    await flag.wait()
    #    self.mover.setThrottle(0)
    #    print( "too close!")

    def init(self):
        self.mover.setThrottle(0)
        self.listener.set_print_to_screen(True)
        self.verbose = False
        self.voice.set_print_to_screen(True)
        self.agent.verbose = False
    

    async def go(self):
        """Starts Chester moving forward"""
        print( "i'm going forward now")
        self.mover.setThrottle(.3)
    
    async def say(self, msg: str):
        """This function passes msg to the voice engine, 
        which synthesizes a voice and speaks the text of the msg"""
        if self.verbose:
            print( f"I'm about to say {msg} using self.voice.say")
        await asyncio.to_thread(self.voice.say(msg))

    async def do_not_crash(self):
        while True:
            if self.sensor.getDistance() < .3:
                await self.mover.backup(0)

            
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
        if self.verbose:
            print( f"executing message: {msg}")
        await self.agent.ask_agent(msg)



    async def main(self):
        await self.listen_loop()

    def run(self):
        try:
            asyncio.run(self.main())
            #loop = asyncio.get_event_loop()
            #loop.create_task(self.do_not_crash())
            #loop.create_task(self.get_message())
            #self.mover.setThrottle(.5)
            asyncio.run( self.do_not_crash())
        finally:
            self.mover.setThrottle(0)
        #try:
        #    loop.run_forever()
        #finally:
        #    loop.close()


    