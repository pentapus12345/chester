from Classes.Mover import Mover
from Classes.UltrasonicSensor import UltrasonicSensor
import time

mover = Mover()
sensor = UltrasonicSensor()


speed_factor = []


initialDistance = sensor.getDistance()
distance = []
print( initialDistance )
mover.setThrottle(.5)
for i in range(10):
    time.sleep(1)
    finalDistance = sensor.getDistance()
    distance.append(initialDistance-finalDistance)
    mover.setThrottle(-.5)
    time.sleep(1)
    mover.setThrottle(.5)
mover.setThrottle(0)

print( distance )



initialDistance = sensor.getDistance()
mover.setThrottle(.5)
time.sleep(1)
mover.setThrottle(0)


#for i in range(1,11):
#    for j in [-1,1]:
#        throttle = i/10*j
#        initialDistance = sensor.getDistance()
#        mover.setThrottle(throttle)
#        time.sleep(1)
#        mover.setThrottle(0)
#        finalDistance = sensor.getDistance()
#        speed_factor.append((initialDistance-finalDistance)/throttle)

#print( speed_factor)


