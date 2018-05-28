from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
import xbox


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).

#pwm = Adafruit_PCA9685.PCA9685()   #COMMENT WHEN TESTING WITHOUT I2C ATTACHED
#pwm.set_pwm_freq(60)               #COMMENT WHEN TESTING WITHOUT I2C ATTACHED


# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

#Initialize joystick
joy = xbox.Joystick()


# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

steer = 0 #channels on board
gas = 4

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    #pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
#pwm.set_pwm_freq(60)

def map_pulse(val, inMin, inMax, outMin, outMax):
    return (val - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
def gas_pulse(y):
    return map_pulse(y, 0, 1, 0, 496); # edit later, 10% speed
def steer_pulse(x):
    return map_pulse(x, -1, 1, servo_min, servo_max) #check ranges of steering




print('Now taking controller input...')
flag = False
while not joy.Back():
    # Move servo on channel O between extremes.

    y = joy.leftY()
    x = joy.rightX()
    if y < 0:
       y = 0
    print "X: ", steer_pulse(x), " y: ", gas_pulse(y)
    time.sleep(0.1) #Just to stop it sending IO as fast as possible

    #pwm.set_pwm(steer, 0, servo_min + (servo_max - servo_min)*x)
    #pwm.set_pwm(gas, 0, servo_min + (servo_max - servo_min)*y)
    
joy.close()

