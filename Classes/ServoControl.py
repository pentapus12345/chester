from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import time
import threading

class ServoControl(threading.Thread):

    def __init__(self):
        # keep this object alive (don’t use a with-block!)
        #i2c = busio.I2C(SCL, SDA)
        #self.pwm_servo = PCA9685(i2c, address=0x5f)
        #self.pwm_servo.frequency = 50
        # create a persistent I2C bus handle (no try_lock loop)
        #i2c = I2C()  
        #self.pwm_servo.frequency = 50
        ##self.pwm_servo = PCA9685(i2c, address=0x5f)
        #self.i2c = busio.I2C(SCL, SDA)
        # initialize the PCA9685 on that bus
        #self.pwm_servo = PCA9685(self.i2c, address=0x5f)
        #self.pwm_servo.frequency = 50
        self.ctrlRangeMax = 180
        self.ctrlRangeMin = 0
        self.angleRange = 180
        self.scMode = 'auto'
        self.scTime = 2.0
        self.scSteps = 30
        self.scDelay = 0.09
        self.scMoveTime = 0.09
        self.pos = [90, 90, 90]
        super(ServoControl, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()
        #self.initialize()

    def set_angle(self,ID, angle):
        # global i2c,pwm_servo
        i2c = busio.I2C(SCL, SDA)
        # Create a simple PCA9685 class instance.
        pwm_servo = PCA9685(i2c, address=0x5f) #default 0x40

        pwm_servo.frequency = 50
        servo_angle = servo.Servo(pwm_servo.channels[ID], min_pulse=500, max_pulse=2400,actuation_range=180)
        servo_angle.angle = angle
    def pause(self):
        print('......................pause..........................')
        self.__flag.clear()
    
    def resume(self):
        print('resume')
        self.__flag.set()

    f="""def __init__(self):
        # 1) Open the Pi's I²C-1 bus via smbus2
        bus = SMBus(1)

        # 2) Wrap it in the BusDevice helper
        device = I2CDevice(bus, 0x5f)

        # 3) Instantiate PCA9685 on that real I²C bus
        self.pwm_servo = PCA9685(i2c_device=device)
        self.pwm_servo.frequency = 50

        # … rest of your init …
        self.pos = [90, 90, 90]
        self.initialize()


    def set_angle(self, servo_id: int, angle: int)->None:
        i2c = busio.I2C(SCL, SDA)
        pwm_servo = PCA9685(i2c, address=0x5f)
        pwm_servo.frequency = 50
        servo_angle = servo.Servo(pwm_servo.channels[servo_id], min_pulse=500, max_pulse=2400,actuation_range=180)
        servo_angle.angle = angle
        self.pos[servo_id] = angle
        time.sleep(.01)

    def get_angle(self, servo_id: int)->int:
        return( self.pos[servo_id] )
    
    def initialize(self):
        for i in range(3):
            self.set_angle(i, self.pos[i])
            time.sleep(.01)"""