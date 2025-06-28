from Classes.Mover import Mover
from Classes.UltrasonicSensor import UltrasonicSensor
import time

mover = Mover()
sensor = UltrasonicSensor()

print( sensor.getDistance())

#mover.setSpeed(-1)
#time.sleep(1)
#mover.setSpeed(0)