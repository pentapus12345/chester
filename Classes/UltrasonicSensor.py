from gpiozero import DistanceSensor
from json import load
from asyncio import Event


class UltrasonicSensor(object):
    def __init__(self):
        with open("Assets/parameters.json") as f:
            data = load(f)
            ultrsonic_sensor = data["ultrasonic_sensor"]
            echo = ultrsonic_sensor["echo"]
            trigger = ultrsonic_sensor["trigger"]
        self.sensor = DistanceSensor(echo=echo, trigger=trigger,max_distance=2)


    def getDistance(self):
        try:
            d = self.sensor.distance
            return (d or float('inf')) * 100
        except Exception as e:
            print("⚠️ getDistance error:", e)
            return float('inf')
    
    async def too_close(self, flag):
        too_close = False
        while not too_close:
            dist = self.getDistance()
            if dist < 20:
                flag.set()
                print( "uh oh")
                too_close = True
                



