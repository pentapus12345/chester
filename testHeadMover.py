from Classes.HeadMover import HeadMover
from Classes.ServoControl import ServoControl
s = ServoControl()
h = HeadMover(s)
import time

s.set_angle(1,120)
s.set_angle(2,120)

time.sleep(1)
h.look_in_direction(theta=20,phi=20,time_to_take=2)

