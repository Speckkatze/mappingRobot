import time
import math
import RPi.GPIO as GPIO
from PIL import Image

# generate white png to function as map
map = Image.new("RGB", (1000, 1000), (255, 255, 255))
map.save("mapOfRoom.png")   # save map

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
straightStepCounter = 0
turnStepCounter = 0
vectorArray = []
angle = 0                   # 11.2 turn steps = 1° turn 
# coords start out in the middle of the png
xCoord = 500
yCoord = 500
isBumped = True


turnDirIndicator = False

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the input pins for push buttons
GPIO.setup(11, GPIO.IN) # off switch
GPIO.setup(8, GPIO.IN)  # bumper 1 (left)
GPIO.setup(9, GPIO.IN)  # bumper 2 (middle)
GPIO.setup(23, GPIO.IN) # bumper 3 (right)

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


# Run code until stop button is pressed
while GPIO.input(11) == GPIO.LOW:
    # Function to let motors spin in opposite direction for driving straight


    def driveStraight(dir, quartRots):
        global isBumped
        isBumped = True
        straightStepCounter = 0
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
        for i in range(quartRots):
            if isBumped:
                for i in range(8):
                    if stopButtonPress():
                        break
                    if bumper1Press() or bumper2Press() or bumper3Press():
                        isBumped = False
                        vectorCalculate(straightStepCounter, 0)
                        if bumper1Press() or bumper2Press():
                            wallHit(1)                          # turn right when hit with left or middle bumper
                        elif bumper3Press():
                            wallHit(0)                          # turn left when hit with right bumper
                        break
                    for i in range(50):  # motors go set amount of steps
                        GPIO.output(step_pin0, GPIO.HIGH)
                        GPIO.output(step_pin1, GPIO.HIGH)
                        time.sleep(delay)           # delay between steps
                        GPIO.output(step_pin0, GPIO.LOW)
                        GPIO.output(step_pin1, GPIO.LOW)
                        time.sleep(delay)  
                    straightStepCounter = straightStepCounter + 50
        # motors turn off

        # TODO vector calculate
        if dir == 0:
            vectorCalculate(400 * quartRots, 1)
        elif dir == 1:
            vectorCalculate(-400 * quartRots, 1)
        
        GPIO.output(enable_pin0, GPIO.LOW)
        GPIO.output(enable_pin1, GPIO.LOW)
        

    # Function to let motors spin in the same direction for turning
    def driveTurn(turnDir, eighthRot):
        turnStepCounter = 0
        turnSteps = eighthRot*8       # steps needed for 45° rotation of robot
        delay = 0.002                   # bigger delay for lower turn rate
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
        for i in range(eighthRot):
            for i in range(8):
                if stopButtonPress():
                    break
                for i in range(63):  # motors go set amount of steps
                    GPIO.output(step_pin0, GPIO.HIGH)
                    GPIO.output(step_pin1, GPIO.HIGH)
                    time.sleep(delay)       # delay between steps
                    GPIO.output(step_pin0, GPIO.LOW)
                    GPIO.output(step_pin1, GPIO.LOW)
                    time.sleep(delay)
                turnStepCounter = turnStepCounter + 63
        # motors turn off
        print(angle)
        GPIO.output(enable_pin0, GPIO.LOW)
        GPIO.output(enable_pin1, GPIO.LOW)
        if turnDir == 0:
            addDegrees(0, turnStepCounter)
            print(angle)
        elif turnDir == 1:
            addDegrees(1, turnStepCounter)
            print(angle)

    def wallHit(dir):
        delay = 0.0005                  # smaller delay for faster turn rate
        GPIO.output(dir_pin0, GPIO.HIGH)
        GPIO.output(dir_pin1, GPIO.LOW)
        # motors turn on
        GPIO.output(enable_pin0, GPIO.HIGH)
        GPIO.output(enable_pin1, GPIO.HIGH)
        for i in range(1600):  # motors go set amount of steps
            GPIO.output(step_pin0, GPIO.HIGH)
            GPIO.output(step_pin1, GPIO.HIGH)
            time.sleep(delay)           # delay between steps
            GPIO.output(step_pin0, GPIO.LOW)
            GPIO.output(step_pin1, GPIO.LOW)
            time.sleep(delay)  
        GPIO.output(enable_pin0, GPIO.LOW)
        GPIO.output(enable_pin1, GPIO.LOW)
        vectorCalculate(-1600, 1)
        time.sleep(1)      # wait
        driveTurn(dir, 3)

    def vectorCalculate(steps, wallIndicator):
        radius = steps * 0.1 * 0.13125
        global angle
        global vectorArray
        global xCoord
        global yCoord
        x = 0
        y = 0
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        xCoord += x
        yCoord += y
        vectorArray.append([x,y])
        plotPointOnMap(wallIndicator, xCoord, yCoord)

        # TODO: integration of compass angle
        # https://tutorials-raspberrypi.com/build-your-own-raspberry-pi-compass-hmc5883l/
        # https://github.com/Slaveche90/gy271compass
        # https://math.stackexchange.com/questions/260096/find-the-coordinates-of-a-point-on-a-circle
        # x=r*sin, y=r*cos

    def stopButtonPress():
        if GPIO.input(11) == GPIO.HIGH:
            return True
    def bumper1Press():
        if GPIO.input(8) == GPIO.HIGH:
            print("Bumper 1 pressed")
            return True
    def bumper2Press():
        if GPIO.input(9) == GPIO.HIGH:
            print("Bumper 2 pressed")
            return True
    def bumper3Press():
        if GPIO.input(23) == GPIO.HIGH:
            print("Bumper 3 pressed")
            return True

    # function to change degrees, takes direction and actual rotation distance into account. Also makes sure that angle is always 1-360°
    def addDegrees(direction, degAdd):
        global angle
        if direction == 1:
            angle = angle - degAdd / 11.70202
        elif direction == 0:
            angle = angle + degAdd / 11.70202

        if angle > 360:
            angle -= 360
        elif angle < 1:
            angle += 360

    def plotPointOnMap(wallOrNoWall, x, y):
        map = Image.open("mapOfRoom.png")
        pixels = map.load()
        if wallOrNoWall == 0:
            pixels[x, y] = (255, 0, 0)
        elif wallOrNoWall == 1:
            pixels[x, y] = (0, 0, 0)
        map.save("mapOfRoom.png")
        
    time.sleep(0.1)    # time delay between loops

    driveStraight(0, 4)
else:

    # Clean up the GPIO pins
    map.save("mapOfRoom.png")
    print(vectorArray)
    GPIO.cleanup()
