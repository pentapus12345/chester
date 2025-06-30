from Classes.ServoControl import ServoControl
import time
s = ServoControl()

s.set_angle(1,80)
time.sleep(1)
s.set_angle(1,120)

s.set_angle(2,90)
time.sleep(1)
s.set_angle(2,0)
time.sleep(1)
s.set_angle(2,180)
time.sleep(1)
s.set_angle(2,90)