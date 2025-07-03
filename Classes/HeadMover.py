from Classes.ServoControl import ServoControl
import time

class HeadMover(object):
    def __init__(self, servo_control: ServoControl):
        self.servo_control=servo_control
        self.hor_id = 1
        self.vert_id = 2



    def look_in_direction(self, theta: int, phi: int, time_to_take: float):
        """Tells the head to look in a direction defined by spherical coordinates theta and phi with
        lookking in the direction of the x-axis being straight ahead, moves to this position in the time given by time"""
        if time_to_take<=0:
            time_to_take=.1
        old_theta = self.servo_control.get_angle(self.hor_id)
        old_phi = self.servo_control.get_angle(self.vert_id)
        steps = 2
        delta_t = time_to_take/steps
        for i in range(steps):
            factor = (steps-i)/steps
  
            
            new_theta = theta - (theta-old_theta)*factor
            new_phi = phi - (phi-old_phi)*factor
            print( f"factor: {factor}, goal_theta: {theta}, new_theta: {new_theta}")
            print( f"factor: {factor}, goal_phi: {phi}, new_phi: {new_phi}")
            self.servo_control.set_angle(self.hor_id,new_phi )
            self.servo_control.set_angle(self.vert_id,new_theta)
            time.sleep(delta_t)

        
