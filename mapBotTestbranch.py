import time
import math
import RPi.GPIO as GPIO


# Define the pins for the DRV8825 stepper driver (motor 1)
dir_pin0 = 13
step_pin0 = 19
enable_pin0 = 12
mode_pins0 = (16, 17, 20)

# Define the pins for the DRV8825 stepper driver (motor 2)
dir_pin1 = 24
step_pin1 = 18
enable_pin1 = 4
mode_pins1 = (21, 22, 27)

# Define the delay between steps
delay = 0.0005

turnDirIndicator = False

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the input pins for push buttons
GPIO.setup(26, GPIO.IN)

# Set up the GPIO pins
# motor 1
GPIO.setup(dir_pin0, GPIO.OUT)
GPIO.setup(step_pin0, GPIO.OUT)
GPIO.setup(enable_pin0, GPIO.OUT)

# motor 2
GPIO.setup(dir_pin1, GPIO.OUT)
GPIO.setup(step_pin1, GPIO.OUT)
GPIO.setup(enable_pin1, GPIO.OUT)

# Disable the stepper motor by setting the enable pin to low
GPIO.output(enable_pin0, GPIO.LOW)
GPIO.output(enable_pin1, GPIO.LOW)

print(GPIO.input(26))

# Run code until stop button is pressed
while GPIO.input(26) == GPIO.LOW:
    # Function to let motors spin in opposite direction for driving straight
    def driveStraight(dir, quartRots):
        straightSteps = quartRots*50    # 200 steps = full rotation, 50 steps = 1/4 rotation
        delay = 0.0005                  # smaller delay for faster turn rate
        if dir == 0:    # motors direction set in different directions
            GPIO.output(dir_pin0, GPIO.LOW)
            GPIO.output(dir_pin1, GPIO.HIGH)
        elif dir == 1:  # motors direction set in opposite diretion from dir == 0
            GPIO.output(dir_pin0, GPIO.HIGH)
            GPIO.output(dir_pin1, GPIO.LOW)
        else:
            raise ValueError("dir not a correct value (0 for forwards, 1 for backwards)")
        # motors turn on
        GPIO.output(enable_pin0, GPIO.HIGH)
        GPIO.output(enable_pin1, GPIO.HIGH)
        for i in range(straightSteps):  # motors go set amount of steps
            GPIO.output(step_pin0, GPIO.HIGH)
            GPIO.output(step_pin1, GPIO.HIGH)
            time.sleep(delay)           # delay between steps
            GPIO.output(step_pin0, GPIO.LOW)
            GPIO.output(step_pin1, GPIO.LOW)
            time.sleep(delay)
        # motors turn off
        GPIO.output(enable_pin0, GPIO.LOW)
        GPIO.output(enable_pin1, GPIO.LOW)
        

    # Function to let motors spin in the same direction for turning
    def driveTurn(turnDir, eighthRot):
        turnSteps = eighthRot*63        # !!!SPACEHOLDER!!! steps needed for 45° rotation of robot
        delay = 0.005                   # bigger delay for lower turn rate
        if turnDir == 0:    # motors set in same direction
            GPIO.output(dir_pin0, GPIO.HIGH)
            GPIO.output(dir_pin1, GPIO.HIGH)
        elif turnDir == 1:  # motors set in same opposite direction
            GPIO.output(dir_pin0, GPIO.LOW)
            GPIO.output(dir_pin1, GPIO.LOW)
        else:
            raise ValueError("turnDir not a correct value (0 for left turn, 1 for right turn)")
        # motors turn on
        GPIO.output(enable_pin0, GPIO.HIGH)
        GPIO.output(enable_pin1, GPIO.HIGH)
        for i in range(turnSteps):  # motors go set amount of steps
            GPIO.output(step_pin0, GPIO.HIGH)
            GPIO.output(step_pin1, GPIO.HIGH)
            time.sleep(delay)       # delay between steps
            GPIO.output(step_pin0, GPIO.LOW)
            GPIO.output(step_pin1, GPIO.LOW)
            time.sleep(delay)
        # motors turn off
        GPIO.output(enable_pin0, GPIO.LOW)
        GPIO.output(enable_pin1, GPIO.LOW)

    def wallHit():
        turnDirIndicator = not turnDirIndicator
        driveStraight(1,2)  # get distance from wall
        delay.sleep(1)      # wait
        driveTurn(0, 3)
        vectorCalculate(2)   # does the compass calculation stuff and transmission for later mapping

    def vectorCalculate(quarrots):
        radius = quarrots * 5
        angle = 10 # compass angle
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        return (x, y)
        # TODO: integration of compass angle
        # https://tutorials-raspberrypi.com/build-your-own-raspberry-pi-compass-hmc5883l/
        # https://github.com/Slaveche90/gy271compass
        # https://math.stackexchange.com/questions/260096/find-the-coordinates-of-a-point-on-a-circle
        # x=r*sin, y=r*cos




    time.sleep(0.25)

    driveStraight(0, 40)
    time.sleep(0.5)
    driveTurn(0, 4)
else:

    # Clean up the GPIO pins
    GPIO.cleanup()
