import time
import RPi.GPIO as GPIO

# Define the pins for the DRV8825 stepper driver
dir_pin = 24
step_pin = 18
enable_pin = 4

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pins
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(enable_pin, GPIO.OUT)

# Disable the stepper motor by setting the enable pin to low
GPIO.output(enable_pin, GPIO.LOW)

# Set the direction of the stepper motor
GPIO.output(dir_pin, GPIO.HIGH)

# Define the number of steps for the stepper motor to rotate
steps = 1000

# Define the delay time between steps
delay = 0.0005

# Enable the stepper motor by setting the enable pin to high
GPIO.output(enable_pin, GPIO.HIGH)

# Loop through the steps and control the stepper motor
for i in range(steps):
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(delay)

# Disable the stepper motor by setting the enable pin to low
GPIO.output(enable_pin, GPIO.LOW)

# Clean up the GPIO pins
GPIO.cleanup()