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
        now_theta = self.servo_control.get_angle(self.hor_id)-90
        now_phi = self.servo_control.get_angle(self.hor_id)
        delta_theta = theta - now_theta
        delta_phi = phi - now_phi
        steps = 10
        delta_t = time_to_take/steps
        for i in range(steps):
            factor = steps-i
  
            
            new_theta = theta - (theta-now_theta)*factor/steps
            print( f"factor: {factor}, now_theta: {now_theta}, new_theta: {new_theta}")
            f="""
            self.servo_control.set_angle(self.hor_id,new_theta )
            time.sleep(delta_t)"""

        
