import time
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

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)


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
    GPIO.output(enable_pin0, GPIO.LOW)
    GPIO.output(enable_pin1, GPIO.LOW)
    

def driveTurn(turnDir, eighthRot):
    turnSteps = eighthRot*50
    delay = 0.001
    if turnDir == 0:
        GPIO.output(dir_pin0, GPIO.HIGH)
        GPIO.output(dir_pin1, GPIO.HIGH)
    elif turnDir == 1:
        GPIO.output(dir_pin0, GPIO.LOW)
        GPIO.output(dir_pin1, GPIO.LOW)
    else:
        raise ValueError("turnDir not a correct value (0 for left turn, 1 for right turn)")
    GPIO.output(enable_pin0, GPIO.HIGH)
    GPIO.output(enable_pin1, GPIO.HIGH)
    
    
    for i in range(turnSteps):
        GPIO.output(step_pin0, GPIO.HIGH)
        GPIO.output(step_pin1, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(step_pin0, GPIO.LOW)
        GPIO.output(step_pin1, GPIO.LOW)
        time.sleep(delay)

    GPIO.output(enable_pin0, GPIO.LOW)
    GPIO.output(enable_pin1, GPIO.LOW)

driveStraight(0, 40)
time.sleep(0.5)
driveTurn(0, 20)



# Clean up the GPIO pins
GPIO.cleanup()
