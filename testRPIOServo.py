from Classes.RPIOServo import ServoCtrl
import time

scGear = ServoCtrl()
scGear.moveInit()

    
value = 0
dir = 1
#while 1:
#    scGear.moveAngle(1, -50)
#    time.sleep(1)
#    scGear.moveAngle(1, 50)
#    time.sleep(1)

scGear.moveAngle(1,50)
scGear.moveAngle(2,50)