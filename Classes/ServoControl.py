import busio
from board import SCL, SDA, I2C
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class ServoControl(object):

    def __init__(self):
        # create a persistent I2C bus handle (no try_lock loop)
        i2c = I2C()  
        self.pwm_servo = PCA9685(i2c, address=0x5f)
        self.pwm_servo.frequency = 50
        #self.i2c = busio.I2C(SCL, SDA)
        # initialize the PCA9685 on that bus
        #self.pwm_servo = PCA9685(self.i2c, address=0x5f)
        #self.pwm_servo.frequency = 50

        self.pos = [90, 90, 90]
        self.initialize()

            


    def set_angle(self, servo_id: int, angle: int)->None:
        servo_angle = servo.Servo(self.pwm_servo.channels[servo_id], min_pulse=500, max_pulse=2400,actuation_range=180)
        servo_angle.angle = angle
        self.pos[servo_id] = angle

    def get_angle(self, servo_id: int)->int:
        return( self.pos[servo_id] )
    
    def initialize(self):
        for i in range(3):
            self.set_angle(i, self.pos[i])