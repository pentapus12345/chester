from Classes.HeadMover import HeadMover
from Classes.ServoControl import ServoControl
s = ServoControl()
h = HeadMover(s)

h.look_in_direction(0,90,1)
