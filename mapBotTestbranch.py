import time
import RPi.GPIO as GPIO


# Define the pins for the DRV8825 stepper driver
dir_pin0 = 13
step_pin0 = 19
enable_pin0 = 12
mode_pins0 = (16, 17, 20)

# Define the pins for the DRV8825 stepper driver
dir_pin1 = 24
step_pin1 = 18
enable_pin1 = 4
mode_pins1 = (21, 22, 27)

delay = 0.0005

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)


# Set up the GPIO pins
GPIO.setup(dir_pin0, GPIO.OUT)
GPIO.setup(step_pin0, GPIO.OUT)
GPIO.setup(enable_pin0, GPIO.OUT)

GPIO.setup(dir_pin1, GPIO.OUT)
GPIO.setup(step_pin1, GPIO.OUT)
GPIO.setup(enable_pin1, GPIO.OUT)


# Disable the stepper motor by setting the enable pin to low
GPIO.output(enable_pin0, GPIO.LOW)
GPIO.output(enable_pin1, GPIO.LOW)




def driveStraight(dir, quartRots):
    straightSteps = quartRots*50
    delay = 0.0005
    if dir == 0:
        GPIO.output(dir_pin0, GPIO.LOW)
        GPIO.output(dir_pin1, GPIO.HIGH)
    elif dir == 1:
        GPIO.output(dir_pin0, GPIO.HIGH)
        GPIO.output(dir_pin1, GPIO.LOW)
    else:
        raise ValueError("dir not a correct value (0 for forwards, 1 for backwards)")
    
    GPIO.output(enable_pin0, GPIO.HIGH)
    GPIO.output(enable_pin1, GPIO.HIGH)

    for i in range(straightSteps):
        GPIO.output(step_pin0, GPIO.HIGH)
        GPIO.output(step_pin1, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(step_pin0, GPIO.LOW)
        GPIO.output(step_pin1, GPIO.LOW)
        time.sleep(delay)

    GPIO.output(enable_pin0, GPIO.LOW)
    GPIO.output(enable_pin1, GPIO.LOW)

def driveGay(turnDir, eighthRot):
    turnSteps = eighthRot*50
    delay = 0.001
    if turnDir == 0:
        GPIO.output(dir_pin0, GPIO.HIGH)
        GPIO.output(dir_pin1, GPIO.HIGH)
    elif turnDir == 1:
        GPIO.output(dir_pin0, GPIO.LOW)
        GPIO.output(dir_pin1, GPIO.LOW)
    else:
        raise ValueError("dir not a correct value (0 for left turn, 1 for right turn)")

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
driveGay(0, 20)




"""
# Set the direction of the stepper motor
GPIO.output(dir_pin0, GPIO.LOW)
GPIO.output(dir_pin1, GPIO.HIGH)

# Define the number of steps for the stepper motor to rotate
steps = 1000

# Enable the stepper motor by setting the enable pin to high
GPIO.output(enable_pin0, GPIO.HIGH)
GPIO.output(enable_pin1, GPIO.HIGH)

# Loop through the steps and control the stepper motor
for i in range(steps):
    GPIO.output(step_pin0, GPIO.HIGH)
    GPIO.output(step_pin1, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(step_pin0, GPIO.LOW)
    GPIO.output(step_pin1, GPIO.LOW)
    time.sleep(delay)

# Disable the stepper motor by setting the enable pin to low
GPIO.output(enable_pin0, GPIO.LOW)
GPIO.output(enable_pin1, GPIO.LOW)






time.sleep(0.5)






# Set the direction of the stepper motor
GPIO.output(dir_pin0, GPIO.HIGH)
GPIO.output(dir_pin1, GPIO.LOW)

# Define the number of steps for the stepper motor to rotate
steps = 1000

# Define the delay time between steps
delay = 0.0005

# Enable the stepper motor by setting the enable pin to high
GPIO.output(enable_pin0, GPIO.HIGH)
GPIO.output(enable_pin1, GPIO.HIGH)

# Loop through the steps and control the stepper motor
for i in range(steps):
    GPIO.output(step_pin0, GPIO.HIGH)
    GPIO.output(step_pin1, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(step_pin0, GPIO.LOW)
    GPIO.output(step_pin1, GPIO.LOW)
    time.sleep(delay)

# Disable the stepper motor by setting the enable pin to low
GPIO.output(enable_pin0, GPIO.LOW)
GPIO.output(enable_pin1, GPIO.LOW)
"""




# Clean up the GPIO pins
GPIO.cleanup()