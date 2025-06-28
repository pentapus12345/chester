from adafruit_motor import motor
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from Classes.UltrasonicSensor import UltrasonicSensor
import time

class Mover(object):
    def __init__(self):
        self.motor_channel_1 =  14      #Define the positive pole of M1
        self.motor_channel_2 =  15      #Define the negative pole of M1
        self.i2c = busio.I2C(SCL, SDA)
        self.pwm_motor = PCA9685(self.i2c, address=0x5f) #default 0x40
        self.motor = motor.DCMotor(self.pwm_motor.channels[self.motor_channel_1],
                                    self.pwm_motor.channels[self.motor_channel_2])
        self.motor.decay_mode = motor.SLOW_DECAY

        self.speed = .2
        self.pwm_motor.frequency = 50 # a good freq for this kind of motor

        #self.sensor = UltrasonicSensor()
 

    
    def setThrottle(self, throttle: float)->None:
        self.motor.throttle = throttle


    async def backup(self, angle: int)->None:
        self.setThrottle(-.3)
        time.sleep(1)
        self.setThrottle(0)